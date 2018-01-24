import urllib.parse
import concurrent.futures as cc
from collections import namedtuple
from gw2apiwrapper.functions import getJson, typer
import gw2apiwrapper.descriptions as eps


class AccountAPI:
    def __init__(self, api_key):
        '''
        Initalize various bits of account information.
        '''
        self.api_key = api_key
        self.header = {'Authorization': 'Bearer ' + self.api_key}
        self.url = 'https://api.guildwars2.com/v2/'

        data = self.getJson('tokeninfo')
        self.permissions = data['permissions']

        data = self.getJson('account/')

        self.accountID = data['id']
        self.username = data['name']
        self.world = data['world']
        self.guilds = data['guilds']

    def getJson(self, api):
        '''
        Simple wrapper for less typing.
        '''
        return getJson(self.url + api, self.header)

    def checkPermission(self, apiName):
        '''
        Fail if we're missing the required permission.

        Raises PermissionError exception on failure.
        '''
        if apiName not in self.permissions:
            # PEP8 compliance Matt. It's the devil.
            # It makes me do bad things. But the line is pink
            # and it must not be pink.
            raise PermissionError(apiName)

    def getNodes(self):
        '''
        Gets the name of the resource nodes you have unlocked
        for your home instance.

        Info: https://wiki.guildwars2.com/wiki/API:2/account/home/nodes

        Returns a list of names.
        '''
        self.checkPermission('progression')

        return self.getJson('account/home/nodes')

    def getCats(self):
        '''
        Get the details of your...cat ownership...Why
        does this exist?

        Returned a simple dictoinary represented by the data
        at https://wiki.guildwars2.com/wiki/API:2/account/home/cats
        '''
        self.checkPermission('progression')

        # I won't dignify this with more of a response.
        return self.getJson('account/home/cats')

    @typer
    def getRaids(self):
        '''
        Get the details of your completed dungeons from
        the official API.

        NOTE: I can't test if this works as I don't do raids.
        If you do, feel free to send me a message so I can verify it.
        '''
        self.checkPermission('progression')

    def getGuild(self, guildID):
        '''
        Get the extended details of a guild the API key we are
        authenticated to is a member of.
        '''
        self.checkPermission('guilds')

        # Build our tuple.
        jsonData = self.getJson('guild/{}'.format(guildID))
        obj = namedtuple('Guild', jsonData.keys())

        return obj(**jsonData)

    @typer
    def getDungeons(self):
        '''
        Gets the details of your completed dungeons from
        the official API.

        NOTE: I can't test if this works, I don't do dungeons.
        If you do, feel free to send me a message so I can verify it.
        '''
        self.checkPermission('progression')

    @typer
    def getFinishers(self):
        '''
        Gets the details of your unlocked finishers from
        the official API.

        Contains a list of dictionaries with the following keys:

        id        - (int) ID of Finisher
        permanent - (Boolean) True/false for permanancy of finisher.
        object    - (Item) Object representing unlock_item for finisher.
        '''
        self.checkPermission('unlocks')

    def getWallet(self):
        '''
        Gets your money and money related accessories.
        So Laurels, Bandit Crests, the Works.

        Contains a list of dictionaries containing the
        following keys:

        id          - (int) ID of item/currency.
        description - (str) Description of item/currency.
        icon        - (str) URL of icon assest of item/currency.
        name        - (str) name of item/currency.
        count       - (int) Amount of item/currency.
        order       - (int) Ordering index for least/greatest.
        '''
        self.checkPermission('wallet')

        # Doesn't require authentication.
        currencyJSON = self.getJson('currencies?ids=all')

        # Does require authentication.
        walletJSON = self.getJson('account/wallet')

        for currency in currencyJSON:
            for item in walletJSON:
                if currency['id'] == item['id']:
                    currency.update({'count': item['value']})

        # Set the objects 'wallet' attribute.
        self.wallet = currencyJSON

        return(self.wallet)

    @typer
    def getRecipes(self):
        '''
        Gets your unlocked recipes and builds objects based off
        the returned JSON from the official Guild Wars 2 API.

        Returns list of Recipe objects. (see descriptions)
        '''
        self.checkPermission('unlocks')

    @typer
    def getTitles(self):
        '''
        Gets your Titles and builds Title objects based off
        the returned JSON from the official Guild Wars 2 API.

        Note: This one can take a few seconds to finish.
        '''
        self.checkPermission('progression')

    @typer
    def getBank(self):
        '''
        Gets your banks raw JSON via the Guild Wars 2 official
        API and stores it in the object.

        Returns a list of dictionaries which have keys:
        id        - (int) The item's ID.
        count     - (int) The amount of items in the item stack.
        object    - (Item)
        skin      - (int, optional) If not default skin, its ID.
        upgrades  - (list, optional) IDs for each rune/signet on the item.
        infusions - (list, optional) IDs for each infusion on the item.

        '''
        self.checkPermission('inventories')

    @typer
    def getAchievements(self):
        '''
        Gets your achievements raw JSON via the Guild Wars 2
        official API and stores an Achievement objects based
        off the IDs inside.

        Returns a list of dictionaries with the following keys:
        id      - (int) The achievement's ID.
        object  - (Achievement) The object representing achiement.
        current - (int) The current progress on the achivement.
        max     - (int) The total progress needed to be finished.
        done    - (boolean) True/False for if achievement is finished.

        '''
        self.checkPermission('progression')

    @typer
    def getMaterials(self):
        '''
        Gets your materials raw JSON via the Guild Wars 2 official
        API and stores it in the object.

        Returns a list of dictionaries which have keys:

        id       - (int) The item ID of the material.
        category - (int) The material category the item belongs to.
        count    - (int) The amount of material in storage.
        object   - (Item) The object representing what's in slot.

        '''
        self.checkPermission('inventories')

    @typer
    def getOutfits(self):
        '''
        Get your unlocked outfits from the Guild Wars 2 official
        outfit API.

        Returns a list of Outfit objects (see descriptions)
        '''
        self.checkPermission('unlocks')

    @typer
    def getMasteries(self):
        '''
        Gets the accounts current masteries from the Guild Wars 2
        official API and stores objects representing them.

        Returns a list of dictionaries with the following keys:

        id     - (int) The mastery ID.
        level  - (int) The current level of said mastery.
        object - (Mastery) The object representing the mastery.
        '''
        self.checkPermission('progression')

    @typer
    def getInventory(self):
        '''
        Queries the shared inventory API endpoint for
        Guild wars 2.

        Returns list of dictionaries.

        id      - (int) Item ID in slot.
        count   - (int) Amount of item in slot.
        binding - (str) The bound/binding status of item.
        object  - (Item) Object representing item in slot.

        DEV NOTE: I do not have shared invetory slots.
        This method is experimental until I can get one
        or a key is shared that has one. Use at your own peril.
        '''
        self.checkPermission('inventories')

    def getTradeHistory(self):
        '''
        Gets all trading post activity on your account
        via the API.

        Assigns (and returns) the following attributes.

        self.buying - Dictionary of keys:
            'item_id', 'price', 'id', 'created', 'quantity'

        self.bought -  Dictionary of keys:
            'item_id', 'price', 'id', 'created', 'quantity',
            'purchased'

        self.selling - Dictionary of keys:
            'item_id', 'price', 'id', 'created', 'quantity'

        self.sold - Dictionary of keys:
            'item_id', 'price', 'id', 'created', 'quantity'
            'purchased'
        '''
        # Check for permissions first.
        self.checkPermission('tradingpost')

        # This one is a bit tricky. Decided to just get
        # all of the data for transactions instead of choosing.
        currentURL = 'commerce/transactions/current'

        # Get the data.
        buyingData = self.getJson(currentURL + '/buys')
        sellingData = self.getJson(currentURL + '/sells')

        # If there is no buying data, set it to None.
        # You know, like API should have.
        if len(buyingData) > 0:
            self.buying = buyingData
        else:
            self.buying = None  # pragma: no cover

        # Same here.
        if len(sellingData) > 0:
            self.selling = sellingData
        else:
            self.selling = None  # pragma: no cover

        # Get our transaction HISTORY. Only completed trades.
        # PEP8...please.
        historyURL = 'commerce/transactions/history/'
        boughtData = self.getJson(historyURL + 'buys')
        soldData = self.getJson(historyURL + 'sells')

        # As before, sanitize this.
        if len(boughtData) > 0:
            self.bought = boughtData  # pragma: no cover
        else:
            self.bought = None  # pragma: no cover

        # And this.
        if len(soldData) > 0:
            self.sold = soldData  # pragma: no cover
        else:
            self.sold = None  # pragma: no cover

        # Return the information...for use immediately?
        return({'sold': self.sold, 'bought': self.bought,
                'selling': self.selling, 'buying': self.buying})

    @typer
    def getCharacters(self):
        '''
        Uses the Guild Wars 2 API to query for a given
        character name on your account.

        https://wiki.guildwars2.com/wiki/API:2/characters#Response
        '''
        self.checkPermission('characters')

    @typer
    def getDyes(self):
        '''
        Query the Guild Wars 2 account Dye API and build
        objects based off the JSON.

        https://wiki.guildwars2.com/wiki/API:2/account/dyes#Response
        '''
        self.checkPermission('unlocks')

    @typer
    def getSkins(self):
        '''
        Queries the Guild Wars 2 account Skins API
        and builds an object (or objects) based on the
        returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/account/skins#Response
        '''
        self.checkPermission('unlocks')

    @typer
    def getMinis(self):
        '''
        Queries the Guild Wars 2 account Minis API
        and builds an object (or objects) based on the
        returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/account/minis#Response
        '''
        self.checkPermission('unlocks')

    def getTraits(self, charName, areaFlag=None):
        '''
        Query multiple APIs (account specialization, trait, etc)
        and build the needed objects.

        Reference:
          - https://wiki.guildwars2.com/wiki/API:2/specializations#Response
          - https://wiki.guildwars2.com/wiki/API:2/traits#Response

        Takes an optional parameter 'areaFlag' with the following
        acceptable strings: pvp, pve, wvw

        Returns a list of dictionaries containing the following
        keys:

        line   - (obj) Specialization object for a given line.
        traits - (list) A list of Trait objects of the taken traits.

        Note: this can take ~7 seconds, as it builds a FULL
        set of builds for each game mode.
        '''
        self.checkPermission('builds')

        # PEP8 PLS
        apiStr = 'characters/{}/specializations'.format(charName)
        urlStr = urllib.parse.quote(apiStr)

        # Default case.
        if areaFlag is None:
            # Get the JSON in a very ugly way.
            buildJSON = self.getJson(urlStr)['specializations']

            # This feels dirty.
            build = {}

            # Build our lists to reduce requests.
            for area in buildJSON:
                build[area] = []
                # Specialization strings.
                # We format everything here purely for PEP8.
                specIDs = ','.join(str(x['id']) for x in buildJSON[area])

                specStr = 'specializations?ids={}'.format(specIDs)

                # Specialization JSON
                JSON = self.getJson(specStr)

                # Object list.
                specObjs = []

                # This is ugly, but it cut run time in HALF.
                # Get a thread pool going to speed this object up.
                with cc.ThreadPoolExecutor(max_workers=10) as executor:
                    # PEP8
                    caller = eps.Specialization

                    # Submit our function to the pool.
                    cmd = {executor.submit(caller, x): x for x in JSON}

                    # Append as they complete.
                    for future in cc.as_completed(cmd):
                        try:
                            specObjs.append(future.result())
                        except Exception as e:  # pragma: no cover
                            print('Error: ', e)

                # Trait list. [[id,id,id], [id,id,id], [id,id,id]]
                traitList = [x['traits'] for x in buildJSON[area]]

                # This is really ugly, but it does work.
                for spec in specObjs:
                    # Need an empty traits list per specialization.
                    traits = []
                    for traitID in traitList:
                        for trait in traitID:
                            for obj in spec.majors:
                                if trait == obj.id:
                                    traits.append(obj)

                    # Build the dictionary..
                    build[area].append({'line': spec, 'traits': traits})

            # WHAT DO WE WANT?
            return(build)

        # They asked for soemthing specific
        elif type(areaFlag) is str:
            # Empty build array.
            build = []

            # Get the JSON
            buildJSON = self.getJson(urlStr)['specializations'][areaFlag]

            # String/URL building.
            specIDs = ','.join(str(x['id']) for x in buildJSON)
            specStr = 'specializations?ids={}'.format(specIDs)

            # Getting the JSON
            JSON = self.getJson(specStr)

            # Object List.
            specObjs = []

            # This is ugly, but it cut run time in HALF.
            # Get a thread pool going to speed this object up.
            with cc.ThreadPoolExecutor(max_workers=10) as executor:
                # PEP8 pls
                caller = eps.Specialization
                # Submit our function to the pool.
                cmd = {executor.submit(caller, x): x for x in JSON}

                # Append as they complete.
                for future in cc.as_completed(cmd):
                    try:
                        specObjs.append(future.result())
                    except Exception as e:  # pragma: no cover
                        print('Error: ', e)

            # Trait list.
            traitList = [x['traits'] for x in buildJSON]

            for spec in specObjs:
                # Need an empty traits list per specialization.
                traits = []
                for traitID in traitList:
                    for trait in traitID:
                        for obj in spec.majors:
                            if trait == obj.id:
                                traits.append(obj)

                # Append it to our end List.
                build.append({'line': spec, 'traits': traits})

            # BUILDS
            return(build)

    def getMatchResults(self, matchID):
        '''
        Get the results for a match(s) from the
        Guild Wars 2 API.

        To get all matches, pass "all"

        Returns PVPMatch Object(s).
        '''
        self.checkPermission('pvp')

        if type(matchID) is str:
            # Build the ID string.
            if matchID == 'all':
                gameSTR = 'pvp/games?ids=all'
            else:
                gameSTR = 'pvp/games?ids={}'.format(matchID)

            # Get the JSON
            jsonData = self.getJson(gameSTR)
            obj = namedtuple('PVPMatch', jsonData[0].keys())

            # Make the objects.
            matches = []
            for match in jsonData:
                try:
                    matches.append(obj(**match))
                except TypeError:
                    # Very likely missing or adding new attributes.
                    temp_obj = namedtuple('PVPMatch', match.keys())
                    matches.append(temp_obj(**match))

            return(matches)

        # A list of IDs.
        elif type(matchID) is list:
            # Empty match list for later.
            matches = []

            # Build a list broken into 200.
            # This isn't nesscary as of 09/08/2015
            # Never hurts to be prepared though.
            safeIDs = [matchID[x:x + 200] for x in range(0, len(matchID), 200)]

            for safe in safeIDs:
                # Build the list.
                cleanStr = ','.join(str(x) for x in safe)

                cleanURL = 'pvp/games?ids={}'.format(cleanStr)

                for match in self.getJson(cleanURL):
                    obj = namedtuple('PVPMatch', match.keys())
                    matches.append(obj(**match))

            # Return objects.
            return(matches)

        # Raise an issue. What did you even give us?!
        else:
            raise TypeError('getMatchResults invalid param')

    def getPVPStats(self):
        '''
        Queries the Guild Wars 2 'pvp/stats' API
        and assigns the attributes to the current
        instance.

        It is self explaining. Read it.
        '''
        self.checkPermission('pvp')

        statJSON = self.getJson('pvp/stats')

        # General Rank is top level.
        self.pvp_rank = statJSON['pvp_rank']

        # These are all objects and therefore have to go down
        # a certain amoount of levels.
        self.pvp_wins = statJSON['aggregate']['wins']
        self.pvp_losses = statJSON['aggregate']['losses']
        self.pvp_desertions = statJSON['aggregate']['desertions']
        self.pvp_byes = statJSON['aggregate']['byes']
        self.pvp_forfeits = statJSON['aggregate']['forfeits']

        # Profession specific.
        # Contains a two layered dictionary with
        # same information as  the above.
        self.pvp_professions = statJSON['professions']
        # eg. self.professions['elementalist']['wins']

        # The ladder specific stats.
        # Contains a dictionary of similar stats to the above.
        self.pvp_ranked = statJSON['ladders']['ranked']
        self.pvp_unranked = statJSON['ladders']['unranked']

    def getGuildRanks(self, guildID):
        '''
        Simple method. Returns a list of dictionaries containing
        the ranks and their permissions.

        'id'          - Name of rank.
        'order'       - Position in the list.
        'icon'        - URL to the icon of the rank.
        'permissions' - Rank permissions See below.

        This method only works for guild leaders.
        '''
        url = "guild/{}/ranks".format(guildID)

        return(self.getJson(url))

    def getGuildMembers(self, guildID):
        '''
        Simple method. Returns a list of dictionaries
        containing the member, date they joined, and their rank.

        dict.keys():

        'name' - Member account ID.
        'rank' - Member rank.
        'joined' - Member join date.

        This method only works for guild leaders.
        '''
        url = "guild/{}/members".format(guildID)

        return(self.getJson(url))

import urllib.parse
import concurrent.futures as cc
from GW2API import descriptions as eps
from GW2API.functions import getJson, typer


class GlobalAPI:
    def __init__(self):
        self.url = 'https://api.guildwars2.com/v2/'

    def getJson(self, api):
        '''
        Simple wrapper for less typing.
        '''
        return(getJson(self.url + api, header=None))

    @typer
    def getRaid(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.
        '''
        pass

    @typer
    def getGuild(self, json):
        '''
        Query the non-authed Guild wars 2 API to build
        objects from the returned JSON.
        '''
        pass

    @typer
    def getDungeon(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.
        '''
        pass

    @typer
    def getSkill(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.
        '''
        pass

    @typer
    def getLegend(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.
        '''
        pass

    @typer
    def getFinisher(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        See Finisher class for documentation.
        '''
        pass

    @typer
    def getTitle(self, json):
        '''
        Query the non-authed Guild wars 2 API to build
        objects from the returned JSON.

        See Title class for documentation
        '''
        pass

    @typer
    def getOutfit(self, json):
        '''
        Query the non-authed Guild wars 2 API to build
        objects from the returned JSON.

        See Outfit class for documentation
        '''
        pass

    @typer
    def getMasteries(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        See Mastery class for documentation
        '''
        pass

    @typer
    def getPet(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        See Pet class for documentation
        '''
        pass

    @typer
    def getRace(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        See Race class for documentation
        '''
        pass

    @typer
    def getProfession(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects based off the Returned JSON.

        See Profession class for documentation
        '''
        pass

    @typer
    def getGuildUpgrade(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects off the returned JSON.

        See GuildUpgrade class for documentation

        Returns GuildUpgrade(s) objects.
        '''
        pass

    @typer
    def getGuildPermission(self, json):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects off the returned JSON.

        See GuildPermission class for documentation

        Returns GuildPermission(s) objects.
        '''
        pass

    @typer
    def getAchievement(self, json):
        '''
        Query the non-authed Guild Wars 2 achievement
        API and build Achievement(s) objects based off
        the returned json.

        See Achievement class for documentation

        Returns Achievement(s) objects.
        '''
        pass

    @typer
    def getAchievementGroup(self, json):
        '''
        Query the non-authed Guild Wars 2 achievement
        groups API and build objects based off the return JSON.

        See AchievementGroup class for documentation.

        Returns AchievementGroup(s) objects.
        '''
        pass

    @typer
    def getAchievementCategory(self, json):
        '''
        Query the non-authed Guild Wars 2 achievement/categories
        API and build objects from the JSON.

        See AchievementCategory class for more documentation.

        Returns AchievementCategory(s) objects.
        '''
        pass

    @typer
    def getSkin(self, json):
        '''
        Query the non-authed skin Guild Wars 2 Skin API
        and build Skin object(s) based on it.

        See the Skin class for documentation.

        Returns Skin object(s).
        '''
        pass

    @typer
    def getItem(self, json):
        '''
        Query the Guild Wars 2 item API and build
        object(s) based off the returned JSON.

        See Item class for more documentation.

        Returns Item object(s).
        '''
        pass

    @typer
    def getDye(self, json):
        '''
        Query the Guild Wars 2 Dye API and build
        object(s) based off the returned JSON.

        See Dye class for more documentation.

        Returns Dye object(s).
        '''
        pass

    @typer
    def getRecipe(self, json):
        '''
        Query the Guild Wars 2 Recipe API and build
        object(s) based off the returned JSON.

        See Recipe class for more documentation.

        Returns Recipe object(s).
        '''
        pass

    @typer
    def getMini(self, json):
        '''
        Query the Guild Wars 2 Mini API and build
        object(s) based off the returned JSON.

        See Mini class for more documentation.

        Returns Mini object(s).
        '''
        pass

    def getWVWObjective(self, wvwID, objects=None):
        '''
        Query the Guild Wars 2 wvw/objectives API and build
        object(s) based off the returned JSON.

        Accepts lists, strings, and WVWMaps.

        See WVWObjective class for more documentation.

        Returns WVWObjective object(s).
        '''
        if type(wvwID) is list:
            if objects is None:
                objects = []

            # Build clean string to append to URL.
            cleanList = ','.join(str(x) for x in wvwID)

            # Build the URL.
            cleanURL = 'wvw/objectives?ids={}'.format(cleanList)

            data = self.getJson(cleanURL)

            # Generate the objects.
            for name in data:
                objects.append(eps.WVWObjective(name))

            # Return said objects.
            return(objects)

        elif type(wvwID) is str:
            if wvwID == 'all':
                if objects is None:
                    objects = []

                # Default case: get all of them.
                wvwJSON = self.getJson('wvw/objectives?ids=all')

                # Generate objects.
                for item in wvwJSON:
                    objects.append(eps.WVWObjective(item))

                # Return them all.
                return(objects)

            else:
                jsonData = self.getJson('wvw/objectives/{}'.format(wvwID))

                # Return the Object.
                return(eps.WVWObjective(jsonData))

        # I hate this.
        elif type(wvwID) is eps.WVWMap:
            if objects is None:
                objects = []

            # We will have to do a couple requests.
            idList = [x['id'] for x in wvwID.objectives]

            # Build the URL string.
            cleanList = ','.join(idList)

            # Get the JSON.
            wvwJSON = self.getJson('wvw/objectives?ids={}'.format(cleanList))

            for item in wvwJSON:
                for current in wvwID.objectives:
                    if item['id'] == current['id']:
                        # Make the object.
                        new = eps.WVWObjective(item)

                        # Assign the WVWMap specfic values.
                        new.owner        = current['owner']
                        new.last_flipped = current['last_flipped']
                        new.claimed_at   = current['claimed_at']
                        new.claimed_by   = current['claimed_by']

                        # Append to our object list.
                        objects.append(new)

            # Return our "modified" WVWObjectives
            return(objects)

    def getWVWMatches(self, matchID, objects=None):
        '''
        Build and return WVWMatch objects for all
        currently in progress WVW Matches.

        See WVWMatch documentation.
        '''
        if type(matchID) is list:
            if objects is None:
                objects = []

            # Build clean string to append to URL.
            cleanList = ','.join(str(x) for x in matchID)

            # Build the URL.
            cleanURL = 'wvw/matches?ids={}'.format(cleanList)

            data = self.getJson(cleanURL)

            # Generate the objects.
            for name in data:
                objects.append(eps.WVWMatch(name))

            # Return said objects.
            return(objects)

        elif type(matchID) is str:
            if matchID == 'all':
                if objects is None:
                    objects = []

                # Default case: get all of them.
                wvwJSON = self.getJson('wvw/matches?ids=all')

                # Generate objects.
                for item in wvwJSON:
                    objects.append(eps.WVWMatch(item))

                # Return them all.
                return(objects)

            else:
                jsonData = self.getJson('wvw/matches/{}'.format(matchID))

                # Return the Object.
                return(eps.WVWMatch(jsonData))

    def getDailies(self, tomorrow=False):
        '''
        Simple method to grab the dailies from GW2 official
        API and returns achievement objects for them.
        '''
        # Temporary list to reduce requests.
        idList = []

        # The data.
        if tomorrow:
            jsonData = self.getJson('achievements/daily/tomorrow')
        else:
            jsonData = self.getJson('achievements/daily')

        # Get the achievements for each area.
        for key in jsonData.keys():
            for achievement in jsonData[key]:
                idList.append(achievement['id'])

        return(self.getAchievement(idList))


class AccountAPI:
    def __init__(self, api_key):
        '''
        Initalize various bits of account information.
        '''
        self.api_key = api_key
        self.header  = {'Authorization': 'Bearer ' + self.api_key}
        self.url     = 'https://api.guildwars2.com/v2/'

        data = self.getJson('tokeninfo')
        self.permissions = data['permissions']

        data = self.getJson('account/')

        self.accountID = data['id']
        self.username  = data['name']
        self.world     = data['world']
        self.guilds    = data['guilds']

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

        guild = eps.Guild(self.getJson('guild/{}'.format(guildID)))
        return guild

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

        pass

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

        pass

    @typer
    def getMaterials(self):
        '''
        Gets your materials raw JSON via the Guild Wars 2 official
        API and stores it in the object.

        Also returns this information, to immediately use in thing
        such as a for loop.

        Use the rest of the API to get more detailed information.

        Returns a list of dictionaries which have keys:

        id       - (int) The item ID of the material.
        category - (int) The material category the item belongs to.
        count    - (int) The amount of material in storage.
        object   - (Item) The object representing what's in slot.

        '''
        self.checkPermission('inventories')

        pass

    @typer
    def getOutfits(self):
        '''
        Get your unlocked outfits from the Guild Wars 2 official
        outfit API.

        Returns a list of Outfit objects (see descriptions)
        '''
        self.checkPermission('unlocks')
        pass

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
        pass

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
        pass

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
        buyingData  = self.getJson(currentURL + '/buys')
        sellingData = self.getJson(currentURL + '/sells')

        # If there is no buying data, set it to None.
        # You know, like API should have.
        if len(buyingData) > 0:
            self.buying = buyingData
        else:
            self.buying = None

        # Same here.
        if len(sellingData) > 0:
            self.selling = sellingData
        else:
            self.selling = None

        # Get our transaction HISTORY. Only completed trades.
        # PEP8...please.
        historyURL = 'commerce/transactions/history/'
        boughtData = self.getJson(historyURL + 'buys')
        soldData   = self.getJson(historyURL + 'sells')

        # As before, sanitize this.
        if len(boughtData) > 0:
            self.bought = boughtData
        else:
            self.bought = None

        # And this.
        if len(soldData) > 0:
            self.sold = soldData
        else:
            self.sold = None

        # Return the information...for use immediately?
        return({'sold': self.sold, 'bought': self.bought,
                'selling': self.selling, 'buying': self.buying})

    @typer
    def getCharacters(self):
        '''
        Uses the Guild Wars 2 API to query for a given
        character name on your account, and passes the
        information to the 'Character()' object.

        See the Character class for documentation.
        '''
        self.checkPermission('characters')

        pass

    @typer
    def getDyes(self):
        '''
        Query the Guild Wars 2 account Dye api and build
        'Dye()' objects based off the JSON.

        See the Dye class for its documentation.

        NOTE: This can be slightly memory intensive. It IS every
        Dye you have unlocked after all.
        '''
        self.checkPermission('unlocks')

        pass

    @typer
    def getSkins(self):
        '''
        Queries the Guild Wars 2 account Skins API
        and builds an object (or objects) based on the
        returned JSON.

        See the Skin class for its documentation.

        NOTE: This can be slightly memory intensive. It IS every
        skin you have unlocked after all.
        '''
        self.checkPermission('unlocks')

        pass

    @typer
    def getMinis(self):
        '''
        Queries the Guild Wars 2 account Minis API
        and builds an object (or objects) based on the
        returned JSON.

        See the Mini class for its documentation.

        NOTE: This can be slightly memory intensive. It IS every
        mini you have unlocked after all.
        '''
        self.checkPermission('unlocks')

    def getTraits(self, charName, areaFlag=None):
        '''
        Query multiple APIs (account specialization, trait, etc)
        and build the needed objects.

        See the Specialization and Trait classes for documentation.

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
                try:
                    specIDs = ','.join(str(x['id']) for x in buildJSON[area])
                except TypeError:
                    continue

                specStr = 'specializations?ids={}'.format(specIDs)

                # Specialization JSON
                JSON = self.getJson(specStr)

                # Object list.
                specObjs = []

                # This is ugly, but it cut run time in HALF.
                # Get a thread pool going to speed this object up.
                with cc.ThreadPoolExecutor(max_workers = 10) as executor:
                    # PEP8
                    caller = eps.Specialization

                    # Submit our function to the pool.
                    cmd = {executor.submit(caller, x): x for x in JSON}

                    # Append as they complete.
                    for future in cc.as_completed(cmd):
                        try:
                            specObjs.append(future.result())
                        except Exception as e:
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
            with cc.ThreadPoolExecutor(max_workers = 10) as executor:
                # PEP8 pls
                caller = eps.Specialization
                # Submit our function to the pool.
                cmd = {executor.submit(caller, x): x for x in JSON}

                # Append as they complete.
                for future in cc.as_completed(cmd):
                    try:
                        specObjs.append(future.result())
                    except Exception as e:
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
            if matchID == 'all':
                # Build the ID string.
                gameSTR = 'pvp/games?ids=all'

                # Make the objects.
                matches = [eps.PVPMatch(x) for x in self.getJson(gameSTR)]

                return(matches)
            else:
                # Build the URL
                gameSTR = 'pvp/games?id={}'.format(matchID)

                # Use the url.
                match = eps.PVPMatch(self.getJson(gameSTR))

                return(match)

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
                    matches.append(eps.PVPMatch(match))

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
        self.pvp_wins       = statJSON['aggregate']['wins']
        self.pvp_losses     = statJSON['aggregate']['losses']
        self.pvp_desertions = statJSON['aggregate']['desertions']
        self.pvp_byes       = statJSON['aggregate']['byes']
        self.pvp_forfeits   = statJSON['aggregate']['forfeits']

        # Profession specific.
        # Contains a two layered dictionary with
        # same information as  the above.
        self.pvp_professions = statJSON['professions']
        # eg. self.professions['elementalist']['wins']

        # The ladder specific stats.
        # Contains a dictionary of similar stats to the above.
        self.pvp_ranked   = statJSON['ladders']['ranked']
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

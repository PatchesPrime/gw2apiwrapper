import urllib.parse
import urllib.request
import json
import concurrent.futures as cc

class PermissionError(Exception):
    pass

class FlagParameterError(Exception):
    pass

class BadIDError(Exception):
    pass

# Seperate functions from classes via file?
def getJson(url, header = None):
    '''
    Got tired of writing this over and over.
    What functions are for, right?
    '''
    try:
        if header is not None:
            request = urllib.request.Request(url, None, header)
            with urllib.request.urlopen(request) as response:
                jsonData = json.loads(response.read().decode('UTF-8'))
                return(jsonData)
        else:
            # This one doesn't need a header.
            with urllib.request.urlopen(url) as response:
                return(json.loads(response.read().decode('UTF-8')))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # 404 NOT FOUND is useful, but it helps to point them
            # in the right direction.
            error = 'HTTPError! Likely bad ID: {} {}'.format(e.code, e.msg)

            # Dangerous magic!
            raise BadIDError(error) from None

        elif e.code == 403:
            # 403: Forbidden is invalid authentication.
            error = 'HTTPError! Likely bad APIKEY: {} {}'.format(e.code, e.msg)

            # MORE DANGEROUS MAGIC
            raise PermissionError(error) from None

        else:
            raise(e)

def getBuild():
    '''
    Get the current build ID for Guild Wars 2.

    Returns an integer.
    '''
    return(getJson('https://api.guildwars2.com/v2/build')['id'])

def getAssets():
    '''
    Get commonly requested files from Guild Wars 2
    offical API. Waypoint icons and the like.

    Returns a list of dictionaries containing the keys:

    id   - (int) The ID of asset.
    icon - (str) URL off the asset.
    '''
    return(getJson('https://api.guildwars2.com/v2/files?ids=all'))

def isMaterial(itemID):
    '''
    Takes an item ID (int or list), and checks the materials
    sections of the Guild Wars 2 bank via API.

    If given an INT, it will return one of two values:

    False - ID is not a material.
    True  - ID is material. String is category.

    If given a LIST, it will return one of two values:

    None - No items in LIST are materials.
    SET  - A set containing the IDs that matched a material.

    eg.
        if 129721 in isMaterial([19721, 224295]):
            print('True, 112971 is a material')

    '''
    # Get initial URL and request it.
    matURL = 'https://api.guildwars2.com/v2/materials?ids=all'
    matCategories = getJson(matURL)

    if type(itemID) is int:
        # Use the information.
        for category in matCategories:
            if itemID in category['items']:
                return(True)

        # Return a negative result as the default.
        return(False)

    if type(itemID) is list:
        # We'll need a temporary list if we don't
        # want one of the world ugliest list comprehension.
        matIDs = []

        # Add the IDs to the list.
        for category in matCategories:
            matIDs.extend(category['items'])


        # Return the IDs that ARE materials.
        return(set(matIDs).intersection(itemID))



def recipeSearch(in_or_out, itemID):
    '''
    Search using the 'recipe/search' API for the given
    ID. Depending on your parameters, it will either
    return the recipes that produce (output) or take
    (input) the item ID.

    Returns a list containing the revelent IDs.
    '''
    # I just want it on record that I don't like this method.
    # It's ugly and it stinks....PEP8 doe..

    # URL Building. Ugly URL Building.
    urls = {'input': 'https://api.guildwars2.com/v2/recipes/search?input=',
            'output': 'https://api.guildwars2.com/v2/recipes/search?output='}

    # Should be good enough to verify it's one of the inputs
    # We want.
    if in_or_out not in urls.keys():
        raise FlagParameterError('First argument must be 'input' or 'output'')

    # Lets build the URL here. You know, for PEP8s sake.
    cleanURL = urls[in_or_out] + '{}'.format(itemID)

    # Return raw JSON. It will always be a list.
    # Right ANET?
    return(getJson(cleanURL))

def getWorldName(worldID):
    '''
    Ugly function to return the ID and Name of
    the given world ID.

    The API for this is so simple, I didn't feel the need
    to make it any more complicated than this.

    Returns a list of dictionaries. Each dictionary
    has the following keys:

    id         - (int) The numerical ID
    name       - (str) Name of the server.
    population - (str) The population size of the server.
    '''
    # Base URL.
    url = 'https://api.guildwars2.com/v2/worlds?ids='

    # Do some handling here.
    if type(worldID) is list:
        # If it's a list, we want to format it
        # the way the API expects it.
        cleanList = ','.join(str(x) for x in worldID)

        # Actually create the URL
        cleanURL = url + cleanList
    else:
        # Default case is just one ID.
        cleanURL = url + '{}'.format(worldID)

    # Return them. Raw JSON but...oh well?
    return(getJson(cleanURL))

class AccountAPI:
    def __init__(self, api_key):
        '''
        Initalize various bits of account information.
        '''
        self.api_key = api_key
        self.header  = { 'Authorization: ' : 'Bearer ' + self.api_key }
        self.url     = 'https://api.guildwars2.com/v2/'

        data = getJson(self.url + 'tokeninfo', self.header)
        self.permissions = data['permissions']

        accountURL = self.url + 'account/'
        data = getJson(accountURL, self.header)

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
            raise PermissionError('PermissionError: {:s}'.format(apiName))

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
        currencyJSON = getJson(self.url + 'currencies?ids=all')

        # Does require authentication.
        walletJSON = self.getJson('account/wallet')

        for currency in currencyJSON:
            for item in walletJSON:
                if currency['id'] == item['id']:
                    currency.update({'count': item['value']})

        # Set the objects 'wallet' attribute.
        self.wallet = currencyJSON

        return(self.wallet)

    def getBank(self):
        '''
        Gets your banks raw JSON via the Guild Wars 2 official
        API and stores it in the object.

        Also returns this information, to immediately use in thing
        such as a for loop.

        Use the rest of the API to get more detailed information.

        Returns a list of dictionaries which have keys:

        id        - (int) The item's ID.
        count     - (int) The amount of items in the item stack.
        skin      - (int, optional) If not default skin, its ID.
        upgrades  - (list, optional) IDs for each rune/signet on the item.
        infusions - (list, optional) IDs for each infusion on the item.
        '''
        self.checkPermission('inventories')

        # Build the URL.
        bankURL = self.url + 'account/bank'

        # Store it in the object.
        self.bank = getJson(bankURL, self.header)

        # Return a list of dictionaries.
        return(self.bank)

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
        '''
        self.checkPermission('inventories')

        # Build the URL.
        matURL = self.url + 'account/materials'

        # Store it in the object.
        self.materials = getJson(matURL, self.header)

        # Return a list of dictionaries.
        return(self.materials)

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
        tradeURL = self.url + 'commerce/transactions/'

        # Grab the buying and selling information.
        currentURL  = tradeURL + 'current/'
        buyingData  = getJson(currentURL + 'buys', self.header)
        sellingData = getJson(currentURL + 'sells', self.header)

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
        historyURL = tradeURL + 'history/'
        boughtData = getJson(historyURL + 'buys', self.header)
        soldData   = getJson(historyURL + 'sells', self.header)


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
        return({ 'sold': self.sold, 'bought': self.bought,
                 'selling': self.selling, 'buying': self.buying})

    def getCharacterList(self):
        '''
        Instead of having two types of Character instance, just have a method
        to return a list of characters.

        Returns a list of of your character names.
        '''
        self.checkPermission('characters')

        return self.getJson('characters/')

    # Starting here, things get repetative. Still, not bad.
    # Just going to have to clean it up at some point.
    def getCharacter(self, name, objects = None):
        '''
        Uses the Guild Wars 2 API to query for a given
        character name on your account, and passes the
        information to the 'Character()' object.

        See the Character class for documentation.
        '''
        self.checkPermission('characters')

        # Removes the need for a factory by type checking.
        if type(name) is list:
            # Serves a dual purpose. We get a list to append
            # and they have the option of using their own.
            if objects is None:
                objects = []

            # Build clean string to append to URL.
            cleanStr = ','.join(str(x) for x in name)

            # Build the URL.
            cleanURL = urllib.parse.quote('characters?ids={}'.format(cleanStr))

            data = self.getJson(cleanURL)

            # Generate the objects.
            for player in data:
                objects.append(Character(player))

            # Return said objects.
            return(objects)
        elif type(name) is str:
            # Get the data.
            jsonData = self.getJson('characters/' + urllib.parse.quote(name))

            # Return the object that used the data.
            return Character(jsonData)
        else:
            raise TypeError('getCharacter() requires list or str')

    def getDyes(self):
        '''
        Query the Guild Wars 2 account Dye api and build
        'Dye()' objects based off the JSON.

        See the Dye class for its documentation.

        NOTE: This can be slightly memory intensive. It IS every
        Dye you have unlocked after all.
        '''
        self.checkPermission('unlocks')

        # Only exists if it's asked for.
        self.dyes = []

        # Get all of the IDs we're going to need.
        dyeIDs = self.getJson('account/dyes')

        # I am both proud of an ashamed of this line.
        # I split the dyeIDs into 200 element chunks.
        # The API only supports 200 IDs at once.
        # Personally I blame terrorism.
        safeList = [dyeIDs[x:x + 200] for x in range(0, len(dyeIDs), 200)]

        # The construction of the dye attribute.
        for safe in safeList:
            # Clean them up into a proper string.
            cleanStr = ','.join(str(x) for x in safe)

            # Build a pretty URL.
            cleanURL = self.url + 'colors?ids={}'.format(cleanStr)

            # Lets build some objects!
            for dye in getJson(cleanURL):
                self.dyes.append(Dye(dye))

        # Return finished Dye List.
        return(self.dyes)

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

        # Only exists if it's asked for.
        self.skins = []

        # Get all of the IDs we're going to need.
        skinIDs = self.getJson('account/skins')

        # I am both proud of an ashamed of this line.
        # I split the skinIDs into 200 element chunks.
        # The API only supports 200 IDs at once.
        # Personally I blame terrorism.
        safeList = [skinIDs[x:x + 200] for x in range(0, len(skinIDs), 200)]

        # The construction of the skin attribute.
        for safe in safeList:
            # Clean them up into a proper string.
            cleanStr = ','.join(str(x) for x in safe)

            # Build a pretty URL.
            cleanURL = self.url + 'skins?ids={}'.format(cleanStr)

            # Lets build some objects!
            for skin in getJson(cleanURL):
                self.skins.append(Skin(skin))

        # Return it for immediate use as interator.
        # If that's what gets you hard.
        return(self.skins)

    def getTraits(self, charName, areaFlag = None):
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
                specIDs = ','.join(str(x['id']) for x in buildJSON[area])
                specStr = 'specializations?ids={}'.format(specIDs)

                # Specialization JSON
                JSON = self.getJson(specStr)

                # Object list.
                specObjs = []

                # This is ugly, but it cut run time in HALF.
                # Get a thread pool going to speed this object up.
                with cc.ThreadPoolExecutor(max_workers = 10) as executor:
                    # Submit our function to the pool.
                    cmd = {executor.submit(Specialization, x): x for x in JSON}

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
                    build[area].append({ 'line': spec, 'traits': traits})

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
                # Submit our function to the pool.
                cmd = {executor.submit(Specialization, x): x for x in JSON}

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
                build.append({ 'line': spec, 'traits': traits })

            # BUILDS
            return(build)


    def getMatchResults(self, matchID = None):
        '''
        Get the results for a match(s) from the
        Guild Wars 2 API.

        If no ID is supplied, it fetches all games it can.

        Returns PVPMatch Object(s).
        '''
        self.checkPermission('pvp')

        # Default case.
        if matchID is None:
            # Get all the game IDs.
            gameIDs = self.getJson('pvp/games')

            # Build the ID string.
            gameSTR = 'pvp/games?ids={}'.format(','.join(gameIDs))

            # Make the objects.
            matches = [PVPMatch(x) for x in self.getJson(gameSTR)]

            return(matches)

        # Only one ID
        elif type(matchID) is str:
            # Build the URL
            gameSTR = 'pvp/games?id={}'.format(matchID)

            # Use the url.
            match = PVPMatch(self.getJson(gameSTR))

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
                    matches.append(PVPMatch(match))

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

class GlobalAPI:
    def __init__(self):
        self.url     = 'https://api.guildwars2.com/v2/'

    def getJson(self, api):
        '''
        Simple wrapper for less typing.
        '''
        return(getJson(self.url + api, header=None))

    def getSkin(self, skinID, objects = None):
        '''
        Query the non-authed skin Guild Wars 2 Skin API
        and build Skin object(s) based on it.

        See the Skin class for documentation.

        Returns Skin object(s).
        '''
        # Remove the need for a factory.
        if type(skinID) is list:
            if objects is None:
                objects = []

            # Build clean string to append to URL.
            cleanList = ','.join(str(x) for x in skinID)

            # Build the URL.
            cleanURL = urllib.parse.quote('skins?ids={}'.format(cleanList))

            data = self.getJson(cleanURL)

            # Generate the objects.
            for name in data:
                objects.append(Skin(name))

            # Return said objects.
            return(objects)

        elif type(skinID) is int:
            jsonData = self.getJson('skins/{}'.format(skinID))

            # Return the objecct.
            return(Skin(jsonData))
        else:
            raise TypeError('getSkin() requires a str or list.')

    def getItem(self, itemID, objects = None):
        '''
        Query the Guild Wars 2 item API and build
        object(s) based off the returned JSON.

        See Item class for more documentation.

        Returns Item object(s).
        '''
        if type(itemID) is list:
            if objects is None:
                objects = []

            # Build clean string to append to URL.
                cleanList = ','.join(str(x) for x in itemID)

            # Build the URL.
            cleanURL = 'items?ids={}'.format(cleanList)

            data = self.getJson(cleanURL)

            # Generate the objects.
            for name in data:
                objects.append(Item(name))

            # Return said objects.
            return(objects)

        elif type(itemID) is int:
            jsonData = self.getJson('items/{}'.format(itemID))

            # Return the Object.
            return(Item(jsonData))

    def getDye(self, dyeID, objects = None):
        '''
        Query the Guild Wars 2 Dye API and build
        object(s) based off the returned JSON.

        See Dye class for more documentation.

        Returns Dye object(s).
        '''
        if type(dyeID) is list:
            if objects is None:
                objects = []

            # Build clean string to append to URL.
            cleanList = ','.join(str(x) for x in dyeID)

            # Build the URL.
            cleanURL = urllib.parse.quote('dyes?ids={}'.format(cleanList))

            data = self.getJson(cleanURL)

            # Generate the objects.
            for name in data:
                objects.append(Dye(name))

            # Return said objects.
            return(objects)

        elif type(dyeID) is int:
            jsonData = self.getJson('dyes/{}'.format(dyeID))

            # Return the Object.
            return(Dye(jsonData))

    def getRecipe(self, recipeID, objects = None):
        '''
        Query the Guild Wars 2 Recipe API and build
        object(s) based off the returned JSON.

        See Recipe class for more documentation.

        Returns Recipe object(s).
        '''
        if type(recipeID) is list:
            if objects is None:
                objects = []

            # Build clean string to append to URL.
            cleanList = ','.join(str(x) for x in recipeID)

            # Build the URL.
            cleanURL = urllib.parse.quote('recipes?ids={}'.format(cleanList))

            data = self.getJson(cleanURL)

            # Generate the objects.
            for name in data:
                objects.append(Recipe(name))

            # Return said objects.
            return(objects)

        elif type(recipeID) is int:
            jsonData = self.getJson('recipes/{}'.format(recipeID))

            # Return the Object.
            return(Recipe(jsonData))


# I don't actually like this object.
# It seems so simple that it doesn't need to be
# an object, but rather could do with being loose
# functions. Anyone got suggestions? :<
class GW2TP:
    def __init__(self):
        '''
        Initialize various bits of information.
        As in one bit. The 'basic' URL for all commerce API.
        '''
        # Everything here will need access to this URL.
        # So lets put it in the __init__
        self.url = 'https://api.guildwars2.com/v2/commerce/'

    def getJson(self, api):
        '''
        Simple wrapper for less typing.
        '''
        return(getJson(self.url + api, header=None))

    def getListings(self, itemID):
        '''
        Returns the Guild Wars 2 trading post listings
        for given item ID(s).

        Returns a dictionary if only one ID is given.
        Returns a list of dictionaries if a list of IDs is given.
        '''
        # Removed the need for factory.
        if type(itemID) is list:
            cleanList = ','.join(str(x) for x in itemID)
            cleanURL = 'listings?ids={}'.format(cleanList)
        else:
            cleanURL = 'listings/{}'.format(itemID)

        # Feels dirty, but simple json is often
        # most effective as simple data structure.
        return(self.getJson(cleanURL))

    def getPrices(self, itemID):
        '''
        Returns the Guild Wars 2 trading post prices
        for given item ID(s).

        Returns a dictionary if only one ID is given.
        Returns a list of dictionaries if a list of IDs is given.
        '''
        # Removed the need for factory.
        if type(itemID) is list:
            cleanList = ','.join(str(x) for x in itemID)
            cleanURL = 'prices?ids={}'.format(cleanList)
        else:
            cleanURL = 'prices/{}'.format(itemID)

        # Feels dirty, but simple json is often
        # most effective as simple data structure.
        return(self.getJson(cleanURL))

    def getExchange(self, coin_or_gems, quantity):
        '''
        Returns a dictionary of the current exchange rate
        of either coins->gems or gems->coins based off the
        first parameter.

        coin_or_gems accepts the following strings:

        coin - Returns the 'coin to gems' ratio.
        gems - Returns the 'gem to coins' ratio.
        '''
        # Dictionary to hold URLs for the API. Which we use will depend on
        # gold_or_gems
        urls = { 'coin': self.url + 'exchange/coins?quantity=',
                 'gems': self.url + 'exchange/gems?quantity=' }

        # Check if they gave proper input.
        if coin_or_gems in urls.keys():
            # Build a URL.
            cleanURL = urls[coin_or_gems] + '{}'.format(quantity)

            # Use said URL.
            jsonData = self.getJson(cleanURL)

            # Returns a dictionary.
            return(jsonData)
        else:
            # Tell them what they did wrong.
            raise FlagParameterError('First arg must be 'coins' or 'gems'')

class Map:
    '''
    Builds an object that represents the Guild Wars 2
    world map based off the Guild Wars 2 Official API.

    This is a stand-alone object. It has the potential to
    be beefy enough on its own.

    This object handles its own fetching of JSON, and therefore
    requires a map ID in order to function rather than the
    maps JSON.

    '''
    def __init__(self, mapID):
        # Build the basic Map object.
        self.url = 'https://api.guildwars2.com/v2/maps/'
        mapJSON = getJson(self.url + '{}'.format(mapID))


        self.id             = mapJSON['id']
        self.name           = mapJSON['name']
        self.min_level      = mapJSON['min_level']
        self.max_level      = mapJSON['max_level']
        self.default_floor  = mapJSON['default_floor']
        self.floors         = mapJSON['floors']
        self.region_id      = mapJSON['region_id']
        self.region_name    = mapJSON['region_name']
        self.continent_id   = mapJSON['continent_id']
        self.continent_name = mapJSON['continent_name']
        self.map_rect       = mapJSON['map_rect']
        self.continent_rect = mapJSON['continent_rect']

    # This method is pure evil.
    # It deals with the bloated 'continents' API.
    # I can't think of a better way to deal with the
    # 7 layers of nesting ANET decided to use.
    def getDetails(self):
        '''
        getDetails() pulls all the available information on the current
        maps waypoints, pois, vistas, skill points, and hearts from the
        official Guild Wars 2 continent API.

        It's not the cleanest of methods, but you should see what I'm
        working with.
        '''
        # Build the string.
        url = 'https://api.guildwars2.com/v2/continents/1/floors/1/'
        cleanURL = url + 'regions/{}/maps/{}'.format(self.region_id, self.id)

        # Load up the JSON to be used later.
        JSON = getJson(cleanURL)

        # We'll need this.
        self.waypoints   = []
        self.pois        = []
        self.vistas      = []
        self.skillPoints = []
        self.hearts      = []

        # Grab all the 'pois', which include waypoints, poi, and vistas.
        poiInfo = JSON['points_of_interest']

        for current in poiInfo:
            if poiInfo[current]['type'] == 'waypoint':
                self.waypoints.append(poiInfo[current])
            elif poiInfo[current]['type'] == 'landmark':
                self.pois.append(poiInfo[current])
            elif poiInfo[current]['type'] == 'vista':
                self.vistas.append(poiInfo[current])

        # Grab all the Skill Points.
        self.skillPoints = JSON['skill_challenges']

        # Grab all the Hearts (tasks)
        tasksInfo = JSON['tasks']

        for current in tasksInfo:
            self.hearts.append(tasksInfo[current])

class Character:
    '''
    Character objects take a JSON lump of character data and
    convert it to a python object.

    This eliminates the need to pass the API key here.
    It does not inherit the GW2Armory class because we want
    to use an active instance of GW2Armory, not an empty version
    or template.

    Usage:
        # Return object of a character...
        EngiPatches = Character(jsonData)
    '''
    def __init__(self, playerJSON):
        # Assign ALL THE THINGS
        self.name       = playerJSON['name']
        self.race       = playerJSON['race']
        self.gender     = playerJSON['gender']
        self.profession = playerJSON['profession']
        self.level      = playerJSON['level']

        # Replace this with self.getGuild()
        self.guildID = playerJSON['guild']

        # Returning to our scheduled broadcast.
        self.creation = playerJSON['created']
        self.age      = playerJSON['age']
        self.deaths   = playerJSON['deaths']
        self.gear     = playerJSON['equipment']
        self.bags     = playerJSON['bags']

class Item:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official item API.

    '''
    # NOTE: snarky comments aside, the webdev of anet said this
    # paticular API is the bane of his existence. I am not alone.
    def __init__(self, itemJSON):
        # Build the items attributes into the object.
        self.id   = itemJSON['id']
        self.name = itemJSON['name']
        self.icon = itemJSON['icon']
        self.type = itemJSON['type']

        # Here we go. Optional arguments that are not
        # defined or empty if not in use. This is bad
        # practice on ANETs part.
        try:
            self.description = itemJSON['description']
        except KeyError:
            self.description = None

        self.rarity = itemJSON['rarity']
        self.level  = itemJSON['level']
        self.vendor = itemJSON['vendor_value']
        # Another optional that causes errors due to no
        # default empty value..
        try:
            self.baseskin = itemJSON['default_skin']
        except KeyError:
            self.baseskin = None

        self.flags        = itemJSON['flags']
        self.valid_modes  = itemJSON['game_types']
        self.restrictions = itemJSON['restrictions']


        # NOTE: This is dependant on the item type, so we have to check that.
        # This whole section is just to tear the JSON down into python object
        # attributes.
        if self.type == 'Armor':
            self.slot          = itemJSON['details']['type']
            self.weight        = itemJSON['details']['weight_class']
            self.defense       = itemJSON['details']['defense']
            self.infusions     = itemJSON['details']['infusion_slots']

            try:
                self.infix_upgrade = itemJSON['details']['infix_upgrade']
            except KeyError:
                self.infix_upgrade = None

            # Some times items don't have runes/sigils.
            # This handles that occasion by changing it to 'None'
            # and suppressing the KeyError
            try:
                self.rune = itemJSON['details']['suffix_item_id']
            except KeyError:
                self.rune = None

            # Seriously: what?
            self.what     = itemJSON['details']['secondary_suffix_item_id']

        if self.type == 'Back':
            self.infusions = itemJSON['details']['infusion_slots']

            # Oh look another thing that ANET didn't handle consistently.
            # If the item doesn't have it, return None or empty.
            # You know, so I don't have to...
            try:
                self.infix_upgrade = itemJSON['details']['infix_upgrade']
            except KeyError:
                self.infix_upgrade = None

            # Oh look, more nonsense because we don't properly
            # handle absent attributes anet...
            try:
                self.jewel = itemJSON['details']['suffix_item_id']
            except KeyError:
                self.jewel = None

            self.what = itemJSON['details']['secondary_suffix_item_id']

        if self.type == 'Bag':
            self.size = itemJSON['details']['size']
            self.safe = itemJSON['details']['no_sell_or_sort']

        if self.type == 'Consumable':
            self.consumable = itemJSON['details']['type']

            try:
                self.effect = itemJSON['details']['description']
            except KeyError:
                self.effect = None

            try:
                self.duration = itemJSON['details']['duration_ms']
            except KeyError:
                self.duration = None

            # NOTE: We could change all try/excepts into one
            # with a for loop.

            # Inconsistency is the devil.
            try:
                self.unlock_type = itemJSON['details']['unlock_type']
            except KeyError:
                self.unlock_type = None

            # Inconsistency is the devil.
            try:
                self.color_id = itemJSON['details']['color_id']
            except KeyError:
                self.color_id = None

            # Inconsistency is the devil.
            try:
                self.recipe_id = itemJSON['details']['recipe_id']
            except:
                self.recipe_id = None

        if self.type == 'Container':
            self.container = itemJSON['details']['type']

        if self.type == 'Gathering':
            self.tool = itemJSON['details']['type']

        if self.type == 'Gizmo':
            self.gizmo = itemJSON['details']['type']

        if self.type == 'Tool':
            self.salvage_kit = itemJSON['details']['type']
            self.charges     = itemJSON['details']['charges']

        if self.type == 'Trinket':
            self.trinket       = itemJSON['details']['type']
            self.infusions     = itemJSON['details']['infusion_slots']

            try:
                self.infix_upgrade = itemJSON['details']['infix_upgrade']
            except KeyError:
                self.infix_upgrade = None


            # Optional attribute with no default value if empty.
            # Again.
            try:
                self.jewel = itemJSON['details']['suffix_item_id']
            except KeyError:
                self.jewel = None

            self.what = itemJSON['details']['secondary_suffix_item_id']

        if self.type == 'UpgradeComponent':
            self.upgrade       = itemJSON['details']['type']
            self.socketable    = itemJSON['details']['flags']
            self.infusion      = itemJSON['details']['infusion_upgrade_flags']
            self.suffix        = itemJSON['details']['suffix']

            try:
                self.infix_upgrade = itemJSON['details']['infix_upgrade']
            except KeyError:
                self.infix_upgrade = None

            try:
                self.bonuses = itemJSON['details']['bonuses']
            except KeyError:
                self.bonuses = None

        if self.type == 'Weapon':
            self.weapon     = itemJSON['details']['type']
            self.damageType = itemJSON['details']['damage_type']
            self.minpower   = itemJSON['details']['min_power']
            self.maxpower   = itemJSON['details']['max_power']

            # Only relevent if a shield.
            if self.weapon == 'Shield':
                self.defense = itemJSON['details']['defense']

            self.infusions = itemJSON['details']['infusion_slots']
            # Some times items don't have runes/sigils.
            try:
                self.sigil = itemJSON['details']['suffix_item_id']
            except KeyError:
                self.sigil = None

            # And another one...
            try:
                self.infix_upgrade = itemJSON['details']['infix_upgrade']
            except KeyError:
                self.infix_upgrade = None

            self.what = itemJSON['details']['secondary_suffix_item_id']

class Skin:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official skin API.

    '''
    def __init__(self, skinJSON):
        self.id           = skinJSON['id']
        self.name         = skinJSON['name']
        self.type         = skinJSON['type']
        self.flags        = skinJSON['flags']
        self.restrictions = skinJSON['restrictions']
        self.icon         = skinJSON['icon']

        # Maybe one day we'll learn a thing or two about
        # API design and give default attributes to missing
        # things instead of just not defining them.
        try:
            self.description = skinJSON['description']
        except KeyError:
            self.description = None

        if self.type == 'Armor':
            self.slot         = skinJSON['details']['type']
            self.weight_class = skinJSON['details']['weight_class']

        if self.type == 'Weapon':
            self.weapon     = skinJSON['details']['type']
            self.damageType = skinJSON['details']['damage_type']

class Recipe:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official recipe API.

    '''
    def __init__(self, recipeJSON):
        self.id = recipeJSON['id']

        # Can be one of several values. Refer to wiki.
        self.type              = recipeJSON['type']
        self.output_id         = recipeJSON['output_item_id']
        self.output_item_count = recipeJSON['output_item_count']
        self.time              = recipeJSON['time_to_craft_ms']

        # Variable length list of disciplines that can craft recipe.
        self.disciplines = recipeJSON['disciplines']
        self.min_rating  = recipeJSON['min_rating']

        # List of flags. Possible values: AutoLearned, LearnedFromItem
        self.flags = recipeJSON['flags']

        # List of recipe ingredients. Contains: item_id, count
        self.ingredients = recipeJSON['ingredients']

class Dye:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official dye API.

    '''
    def __init__(self, dyeJSON):
        self.id       = dyeJSON['id']
        self.name     = dyeJSON['name']
        self.base_rgb = dyeJSON['base_rgb']

        # These are a dictionary containing
        # material specific dye information.
        self.cloth   = dyeJSON['cloth']
        self.leather = dyeJSON['leather']
        self.metal   = dyeJSON['metal']

class Specialization:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official specialization API.
    '''
    def __init__(self, specJSON):
        # We need this for building trait objects.
        self.traitsURL  = 'https://api.guildwars2.com/v2/traits?ids='

        # Back to regularly scheduled programming.
        self.id         = specJSON['id']
        self.name       = specJSON['name']
        self.profession = specJSON['profession']
        self.isElite    = specJSON['elite']
        self.icon       = specJSON['icon']

        # Empty lists for traits.
        self.minors = []
        self.majors = []

        # Build URL and trait lists then use them.
        minorIDs = ','.join(str(x) for x in specJSON['minor_traits'])
        majorIDs = ','.join(str(x) for x in specJSON['major_traits'])

        # Combine the ID strings.
        idString = ','.join((minorIDs, majorIDs))

        # Build objects for traits.
        for trait in getJson(self.traitsURL + idString):
            # Check if trait is minor or major.
            if trait['slot'] == 'Minor':
                self.minors.append(Trait(trait))

            elif trait['slot'] == 'Major':
                self.majors.append(Trait(trait))
                # I like the name of my exception. I think I'll keep it.
            else:
                raise TypeError('Weird trait type! Bailing')

class Trait:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 Official Trait API.
    '''
    def __init__(self, traitJSON):
        self.id             = traitJSON['id']
        self.name           = traitJSON['name']
        self.icon           = traitJSON['icon']
        self.description    = traitJSON['description']
        self.specialization = traitJSON['specialization']
        self.tier           = traitJSON['tier']
        self.slot           = traitJSON['slot']

        # Empty List for use later.
        self.skills = []

        # Optional keys. Again. Really ANET?
        try:
            self.facts = traitJSON['facts']
        except KeyError:
            self.facts = None

        try:
            # Fill the list with Skill objects.
            for skill in traitJSON['skills']:
                self.skills.append(Skill(skill))
        except KeyError:
            self.skills = None

        try:
            self.traited_facts = traitJSON['traited_facts']
        except KeyError:
            self.traited_facts  = None

# TODO / NOTE : This appears to be not in use
# by the Traits API yet. Still, it works and will only require
# minor adjustment when it's implemented.
class Skill:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official Trait API.

    This api returns an optional 'skills' list with unique
    identifier information. This object handles that.
    '''
    def __init__(self, skillJSON):
        self.id          = skillJSON['id']
        self.name        = skillJSON['name']
        self.description = skillJSON['description']
        self.icon        = skillJSON['icon']

        # Optional keys...PLS ANET
        try:
            self.facts = skillJSON['facts']
        except KeyError:
            self.facts = None

        try:
            self.traited_facts = skillJSON['traited_facts']
        except KeyError:
            self.traited_facts = None

class PVPMatch:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official PVP API.
    '''
    def __init__(self, pvpJSON):
        self.id         = pvpJSON['id']
        self.map_id     = pvpJSON['map_id']
        self.started    = pvpJSON['started']
        self.ended      = pvpJSON['ended']
        self.result     = pvpJSON['result']
        self.team       = pvpJSON['team']
        self.profession = pvpJSON['profession']
        self.scores     = pvpJSON['scores']

if __name__ == '__main__':
    pass

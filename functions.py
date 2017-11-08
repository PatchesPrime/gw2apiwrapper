import json
import urllib.parse
import urllib.request
from collections import namedtuple
from GW2API.exceptions import BadIDError, PermissionError, FlagParameterError


class typer(object):
    '''
    This decorator is designed to handle input of a
    variable type for the "getX" methods of objects.

    '''
    def __init__(self, f):
        '''
        Here we build the important information
        once at import, so we don't have to every time
        we call a decorated method..
        '''
        # Convient location for function.
        self.f = f

        # The string we'll need.
        self.api = self.f.__name__[3:].lower() + 's'

        # Some aren't consistent.
        # if self.api == 'dyes':
        #     self.api = 'colors'

        # # Don't judge me...
        # elif self.api == 'banks':
        #     self.api = 'bank'

    def _parse(self, string):
        '''
        Return a "safe" string for URLs.

        Won't even lie: I wrote this for PEP8 character count.
        '''
        return urllib.parse.quote(string)

    def __get__(self, instance, className):
        '''
        This is called immediately before __call__ internally
        and we need the instance object of the method who called us.

        This allows us to have that information.

        Returns typer.__call__
        '''
        self.obj       = instance
        self.className = className

        # Doesn't work unless you return where to
        # go next. Naturally, you want calling it to
        # call __call__
        return self.__call__

    def __call__(self, *args):
        '''
        The workhorse of the "typer" decorator.

        This section handles all the work of determining what to do
        with the input you passed the decorated method.

        Returns an object or list of objects depending on input.
        '''
        # This dictionary provides an easy way for me to direct
        # what kind of data I want from endpoints.
        crossList = {'skins': {'url': 'skins', 'obj': 'Skin'},
                     'dyes': {'url': 'colors', 'obj': 'Dye'},
                     'minis': {'url': 'minis', 'obj': 'Mini'},
                     'bank': {'url': 'items', 'obj': 'Item'},
                     'materials': {'url': 'items', 'obj': 'Material'},
                     'professions': {'url': 'professions', 'obj': 'Profession'},
                     'races': {'url': 'races', 'obj': 'Race'},
                     'pets': {'url': 'pets', 'obj': 'Pet'},
                     'masteries': {'url': 'masteries', 'obj': 'Mastery'},
                     'inventory': {'url': 'items', 'obj': 'Item'},
                     'outfits': {'url': 'outfits', 'obj': 'Outfit'},
                     'titles': {'url': 'titles', 'obj': 'Title'},
                     'recipes': {'url': 'recipes', 'obj': 'Recipe'},
                     'finishers': {'url': 'finishers', 'obj': 'Finisher'},
                     'legends': {'url': 'legends', 'obj': 'Legend'},
                     'dungeons': {'url': 'dungeons', 'obj': 'Dungeon'},
                     'raids': {'url': 'raids', 'obj': 'Raid'},
                     'skills': {'url': 'skills', 'obj': 'Skill'},
                     'items': {'url': 'items', 'obj': 'Item'},

                     # Guild endpoints.
                     'guildupgrades': {'url': 'guild/upgrades',
                                       'obj': 'GuildUpgrade'},
                     'guildpermissions': {'url': 'guild/permissions',
                                          'obj': 'GuildPermission'},
                     'guilds': {'url': 'guild',
                                'obj': 'Guild'},

                     # Achievement Stuff.
                     'achievements': {'url': 'achievements',
                                      'obj': 'Achievement'},
                     'achievementgroups': {'url': 'achievements/groups',
                                           'obj': 'AchievementGroup'},
                     'achievementcategorys': {'url': 'achievements/categories',
                                              'obj': 'AchievementCategory'}}

        # The AccountAPI get methods have an s at the end so
        # we need to remove that due to our __init__
        # "This is begging to be fixed." -Matt.
        # "One day." -Patches
        if self.api[-2:] == 'ss':
            api = self.api[:-1]

        # I didn't think this one through back then.
        # Hack in place :P
        elif self.api == 'banks':
            api = 'bank'

        elif self.api == 'inventorys':
            api = 'inventory'

        # Failure case? we try...
        else:
            api = self.api

        # Easy to remember url...
        if api in crossList.keys():
            url = crossList[api]['url']
        else:
            url = api

        # Dirty, but effective...?
        if 'AccountAPI' in str(self.obj):
            # We do this to check for permissions!
            self.f(self.obj)

            # For returning later.
            objects = []

            # This is hackery.
            if api != 'characters':
                data = self.obj.getJson('account/{}'.format(api))
            else:
                data = self.obj.getJson(api)

            # I am both proud of an ashamed of this line.
            # I split the skinIDs into 200 element chunks.
            # The API only supports 200 IDs at once.
            # Personally I blame terrorism.
            safeList = [data[x:x + 200] for x in range(0, len(data), 200)]

            # This feels wrong, I may address it later if
            # it begins to cause problems.
            try:
                # So it caused a minor problem. See Exception.
                if any(isinstance(x, dict) for x in data):
                    dictFlag = True
                else:
                    dictFlag = False
            except IndexError:
                # Basically, this caused a 'problem'. Note the quotes.
                # I don't have shared inventory slots. data = []
                # Obviously, the above type check breaks from this.
                # That's the theory anyway.
                # Anyone got one and an API key? :)

                # This will silently fail and set dictFlag to False.
                dictFlag = False
                pass

            # The construction of the skin attribute.
            for safe in safeList:
                # Clean them up into a proper string.
                try:
                    # I could do this in a list comprehension but
                    # then it is against PEP8 at 84 charactes.
                    temp = []
                    for current in safe:
                        if current is not None:
                                temp.append(current['id'])

                    # I much prefer list comprehensions.
                    # I will remove the 4 character difference somehow..
                    cleanStr = ','.join(str(x) for x in temp)

                except (KeyError, TypeError):
                    cleanStr = ','.join(str(x) for x in safe)

                # Build a pretty URL.
                if ' ' in cleanStr:
                    # Remove spaces.
                    parsed = self._parse(cleanStr)

                    # As it is now, this line works. If for some reason
                    # you begin getting strange errors, it might be this.
                    # It only works because the 'characters' endpoint is the
                    # only one with spaces.
                    cleanURL = '{}?ids={}'.format(url, parsed)

                else:
                    cleanURL = '{}?ids={}'.format(url, cleanStr)

                # Lets build some objects!
                for item in self.obj.getJson(cleanURL):
                    # This whole for loop makes me laugh.
                    try:
                        objName = crossList[api]['obj']
                    except KeyError:
                        # Something went wrong. Likely 'characters' fault.
                        # Try to build it off the API name
                        if api.title()[-1] == 's':
                            objName = api.title()[:-1]
                        else:
                            objName = api.title()

                    obj = namedtuple(objName, item.keys())

                    # Handle dictionaries differently.
                    if dictFlag:
                        # Add our item object to the dictionary
                        # that references it
                        for part in data:
                            # getBank can return None.
                            if part:
                                if item['id'] == part['id']:
                                    part.update({'object': obj(**item)})

                                    # List of dictionaries recreated!
                                    objects.append(part)
                    else:
                        objects.append(obj(**item))

            # We need to assign the data to the object.
            setattr(self.obj, api, objects)

            # Return it for immediate use as interator.
            # If that's what gets you hard.
            return(objects)

        # Type checking..
        if type(*args) is list:
            # Going to need this.
            objects = []

            # Build clean string to append to URL.
            cleanList = ','.join(str(x) for x in list(*args))

            # Build the URL.
            if ' ' in cleanList:
                # If there is a space, we need to parse that.
                cleanURL = '{}?ids={}'.format(url, self._parse(cleanList))
            else:
                cleanURL = '{}?ids={}'.format(url, cleanList)

            # Get the JSON.
            data = self.obj.getJson(cleanURL)

            # Generate the objects.
            for item in data:
                # Define a namedtuple for use as object.
                # I'm not sure how good of a practice it is to
                # create the namedtuple in here. Likely to change.
                obj = namedtuple(crossList[api]['obj'], item.keys())
                objects.append(obj(**item))

            # Return said objects.
            return(objects)

        elif type(*args) is str:
            # You shouldn't do this. It can take a really
            # long time.
            if args[0] == 'all':
                # Need this too.
                objects = []

                # Default case: get all of them.
                ids = self.obj.getJson(url)

                # Useful line is useful.
                safeList = [ids[x:x + 200] for x in range(0, len(ids), 200)]

                # Generate objects.
                for safe in safeList:
                    # Clean them up into a proper string.
                    cleanStr = ','.join(str(x) for x in safe)
                    cleanStr = self._parse(cleanStr)

                    # Build a pretty URL.
                    cleanURL = '{}?ids={}'.format(url, cleanStr)

                    data = self.obj.getJson(cleanURL)

                    # Build objects.
                    for item in data:
                        obj = namedtuple(crossList[api]['obj'], item.keys())
                        objects.append(obj(**item))

                # Return them all.
                return(objects)
            else:
                safeArgs = (url, self._parse(*args))
                jsonData = self.obj.getJson('{}/{}'.format(*safeArgs))

                obj = namedtuple(crossList[api]['obj'], jsonData.keys())
                return(obj(**jsonData))

        elif type(*args) is int:
            jsonData = self.obj.getJson('{}/{}'.format(url, *args))

            obj = namedtuple(crossList[api]['obj'], jsonData.keys())
            return(obj(**jsonData))


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
            print("Bad URL: ", url)

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

    If given a LIST/SET, it will return one of two values:

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

    if type(itemID) is list or type(itemID) is set:
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
        raise FlagParameterError('First argument must be "input" or "output"')

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


def getEmblem(emblemID, layer = None):
    '''
    A simple method to query the Guild Wars 2 emblem API
    to provide guild emblem assets.

    layer should be either 'fg' or 'bg'.

    eg.

    GW2API.functions.getEmblem(11)

    '''
    # The two URLs.
    urls = {'fg': 'https://api.guildwars2.com/v2/emblem/foregrounds',
            'bg': 'https://api.guildwars2.com/v2/emblem/backgrounds'}

    if layer in urls.keys():
        # Simple, we know what we want: get it.
        cleanURL = "{}?ids={}".format(urls[layer], emblemID)
        return getJson(cleanURL)
    else:
        # Still simple, but takes longer. We don't know what we want.
        # Get both.
        endList = []

        for key in urls.keys():
            cleanURL = "{}?ids={}".format(urls[key], emblemID)
            endList.append(getJson(cleanURL)[0])

    return endList

import json
import urllib.parse
import urllib.request
from .exceptions import BadIDError, PermissionError, FlagParameterError

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
        if self.api == 'dyes':
            self.api = 'colors'

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

    def __call__(self, param):
        '''
        The workhorse of the "typer" decorator.

        This section handles all the work of determining what to do
        with the input you passed the decorated method.

        Returns an object or list of objects depending on input.
        '''
        # Dirty, but effective...?
        if 'AccountAPI' in str(self.obj):
            # The AccountAPI gets have an s at the end so
            # we need to remove that due to our __init__
            if self.api[-2:]  == 'ss':
                self.api = self.api[:-1]

            # For returning later.
            objects = []

            # Get all of the IDs we're going to need.
            if self.api == 'characters':
                # We want character stuff, remove account prefix.
                data = self.obj.getJson(self.api)
            else:
                # We're not looking for character information.
                self.api = 'account/{}'.format(self.api)

            # Get the
            data = self.obj.getJson(self.api)

            # We do this again because the string for our
            # API has possibly been handled. It also sets us
            # up to easily integrate pvp/wvw later.
            if 'dyes' in self.api:
                self.api = 'colors'

            # I am both proud of an ashamed of this line.
            # I split the skinIDs into 200 element chunks.
            # The API only supports 200 IDs at once.
            # Personally I blame terrorism.
            safeList = [data[x:x + 200] for x in range(0, len(data), 200)]

            # The construction of the skin attribute.
            for safe in safeList:
                # Clean them up into a proper string.
                cleanStr = ','.join(str(x) for x in safe)

                # Build a pretty URL.
                if ' ' in cleanStr:
                    cleanURL = '{}?ids={}'.format(self.api, self._parse(cleanStr))
                else:
                    cleanURL = '{}?ids={}'.format(self.api, cleanStr)

                # Lets build some objects!
                for item in self.obj.getJson(cleanURL):
                    objects.append(self.f(self.obj, item))

            # Return it for immediate use as interator.
            # If that's what gets you hard.
            return(objects)

        # Type checking..
        if type(param) is list:
            # Going to need this.
            objects = []

            # Build clean string to append to URL.
            cleanList = ','.join(str(x) for x in param)

            # Build the URL.
            if ' ' in cleanList:
                # If there is a space, we need to parse that.
                cleanURL = '{}?ids={}'.format(self.api, self._parse(cleanList))
            else:
                #
                cleanURL = '{}?ids={}'.format(self.api, cleanList)

            # Get the JSON.
            data = self.obj.getJson(cleanURL)


            # Generate the objects.
            for item in data:
                objects.append(self.f(self.obj, item))

            # Return said objects.
            return(objects)

        elif type(param) is str:
            # You shouldn't do this. It can take a really
            # long time.
            if param == 'all':
                # Need this too.
                objects = []

                # Default case: get all of them.
                ids = self.obj.getJson(self.api)

                # Useful line is useful.
                safeList = [ids[x:x + 200] for x in range(0, len(ids), 200)]

                # Generate objects.
                for safe in safeList:
                    # Clean them up into a proper string.
                    cleanStr = ','.join(str(x) for x in safe)
                    cleanStr = self._parse(cleanStr)

                    # Build a pretty URL.
                    cleanURL = '{}?ids={}'.format(self.api, cleanStr)

                    data = self.obj.getJson(cleanURL)

                    # Build objects.
                    for item in data:
                        objects.append(self.f(self.obj, item))

                # Return them all.
                return(objects)
            else:
                safeArgs = (self.api, self._parse(param))
                jsonData = self.obj.getJson('{}/{}'.format(*safeArgs))

                return(self.f(self.obj, jsonData))

        elif type(param) is int:
            jsonData = self.obj.getJson('{}/{}'.format(self.api, param))

            return(self.f(self.obj, jsonData))

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

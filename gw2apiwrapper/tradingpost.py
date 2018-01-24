from gw2apiwrapper.functions import getJson, typer


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

    @typer
    def getListings(self, itemID):
        '''
        Get's the listings for a given ID or collection of
        IDs from the official Guild Wars 2 API.
        Returns a TPListing object, with attributes 'buys' and 'sells'.
        Both attributes contain a list of dictionaries with the keys:
          listings   - Contain the number of listings at these values.
          unit_price - The price in coin for the item.
          quantity   - Number of items being sold and bought for the listing.
        '''
        pass

    @typer
    def getPrices(self, itemID):
        '''
        Returns the Guild Wars 2 trading post prices
        for given item ID(s).
        Returns a dictionary if only one ID is given.
        Returns a list of dictionaries if a list of IDs is given.
        '''
        pass

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
        urls = {'coin': 'exchange/coins?quantity=',
                'gems': 'exchange/gems?quantity='}

        # Check if they gave proper input.
        if coin_or_gems in urls.keys():
            # Build a URL.
            cleanURL = '{}{}'.format(urls[coin_or_gems], quantity)

            # Use said URL.
            jsonData = self.getJson(cleanURL)

            # Returns a dictionary.
            return(jsonData)
        else:
            # Tell them what they did wrong.
            raise ValueError('First arg must be "coin" or "gems"')

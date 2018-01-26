from collections import namedtuple
from .functions import getJson, typer


class GlobalAPI:
    def __init__(self):
        self.url = 'https://api.guildwars2.com/v2/'

    def getJson(self, api):
        '''
        Simple wrapper for less typing.
        '''
        return(getJson(self.url + api, header=None))

    @typer
    def getMaterialCategories(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/materials#Response
        '''
        pass

    @typer
    def getItemStats(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/itemstats#Response
        '''
        pass

    @typer
    def getRaid(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/raids#Response
        '''
        pass

    @typer
    def getGuild(self, id_or_list):
        '''
        Query the non-authed Guild wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/guild/:id#Response
        '''
        pass

    @typer
    def getDungeon(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/dungeons#Response
        '''
        pass

    @typer
    def getSkill(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/skills#Response
        '''
        pass

    @typer
    def getLegend(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/legends#Response
        '''
        pass

    @typer
    def getFinisher(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/finishers#Response
        '''
        pass

    @typer
    def getTitle(self, id_or_list):
        '''
        Query the non-authed Guild wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/titles#Response
        '''
        pass

    @typer
    def getOutfit(self, id_or_list):
        '''
        Query the non-authed Guild wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/outfits#Response
        '''
        pass

    @typer
    def getMasteries(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/masteries#Response
        '''
        pass

    @typer
    def getPet(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/pets#Response
        '''
        pass

    @typer
    def getRace(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects from the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/races
        '''
        pass

    @typer
    def getProfession(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects based off the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/professions#Response
        '''
        pass

    @typer
    def getGuildUpgrade(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects off the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/guild/upgrades#Response
        '''
        pass

    @typer
    def getGuildPermission(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 API to build
        objects off the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/guild/permissions#Response
        '''
        pass

    @typer
    def getAchievement(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 achievement
        API and build Achievement(s) objects based off
        the returned json.

        https://wiki.guildwars2.com/wiki/API:2/achievements
        '''
        pass

    @typer
    def getAchievementGroup(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 achievement
        groups API and build objects based off the return JSON.

        https://wiki.guildwars2.com/wiki/API:2/achievements/groups#Response
        '''
        pass

    @typer
    def getAchievementCategory(self, id_or_list):
        '''
        Query the non-authed Guild Wars 2 achievement/categories
        API and build objects from the JSON.

        https://wiki.guildwars2.com/wiki/API:2/achievements/categories#Response
        '''
        pass

    @typer
    def getSkin(self, id_or_list):
        '''
        Query the non-authed skin Guild Wars 2 Skin API
        and build Skin object(s) based on it.

        https://wiki.guildwars2.com/wiki/API:2/skins#Response
        '''
        pass

    @typer
    def getItem(self, id_or_list):
        '''
        Query the Guild Wars 2 item API and build
        object(s) based off the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/items#Response
        '''
        pass

    @typer
    def getDye(self, id_or_list):
        '''
        Query the Guild Wars 2 Dye API and build
        object(s) based off the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/colors#Response
        '''
        pass

    @typer
    def getRecipe(self, id_or_list):
        '''
        Query the Guild Wars 2 Recipe API and build
        object(s) based off the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/recipes#Response
        '''
        pass

    @typer
    def getMini(self, id_or_list):
        '''
        Query the Guild Wars 2 Mini API and build
        object(s) based off the returned JSON.

        https://wiki.guildwars2.com/wiki/API:2/minis#Response
        '''
        pass

    def getWVWObjective(self, wvwID, objects=None):
        '''
        Query the Guild Wars 2 wvw/objectives API and build
        object(s) based off the returned JSON.

        Accepts lists, strings, and WVWMaps.

        https://wiki.guildwars2.com/wiki/API:2/wvw/objectives#Response
        '''
        if type(wvwID) is list:
            if objects is None:
                objects = []

            # Build clean string to append to URL.
            cleanList = ','.join(str(x) for x in wvwID)

            # Build the URL.
            cleanURL = 'wvw/objectives?ids={}'.format(cleanList)

            data = self.getJson(cleanURL)
            obj = namedtuple('WVWObjective', data[0].keys())

            # Generate the objects.
            for name in data:
                try:
                    objects.append(obj(**name))
                except TypeError:
                    # Not all WVW Objectives are created equal..
                    # ArenaNet, please be consistent..please.
                    specialObj = namedtuple('WVWObjective', name.keys())
                    objects.append(specialObj(**name))

            # Return said objects.
            return(objects)

        elif type(wvwID) is str:
            if wvwID == 'all':
                if objects is None:
                    objects = []

                # Default case: get all of them.
                wvwJSON = self.getJson('wvw/objectives?ids=all')
                obj = namedtuple('WVWObjective', wvwJSON[0].keys())

                # Generate objects.
                for item in wvwJSON:
                    # As is expected from the GW2 official API
                    # there is inconsistency and no default values
                    # for their returned JSON. So we must do this..
                    try:
                        objects.append(obj(**item))
                    except TypeError:
                        temp_obj = namedtuple('WVWObjective', item.keys())
                        objects.append(temp_obj(**item))

                # Return them all.
                return(objects)

            else:
                jsonData = self.getJson('wvw/objectives/{}'.format(wvwID))
                obj = namedtuple('WVWObjective', jsonData.keys())

                # Return the Object.
                return(obj(**jsonData))

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
            obj = namedtuple('WVWMatch', data[0].keys())

            # Generate the objects.
            for name in data:
                objects.append(obj(**name))

            # Return said objects.
            return(objects)

        elif type(matchID) is str:
            if matchID == 'all':
                if objects is None:
                    objects = []

                # Default case: get all of them.
                wvwJSON = self.getJson('wvw/matches?ids=all')
                obj = namedtuple('WVWMatch', wvwJSON[0].keys())

                # Generate objects.
                for item in wvwJSON:
                    objects.append(obj(**item))

                # Return them all.
                return(objects)

            else:
                jsonData = self.getJson('wvw/matches/{}'.format(matchID))
                obj = namedtuple('WVWMatch', jsonData.keys())

                # Return the Object.
                return(obj(**jsonData))

    def getDailies(self, tomorrow=False):
        '''
        Simple method to grab the dailies from GW2 official
        API and returns achievement objects for them.
        '''
        # Determine if we want the dailies from today or tomorrow.
        if tomorrow:
            jsonData = self.getJson('achievements/daily/tomorrow')
        else:
            jsonData = self.getJson('achievements/daily')

        # Pull all the IDs from the JSON data.
        idList = [data['id'] for value in jsonData.values() for data in value]

        return(self.getAchievement(idList))

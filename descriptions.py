from GW2API.functions import getJson
from urllib.error import HTTPError


class Specialization:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official specialization API.
    '''
    def __init__(self, specJSON):
        # We need this for building trait objects.
        self.traitsURL = 'https://api.guildwars2.com/v2/traits?ids='

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
        self.icon        = skillJSON['icon']
        self.chat_link   = skillJSON['chat_link']
        self.type        = skillJSON['type']
        self.weapon_type = skillJSON['weapon_type']
        self.slot        = skillJSON['slot']
        self.professions = skillJSON['professions']  # See NOTE below.

        # NOTE: This is how I WOULD build a profession for EACH
        # skill object, but turns out this can take a LONG time
        # if you're doing a bunch of skills. It's one request per.
        # Way too much. If you want a Profession object from this
        # You should call it yourself in your code rather than here.

        # p_link = 'https://api.guildwars2.com/v2/professions?id='
        # profs = ','.join(str(x) for x in skillJSON['professions'])
        # self.professions = [Profession(x) for x in [getJson(p_link + profs)]]

        # Optional. Either the value or None.
        self.categories    = skillJSON.get('categories')
        self.attunement    = skillJSON.get('attunement')
        self.cost          = skillJSON.get('cost')
        self.dual_wield    = skillJSON.get('dual_wield')
        self.description   = skillJSON.get('description')
        self.facts         = skillJSON.get('facts')
        self.traited_facts = skillJSON.get('traited_facts')
        self.initiative    = skillJSON.get('initiative')

        # Also optional, but no objects are built from this
        # data for the same reasons as professions up above.
        # If we built objects off these when defined, it would
        # DRASTICALLY increase the time to build Skill objects.
        # Once again, should you want these to be Skill objects
        # instead of IDs, you'll have to do that yourself in your
        # code.
        self.flip_skill       = skillJSON.get('flip_skill')
        self.next_chain       = skillJSON.get('next_chain')
        self.prev_chain       = skillJSON.get('prev_chain')
        self.transform_skills = skillJSON.get('transform_skills')
        self.bundle_skills    = skillJSON.get('bundle_skills')
        self.toolbelt_skill   = skillJSON.get('toolbelt_skill')


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


class WVWMatch:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official wvw/matches API.
    '''
    def __init__(self, wvwJSON):
        self.id    = wvwJSON['id']
        self.start = wvwJSON['start_time']
        self.end   = wvwJSON['end_time']

        # dictionaries
        self.scores = wvwJSON['scores']
        self.worlds = wvwJSON['worlds']
        self.deaths = wvwJSON['deaths']
        self.kills  = wvwJSON['kills']

        # Prime maps list.
        self.maps = []

        # Build the objects. No additional requests
        # so it's fast.
        for data in wvwJSON['maps']:
            self.maps.append(WVWMap(data))


class WVWMap:
    '''
    Class designed to turn WVWMatch 'maps' attributes
    into objects for easier use.
    '''
    def __init__(self, mapJSON):
        self.id      = mapJSON['id']
        self.type    = mapJSON['type']
        self.scores  = mapJSON['scores']
        self.bonuses = mapJSON['bonuses']

        # Note: this is currently bugged for EU
        self.kills   = mapJSON['kills']
        self.deaths  = mapJSON['deaths']

        # list of dictionaries.
        self.objectives = mapJSON['objectives']


class WVWObjective:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official wvw/objectives API.
    '''
    def __init__(self, wvwJSON):
        self.id        = wvwJSON['id']
        self.name      = wvwJSON['name']
        self.type      = wvwJSON['type']
        self.map_id    = wvwJSON['map_id']
        self.map_type  = wvwJSON['map_type']
        self.sector_id = wvwJSON['sector_id']
        self.coord     = wvwJSON.get('coord')

        try:
            self.marker = wvwJSON['marker']
        except KeyError:
            # Optional, so default it if missing.
            self.marker = None

        # Optional stuff that is only assigned when
        # processing a WVWMap object via getWVWObjective()
        # I couldn't think of a better way..
        self.owner        = None
        self.last_flipped = None
        self.claimed_by   = None
        self.claimed_at   = None


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


class Mini:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official mini API.
    '''
    def __init__(self, miniJSON):
        self.id      = miniJSON['id']
        self.name    = miniJSON['name']
        self.icon    = miniJSON['icon']
        self.order   = miniJSON['order']
        self.item_id = miniJSON['item_id']

        # Only exists on a few minis.
        try:
            self.unlock = miniJSON['unlock']
        except KeyError:
            self.unlock = None


class Achievement:
    '''
    Builds and object based off the JSON returned by the
    Guild Wars 2 official achievements API.
    '''
    def __init__(self, achieveJSON):
        self.id = achieveJSON['id']

        try:
            self.icon = achieveJSON['icon']
        except KeyError:
            self.icon = None

        self.name        = achieveJSON['name']
        self.description = achieveJSON['description']
        self.requirement = achieveJSON['requirement']
        self.type        = achieveJSON['type']
        self.flags       = achieveJSON['flags']


class AchievementGroup:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 offical achievements/groups API.
    '''
    def __init__(self, groupJSON):
        catURL = 'https://api.guildwars2.com/v2/achievements/categories?ids='
        self.id          = groupJSON['id']
        self.name        = groupJSON['name']
        self.description = groupJSON['description']
        self.order       = groupJSON['order']
        self.categories  = []

        ids = ','.join(str(x) for x in groupJSON['categories'])
        for cat in getJson(catURL + ids):
            self.categories.append(AchievementCategory(cat))


class AchievementCategory:
    '''
    Builds an object based off the JSON returned by
    the Guild Wars 2 official achievements/categories
    API.
    '''
    def __init__(self, catJSON):
        self.id           = catJSON['id']
        self.name         = catJSON['name']
        self.description  = catJSON['description']
        self.order        = catJSON['order']
        self.icon         = catJSON['icon']
        self.achievements = catJSON['achievements']


class GuildUpgrade:
    '''
    Builds an object based off the JSON returned by
    the Guild Wars 2 official guild/upgrades API.
    '''
    def __init__(self, upgradeJSON):
        upgradeURL = 'https://api.guildwars2.com/v2/guild/upgrades?ids='
        self.id   = upgradeJSON['id']
        self.name = upgradeJSON['name']
        self.icon           = upgradeJSON['icon']
        self.build_time     = upgradeJSON['build_time']
        self.required_level = upgradeJSON['required_level']
        self.experience     = upgradeJSON['experience']
        self.prerequisites  = []

        # Build upgrades.
        ids = ','.join(str(x) for x in upgradeJSON['prerequisites'])

        try:
            for upgrade in getJson(upgradeURL + ids):
                self.prerequisites.append(GuildUpgrade(upgrade))
        except HTTPError:
            # Just has no prerequisites...I guess?
            pass

        # Nested
        self.type = upgradeJSON['type']
            # AccumulatingCurrency - Used for mine capacity upgrades.
            # BankBag              - Used for guild bank upgrades. Additional fields include:
            #     bag_max_items (number) - The maximum item slots of the guild bank tab.
            #     bag_max_coins (number) - The maximum amount of coins that can be stored in the bank tab.
            # Boost      - Used for permanent guild buffs such as waypoint cost reduction.
            # Claimable  - Used for guild WvW tactics.
            # Consumable - Used for banners and guild siege.
            # Decoration - Used for decorations that must be crafted by a Scribe.
            # Hub        - Used for the Guild Initiative office unlock.
            # Unlock     - Used for permanent unlocks, such as merchants and arena decorations.

        # Nested
        self.costs = upgradeJSON['costs']
            # type (string) - The type of cost. One of Item, Collectible, Currency
            # name (string) - The name of the cost.
            # count (number) - The amount needed.
            # item_id (number, optional) - The ID of the item, if applicable.


class Guild:
    '''
    Builds an object representing a Guild according to the GW2API.
    '''
    def __init__(self, guildJSON):
        self.id     = guildJSON['id']
        self.name   = guildJSON['name']
        self.tag    = guildJSON['tag']
        self.emblem = guildJSON['emblem']

        # Optional tags.
        self.level     = guildJSON.get('level')
        self.motd      = guildJSON.get('motd')
        self.influence = guildJSON.get('influence')
        self.aetherium = guildJSON.get('aetherium')
        self.favor     = guildJSON.get('favor')


class GuildPermission:
    '''
    Builds a simple object based off the JSON returned by
    the Guild Wars 2 official guild/permissions API.
    '''
    def __init__(self, gpJSON):
        # Not sure about this class, honestly.
        self.id          = gpJSON['id']
        self.name        = gpJSON['name']
        self.description = gpJSON['description']


class Raid:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official raids API.
    '''
    def __init__(self, rJSON):
        self.id    = rJSON['id']
        self.wings = rJSON['wings']

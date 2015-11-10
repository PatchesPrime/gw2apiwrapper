from .functions import getJson

class Character:
    '''
    Builds an object based off the JSON returned by the
    Guild Wars 2 official character API.
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

        # These are optional, depending on permissions.
        try:
            self.gear = playerJSON['equipment']
        except KeyError:
            # Obviously they didn't give equipment access.
            self.gear = None

        try:
            # This is a 3 element list. pvp, wvw, pve
            self.builds = playerJSON['specializations']
        except KeyError:
            self.builds = None

        try:
            self.bags = playerJSON['bags']
        except KeyError:
            self.bags = None

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
            self.slot      = itemJSON['details']['type']
            self.weight    = itemJSON['details']['weight_class']
            self.defense   = itemJSON['details']['defense']
            self.infusions = itemJSON['details']['infusion_slots']

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
            self.what = itemJSON['details']['secondary_suffix_item_id']

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
            self.trinket   = itemJSON['details']['type']
            self.infusions = itemJSON['details']['infusion_slots']

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
            self.upgrade    = itemJSON['details']['type']
            self.socketable = itemJSON['details']['flags']
            self.infusion   = itemJSON['details']['infusion_upgrade_flags']
            self.suffix     = itemJSON['details']['suffix']

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
        self.coord     = wvwJSON['coord']

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
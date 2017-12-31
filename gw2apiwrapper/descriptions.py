from gw2apiwrapper.functions import getJson


class Specialization:  # pragma: no cover
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


class Skill:  # pragma: no cover
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

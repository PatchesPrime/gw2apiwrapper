import unittest
from GW2API import GlobalAPI
from GW2API import descriptions

# This object retains nothing, so it's fine for it
# to be reused.
gAPI = GlobalAPI()


class TestGlobalAPI(unittest.TestCase):
    def test_getGuild(self):
        guild = gAPI.getGuild('116E0C0E-0035-44A9-BB22-4AE3E23127E5')
        self.assertTrue(isinstance(guild, descriptions.Guild))
        self.assertTrue(guild.name == 'Edit Conflict')

    def test_getDungeon(self):
        dungeon = gAPI.getDungeon('caudecus_manor')
        self.assertTrue(isinstance(dungeon, descriptions.Dungeon))
        self.assertTrue(dungeon.paths[1]['id'] == 'asura')

    def test_getSkill(self):
        # Test int()
        skill = gAPI.getSkill(14375)
        self.assertTrue(isinstance(skill, descriptions.Skill))
        self.assertEqual(skill.name, 'Arcing Slice')

        # Test string()
        skill = gAPI.getSkill(5516)
        self.assertTrue(isinstance(skill, descriptions.Skill))
        self.assertEqual(skill.name, 'Conjure Fiery Greatsword')

        # Test list()
        for unit in gAPI.getSkill([5516, 5517, '14375']):
            self.assertTrue(isinstance(unit, descriptions.Skill))

    def test_getLegend(self):
        legend = gAPI.getLegend('Legend2')

        self.assertTrue(isinstance(legend, descriptions.Legend))
        self.assertEqual(legend.heal.name, 'Enchanted Daggers')
        self.assertEqual(legend.heal.slot, 'Heal')

    def test_getFinisher(self):
        # Test int()
        # I know for a fact finisher id 12 has an unlock item.
        finisher = gAPI.getFinisher(12)
        item = finisher.unlock_items[0]
        self.assertTrue(isinstance(finisher, descriptions.Finisher))
        self.assertEqual(finisher.name, 'Whump the Giant Finisher')
        self.assertEqual(item.name, 'Permanent Whump the Giant Finisher')

        # Test string()
        # Finisher id 1 does not have a finisher item.
        finisher = gAPI.getFinisher('1')
        self.assertTrue(isinstance(finisher, descriptions.Finisher))
        self.assertEqual(finisher.name, 'Rabbit Rank Finisher')

        # Test list()
        # Test both cases: Finisher unlock item and no unlock item.
        for unit in gAPI.getFinisher([1, 12]):
            self.assertTrue(
                isinstance(unit, descriptions.Finisher)
            )
            if unit.unlock_items is not None:
                self.assertTrue(
                    isinstance(unit.unlock_items[0], descriptions.Item)
                )
                self.assertEqual(
                    unit.unlock_items[0].name,
                    'Permanent Whump the Giant Finisher'
                )

    def test_getTitle(self):
        # Test int()
        title = gAPI.getTitle(8)
        achievement = title.achievements[0]
        self.assertTrue(isinstance(title, descriptions.Title))
        self.assertTrue(isinstance(achievement, descriptions.Achievement))
        self.assertEqual(title.name, 'Flameseeker')
        self.assertEqual(achievement.name, 'Flameseeker')

        # Test string()
        title = gAPI.getTitle('8')
        achievement = title.achievements[0]
        self.assertTrue(isinstance(title, descriptions.Title))
        self.assertTrue(isinstance(achievement, descriptions.Achievement))
        self.assertEqual(title.name, 'Flameseeker')
        self.assertEqual(achievement.name, 'Flameseeker')

        # Test list()
        for unit in gAPI.getTitle([8, 9]):
            self.assertTrue(
                isinstance(unit, descriptions.Title)
            )
            self.assertTrue(
                isinstance(unit.achievements[0], descriptions.Achievement)
            )

    def test_getOutfit(self):
        # Test int()
        outfit = gAPI.getOutfit(8)
        unlock_items = outfit.unlock_items[0]
        self.assertTrue(isinstance(outfit, descriptions.Outfit))
        self.assertTrue(isinstance(unlock_items, descriptions.Item))
        self.assertEqual(outfit.name, 'Shadow Assassin Outfit')
        self.assertEqual(unlock_items.name, 'Shadow Assassin Outfit')

        # Test string()
        outfit = gAPI.getOutfit('10')
        unlock_items = outfit.unlock_items[0]
        self.assertTrue(isinstance(outfit, descriptions.Outfit))
        self.assertTrue(isinstance(unlock_items, descriptions.Item))
        self.assertEqual(outfit.name, 'Ceremonial Plated Outfit')
        self.assertEqual(unlock_items.name, 'Ceremonial Plated Outfit')

        # Test list()
        for unit in gAPI.getOutfit([8, 10]):
            self.assertTrue(
                isinstance(unit, descriptions.Outfit)
            )
            self.assertTrue(
                isinstance(unit.unlock_items[0], descriptions.Item)
            )

    def test_getMasteries(self):
        # Test int()
        mastery = gAPI.getMasteries(1)
        self.assertTrue(isinstance(mastery, descriptions.Mastery))
        self.assertEqual(mastery.region, 'Maguuma')

        # Test string()
        mastery = gAPI.getMasteries('2')
        self.assertTrue(isinstance(mastery, descriptions.Mastery))
        self.assertEqual(mastery.region, 'Maguuma')

        # Test list()
        for unit in gAPI.getMasteries([8, 10]):
            self.assertTrue(
                isinstance(unit, descriptions.Mastery)
            )

    def test_getPet(self):
        # Test int()
        pet = gAPI.getPet(33)
        self.assertTrue(isinstance(pet, descriptions.Pet))
        self.assertEqual(pet.name, 'Juvenile Forest Spider')
        self.assertTrue(isinstance(pet.skills[0], descriptions.Skill))

        # Test string()
        pet = gAPI.getPet('42')
        self.assertTrue(isinstance(pet, descriptions.Pet))
        self.assertEqual(pet.name, 'Juvenile Red Jellyfish')
        self.assertTrue(isinstance(pet.skills[0], descriptions.Skill))

        # Test list()
        for unit in gAPI.getPet([33, 42]):
            self.assertTrue(
                isinstance(unit, descriptions.Pet)
            )
            self.assertTrue(
                isinstance(unit.skills[0], descriptions.Skill)
            )

    def test_getRace(self):
        # This works a bit different.
        race = gAPI.getRace('Asura')
        self.assertTrue(isinstance(race, descriptions.Race))

        # Check its skills.
        self.assertTrue(len(race.skills) == 7)
        self.assertEqual(race.skills[0].name, 'Pain Inverter')
        for skill in race.skills:
            self.assertTrue(isinstance(skill, descriptions.Skill))

    def test_getProfession(self):
        # Same thing. Different input.
        prof = gAPI.getProfession('Engineer')
        self.assertTrue(isinstance(prof, descriptions.Profession))

        # Check specializations. Also omg pep8pls
        self.assertTrue(
            isinstance(
                prof.specializations[0],
                descriptions.Specialization
            )
        )

        # If they ever random it up, this will likely break. ANET PLS
        self.assertEqual(prof.specializations[0].name, 'Explosives')

        for spec in prof.specializations:
            self.assertTrue(isinstance(spec, descriptions.Specialization))

    def test_getGuildUpgrade(self):
        upgrade = gAPI.getGuildUpgrade(55)
        self.assertTrue(isinstance(upgrade, descriptions.GuildUpgrade))
        self.assertEqual(upgrade.name, 'Guild Treasure Trove')

        # Check prerequisites
        for pre in upgrade.prerequisites:
            self.assertTrue(
                isinstance(
                    pre,
                    descriptions.GuildUpgrade
                )
            )

        # Check individual for known data.
        self.assertEqual(
            upgrade.prerequisites[0].name, 'Guild Vault: Stash'
        )
        self.assertEqual(
            upgrade.prerequisites[1].name, 'Market Restoration 1'
        )

    def test_getGuildPermission(self):
        perm = gAPI.getGuildPermission('Admin')
        self.assertEqual(perm.name, 'Admin Lower Ranks.')

    def test_getAchievement(self):
        # Test int()
        achieve = gAPI.getAchievement(1840)
        self.assertTrue(isinstance(achieve, descriptions.Achievement))
        self.assertEqual(achieve.name, 'Daily Completionist')

        # Test string()
        achieve = gAPI.getAchievement('910')
        self.assertTrue(isinstance(achieve, descriptions.Achievement))
        self.assertEqual(achieve.name, 'Tequatl the Sunless')

        # Test list()
        for unit in gAPI.getAchievement([1840, 910, 2258]):
            self.assertTrue(
                isinstance(unit, descriptions.Achievement)
            )

    def test_getAchievementGroup(self):
        # Weird IDs.
        ag = gAPI.getAchievementGroup('65B4B678-607E-4D97-B458-076C3E96A810')
        self.assertTrue(isinstance(ag, descriptions.AchievementGroup))
        self.assertEqual(ag.name, 'Heart of Thorns')

        for ac in ag.categories:
            self.assertTrue(isinstance(ac, descriptions.AchievementCategory))

    def test_getAchievementCategory(self):
        ac = gAPI.getAchievementCategory(1)
        self.assertTrue(isinstance(ac, descriptions.AchievementCategory))
        self.assertEqual(ac.name, 'Slayer')

        # Test string()
        ac = gAPI.getAchievementCategory('2')
        self.assertTrue(isinstance(ac, descriptions.AchievementCategory))
        self.assertEqual(ac.name, 'Hero')

        for unit in gAPI.getAchievementCategory([1, 2]):
            self.assertTrue(
                isinstance(unit, descriptions.AchievementCategory)
            )

    def test_getSkin(self):
        # Test int()
        skin = gAPI.getSkin(10)
        self.assertTrue(isinstance(skin, descriptions.Skin))
        self.assertEqual(skin.name, 'Seer Pants')

        # Test string()
        skin = gAPI.getSkin('1')
        self.assertTrue(isinstance(skin, descriptions.Skin))
        self.assertEqual(skin.name, 'Chainmail Leggings')

        # Test list()
        for unit in gAPI.getSkin([1, 2]):
            self.assertTrue(
               isinstance(unit, descriptions.Skin)
            )

    def test_getItem(self):
        # Test int()
        item = gAPI.getItem(28445)
        self.assertTrue(isinstance(item, descriptions.Item))
        self.assertEqual(item.name, 'Strong Soft Wood Longbow of Fire')

        # Test string()
        item = gAPI.getItem('12452')
        self.assertTrue(isinstance(item, descriptions.Item))
        self.assertEqual(item.name, 'Omnomberry Bar')

        # Test list()
        for unit in gAPI.getItem([1, 2]):
            self.assertTrue(
                isinstance(unit, descriptions.Item)
            )

    def test_getDye(self):
        # Test int()
        dye = gAPI.getDye(10)
        self.assertTrue(isinstance(dye, descriptions.Dye))
        self.assertEqual(dye.name, 'Sky')

        # Test string()
        dye = gAPI.getDye('11')
        self.assertTrue(isinstance(dye, descriptions.Dye))
        self.assertEqual(dye.name, 'Starry Night')

        # Test list()
        for unit in gAPI.getDye([1, 2]):
            self.assertTrue(
                isinstance(unit, descriptions.Dye)
            )

    def test_getRecipe(self):
        # Test int()
        recipe = gAPI.getRecipe(7319)
        self.assertTrue(isinstance(recipe, descriptions.Recipe))
        self.assertEqual(recipe.output_id, 46742)

        # Test string()
        recipe = gAPI.getRecipe('7419')
        self.assertTrue(isinstance(recipe, descriptions.Recipe))
        self.assertEqual(recipe.output_id, 46944)

        # Test list()
        for unit in gAPI.getRecipe([1, 2]):
            self.assertTrue(
                isinstance(unit, descriptions.Recipe)
            )

    def test_getMini(self):
        # Test int()
        mini = gAPI.getMini(1)
        self.assertTrue(isinstance(mini, descriptions.Mini))
        self.assertEqual(mini.name, 'Miniature Rytlock')

        # Test string()
        mini = gAPI.getMini('2')
        self.assertTrue(isinstance(mini, descriptions.Mini))
        self.assertEqual(mini.name, 'Miniature Servitor Golem')

        # Test list()
        for unit in gAPI.getMini([1, 2]):
            self.assertTrue(
                isinstance(unit, descriptions.Mini)
            )

    def test_getWVWObjective(self):
        wvwobjid = gAPI.getWVWObjective('all')
        self.assertTrue(len(wvwobjid) > 100)
        # self.assertEqual(wvwobjid[0].name, 'Aldon\'s Ledge')

        wvwobjid = gAPI.getWVWObjective('38-11')
        self.assertEqual(wvwobjid.name, 'Aldon\'s Ledge')

    def test_getWVWMatches(self):
        wvwmatch = gAPI.getWVWMatches('all')
        self.assertTrue(len(wvwmatch) > 5)

        for unit in wvwmatch:
            self.assertTrue(isinstance(unit, descriptions.WVWMatch))

    def test_getDailies(self):
        dailies = gAPI.getDailies()
        self.assertTrue(len(dailies) > 10)

        for unit in dailies:
            self.assertTrue(
                isinstance(unit, descriptions.Achievement)
            )

import unittest
from GW2API import GlobalAPI

# This object retains nothing, so it's fine for it
# to be reused.
gAPI = GlobalAPI()


class TestGlobalAPI(unittest.TestCase):
    def test_getRaid(self):
        raid = gAPI.getRaid('forsaken_thicket')
        self.assertEqual(type(raid).__name__, 'Raid')
        self.assertTrue(raid.id == 'forsaken_thicket')

    def test_getGuild(self):
        guild = gAPI.getGuild('116E0C0E-0035-44A9-BB22-4AE3E23127E5')
        self.assertEqual(type(guild).__name__, 'Guild')
        self.assertTrue(guild.name == 'Edit Conflict')

    def test_getDungeon(self):
        dungeon = gAPI.getDungeon('caudecus_manor')
        self.assertEqual(type(dungeon).__name__, 'Dungeon')
        self.assertTrue(dungeon.paths[1]['id'] == 'asura')

    def test_getSkill(self):
        # Test int()
        skill = gAPI.getSkill(14375)
        self.assertEqual(type(skill).__name__, 'Skill')
        self.assertEqual(skill.name, 'Arcing Slice')

        # Test str()
        skill = gAPI.getSkill('5516')
        self.assertEqual(type(skill).__name__, 'Skill')
        self.assertEqual(skill.name, 'Conjure Fiery Greatsword')

        # Test list()
        for unit in gAPI.getSkill([5516, 5517, '14375']):
            self.assertEqual(type(unit).__name__, 'Skill')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getSkill, {14375})

    def test_getLegend(self):
        legend = gAPI.getLegend('Legend2')

        self.assertEqual(type(legend).__name__, 'Legend')
        self.assertEqual(legend.heal, 26937)

    def test_getFinisher(self):
        # Test int()
        # I know for a fact finisher id 12 has an unlock item.
        finisher = gAPI.getFinisher(12)
        self.assertEqual(type(finisher).__name__, 'Finisher')

        # self.assertTrue(isinstance(finisher, descriptions.Finisher))
        self.assertEqual(finisher.name, 'Whump the Giant Finisher')

        # Test str()
        # Finisher id 1 does not have a finisher item.
        finisher = gAPI.getFinisher('1')
        self.assertEqual(type(finisher).__name__, 'Finisher')
        self.assertEqual(finisher.name, 'Rabbit Rank Finisher')

        # Test list()
        for unit in gAPI.getFinisher([1, 12]):
            self.assertEqual(type(unit).__name__, 'Finisher')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getFinisher, {1})

    def test_getTitle(self):
        # Test int()
        title = gAPI.getTitle(8)
        self.assertEqual(type(title).__name__, 'Title')
        self.assertEqual(title.name, 'Flameseeker')
        self.assertEqual(title.achievement, 118)

        # Test str()
        title = gAPI.getTitle('8')
        self.assertEqual(type(title).__name__, 'Title')
        self.assertEqual(title.name, 'Flameseeker')
        self.assertEqual(title.achievement, 118)

        # Test list()
        for unit in gAPI.getTitle([8, 9]):
            self.assertEqual(type(unit).__name__, 'Title')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getTitle, {8})

    def test_getOutfit(self):
        # Test int()
        outfit = gAPI.getOutfit(8)
        self.assertEqual(type(outfit).__name__, 'Outfit')
        self.assertEqual(outfit.name, 'Shadow Assassin Outfit')
        self.assertEqual(outfit.unlock_items[0], 66658)

        # Test str()
        outfit = gAPI.getOutfit('10')
        self.assertEqual(type(outfit).__name__, 'Outfit')
        self.assertEqual(outfit.name, 'Ceremonial Plated Outfit')
        self.assertEqual(outfit.unlock_items[0], 67040)

        # Test list()
        for unit in gAPI.getOutfit([8, 10]):
            self.assertEqual(type(outfit).__name__, 'Outfit')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getOutfit, {8})

    def test_getMasteries(self):
        # Test int()
        mastery = gAPI.getMasteries(1)
        self.assertEqual(type(mastery).__name__, 'Mastery')
        self.assertEqual(mastery.region, 'Maguuma')

        # Test str()
        mastery = gAPI.getMasteries('2')
        self.assertEqual(type(mastery).__name__, 'Mastery')
        self.assertEqual(mastery.region, 'Maguuma')

        # Test list()
        for unit in gAPI.getMasteries([8, 10]):
            self.assertEqual(type(mastery).__name__, 'Mastery')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getMasteries, {1})

    def test_getPet(self):
        # Test int()
        pet = gAPI.getPet(33)
        self.assertEqual(type(pet).__name__, 'Pet')
        self.assertEqual(pet.name, 'Juvenile Forest Spider')

        # Test str()
        pet = gAPI.getPet('42')
        self.assertEqual(type(pet).__name__, 'Pet')
        self.assertEqual(pet.name, 'Juvenile Red Jellyfish')

        # Test list()
        for unit in gAPI.getPet([33, 42]):
            self.assertEqual(type(pet).__name__, 'Pet')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getPet, {42})

    def test_getRace(self):
        # This works a bit different.
        race = gAPI.getRace('Asura')
        self.assertEqual(type(race).__name__, 'Race')

        # Check its skills.
        self.assertTrue(len(race.skills) == 7)

    def test_getProfession(self):
        # Same thing. Different input.
        prof = gAPI.getProfession('Engineer')
        self.assertEqual(type(prof).__name__, 'Profession')

    def test_getGuildUpgrade(self):
        upgrade = gAPI.getGuildUpgrade(55)
        self.assertEqual(type(upgrade).__name__, 'GuildUpgrade')
        self.assertEqual(upgrade.name, 'Guild Treasure Trove')

        self.assertTrue(58 in upgrade.prerequisites)

    def test_getGuildPermission(self):
        perm = gAPI.getGuildPermission('Admin')
        self.assertEqual(type(perm).__name__, 'GuildPermission')
        self.assertEqual(perm.name, 'Admin Lower Ranks.')

    def test_getAchievement(self):
        # Test int()
        achieve = gAPI.getAchievement(1840)
        self.assertEqual(type(achieve).__name__, 'Achievement')
        self.assertEqual(achieve.name, 'Daily Completionist')

        # Test str()
        achieve = gAPI.getAchievement('910')
        self.assertEqual(type(achieve).__name__, 'Achievement')
        self.assertEqual(achieve.name, 'Tequatl the Sunless')

        # Test list()
        for unit in gAPI.getAchievement([1840, 910, 2258]):
            self.assertEqual(type(achieve).__name__, 'Achievement')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getAchievement, {910})

    def test_getAchievementGroup(self):
        # Weird IDs.
        ag = gAPI.getAchievementGroup('65B4B678-607E-4D97-B458-076C3E96A810')
        self.assertEqual(type(ag).__name__, 'AchievementGroup')
        self.assertEqual(ag.name, 'Heart of Thorns')

    def test_getAchievementCategory(self):
        # Test int()
        ac = gAPI.getAchievementCategory(1)
        self.assertEqual(type(ac).__name__, 'AchievementCategory')
        self.assertEqual(ac.name, 'Slayer')

        # Test str()
        ac = gAPI.getAchievementCategory('2')
        self.assertEqual(type(ac).__name__, 'AchievementCategory')
        self.assertEqual(ac.name, 'Hero')

        # Test list()
        for unit in gAPI.getAchievementCategory([1, 2]):
            self.assertEqual(type(ac).__name__, 'AchievementCategory')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getAchievementCategory, {1})

    def test_getSkin(self):
        # Test int()
        skin = gAPI.getSkin(10)
        self.assertEqual(type(skin).__name__, 'Skin')
        self.assertEqual(skin.name, 'Seer Pants')

        # Test str()
        skin = gAPI.getSkin('1')
        self.assertEqual(type(skin).__name__, 'Skin')
        self.assertEqual(skin.name, 'Chainmail Leggings')

        # Test list()
        for unit in gAPI.getSkin([1, 2]):
            self.assertEqual(type(skin).__name__, 'Skin')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getSkin, {10})

    def test_getItem(self):
        # Test int()
        item = gAPI.getItem(28445)
        self.assertEqual(type(item).__name__, 'Item')
        self.assertEqual(item.name, 'Strong Soft Wood Longbow of Fire')

        # Test str()
        item = gAPI.getItem('12452')
        self.assertEqual(type(item).__name__, 'Item')
        self.assertEqual(item.name, 'Omnomberry Bar')

        # Test list()
        gAPI.getItem([1])
        for unit in gAPI.getItem([1, 2]):
            self.assertEqual(type(unit).__name__, 'Item')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getItem, {28445})

    def test_getDye(self):
        # Test int()
        dye = gAPI.getDye(10)
        self.assertEqual(type(dye).__name__, 'Dye')
        self.assertEqual(dye.name, 'Sky')

        # Test str()
        dye = gAPI.getDye('11')
        self.assertEqual(type(dye).__name__, 'Dye')
        self.assertEqual(dye.name, 'Starry Night')

        # Test list()
        for unit in gAPI.getDye([1, 2]):
            self.assertEqual(type(dye).__name__, 'Dye')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getDye, {10})

    def test_getRecipe(self):
        # Test int()
        recipe = gAPI.getRecipe(7319)
        self.assertEqual(type(recipe).__name__, 'Recipe')
        self.assertEqual(recipe.output_item_id, 46742)

        # Test str()
        recipe = gAPI.getRecipe('7419')
        self.assertEqual(type(recipe).__name__, 'Recipe')
        self.assertEqual(recipe.output_item_id, 46944)

        # Test list()
        for unit in gAPI.getRecipe([1, 2]):
            self.assertEqual(type(recipe).__name__, 'Recipe')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getRecipe, {7319})

    def test_getMini(self):
        # Test int()
        mini = gAPI.getMini(1)
        self.assertEqual(type(mini).__name__, 'Mini')
        self.assertEqual(mini.name, 'Miniature Rytlock')

        # Test str()
        mini = gAPI.getMini('2')
        self.assertEqual(type(mini).__name__, 'Mini')
        self.assertEqual(mini.name, 'Miniature Servitor Golem')

        # Test list()
        for unit in gAPI.getMini([1, 2]):
            self.assertEqual(type(mini).__name__, 'Mini')

        # Test unsupported type
        self.assertRaises(NotImplementedError, gAPI.getMini, {2})

    def test_getWVWObjective(self):
        wvwobjid = gAPI.getWVWObjective('all')
        self.assertTrue(len(wvwobjid) > 100)

        # Test for list functionality.
        wvwids = [x.id for x in wvwobjid]
        wvwobjid = gAPI.getWVWObjective(wvwids)

        wvwobjid = gAPI.getWVWObjective('38-11')
        self.assertEqual(wvwobjid.name, 'Aldon\'s Ledge')

    def test_getWVWMatches(self):
        wvwmatches = gAPI.getWVWMatches('all')
        self.assertTrue(len(wvwmatches) > 5)

        # Test list functionality.
        matchIDs = [x.id for x in wvwmatches]
        wvwmatches = gAPI.getWVWMatches(matchIDs)

        for unit in wvwmatches:
            self.assertEqual(type(unit).__name__, 'WVWMatch')

    def test_getDailies(self):
        dailies = gAPI.getDailies()
        self.assertTrue(len(dailies) > 10)

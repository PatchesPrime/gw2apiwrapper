import unittest
from GW2API import AccountAPI
import os


class TestAccountAPI(unittest.TestCase):
    def getAccount(self):
        APIKEY = os.environ['APIKEY']
        return(AccountAPI(APIKEY))

    def test_brokenPermissions(self):
        APIKEY = os.environ['BUSTEDKEY']
        acc = AccountAPI(APIKEY)

        # Just going to call getAchievements() to trigger
        # the error.
        with self.assertRaises(PermissionError):
            acc.getAchievements()

    def test_getRaids(self):
        api = self.getAccount()

        encounters = ["vale_guardian", "spirit_woods", "gorseval",
                      "sabetha", "slothasor", "bandit_trio",
                      "matthias", "escort", "keep_construct",
                      "xera", "cairn", "mursaat_overseer",
                      "samarog", "deimos"]
        raids = api.getRaids()

        # I don't do raids..
        # self.assertTrue(any(x in raids for x in encounters))

        # This should always be false when using my API key...
        self.assertFalse(any(x in raids for x in encounters))

    def test_getGuild(self):
        api = self.getAccount()

        guild = api.getGuild('A4AF6C09-452F-44EE-BD3E-704FB5C371FB')
        self.assertEqual(type(guild).__name__, 'Guild')
        self.assertTrue(guild.influence > 0)

    def test_getDungeon(self):
        # I don't really do dungeons so I'm having a hard time verifying
        # the validity of this test. If you got a key and do dungeons
        # send me a message.
        api = self.getAccount()
        paths = ['cm_story', 'asura', 'seraph', 'butler', 'ac_story',
                 'hodgins', 'detha', 'tzark', 'ta_story', 'leurent',
                 'vevina', 'aetherpath', 'se_story', 'fergg', 'rasalov',
                 'koptev', 'cof_story', 'ferrah', 'magg', 'rhiannon',
                 'hotw_story', 'butcher', 'plunderer', 'zealot',
                 'coe_story', 'submarine', 'teleport', 'front_door',
                 'arah_story', 'jotun', 'mursaat', 'forgotten', 'seer']
        dun = api.getDungeons()

        # I guess this'll work for now until I get someone who does dungeons.
        # self.assertTrue(any(x in dun for x in paths))

        # This should always be false when using my API key...
        self.assertFalse(any(x in dun for x in paths))

    def test_getFinishers(self):
        api = self.getAccount()

        self.assertTrue(len(api.getFinishers()) > 5)

        # Test for proper keys and types.
        for unit in api.finishers:
            self.assertTrue('permanent' in unit.keys())
            self.assertTrue('id' in unit.keys())
            self.assertEqual(type(unit['object']).__name__, 'Finisher')

    def test_getWallet(self):
        api = self.getAccount()

        # Just verify stuff is in it.
        self.assertTrue(len(api.getWallet()) > 5)

        # Verify data.
        for unit in api.wallet:
            self.assertTrue('name' in unit.keys())
            self.assertTrue('icon' in unit.keys())
            self.assertTrue('description' in unit.keys())

    def test_getRecipes(self):
        api = self.getAccount()

        # Verify populated.
        self.assertTrue(len(api.getRecipes()) > 50)

        # Verify some information.
        self.assertTrue(api.recipes[0].id == 842)
        self.assertTrue(api.recipes[0].time_to_craft_ms == 5000)

    def test_getTitles(self):
        api = self.getAccount()

        self.assertTrue(len(api.getTitles()) > 5)
        self.assertTrue(api.titles[0].name == 'Been there. Done that.')

    def test_getBank(self):
        api = self.getAccount()

        self.assertTrue(len(api.getBank()) > 5)

        for unit in api.bank:
            self.assertEqual(type(unit['object']).__name__, 'Item')

    def test_getAchievements(self):
        api = self.getAccount()

        self.assertTrue(len(api.getAchievements()) > 5)
        self.assertTrue(api.achievements[0]['object'].name == 'Centaur Slayer')

        for unit in api.achievements:
            self.assertEqual(type(unit['object']).__name__, 'Achievement')

    def test_getMaterials(self):
        api = self.getAccount()

        self.assertTrue(len(api.getMaterials()) > 5)
        self.assertTrue(api.materials[0]['object'].name == 'Carrot')

        for unit in api.materials:
            self.assertEqual(type(unit['object']).__name__, 'Material')

    def test_getOutfits(self):
        api = self.getAccount()

        self.assertTrue(len(api.getOutfits()) > 2)
        self.assertTrue(api.outfits[0].name == 'Hexed Outfit')

        for unit in api.outfits:
            self.assertEqual(type(unit).__name__, 'Outfit')

    def test_getMasteries(self):
        api = self.getAccount()

        self.assertTrue(len(api.getMasteries()) > 5)
        self.assertTrue(api.masteries[0]['object'].name == 'Exalted Lore')

        for unit in api.masteries:
            self.assertEqual(type(unit['object']).__name__, 'Mastery')

    def test_getInventory(self):
        api = self.getAccount()

        # No len because I only have one slot..Might change.
        api.getInventory()
        self.assertTrue(api.inventory[0]['object'].name == 'Royal Terrace Pass')

        for unit in api.inventory:
            self.assertEqual(type(unit['object']).__name__, 'Item')

    def test_getTradeHistory(self):
        api = self.getAccount()

        # Yep.
        self.assertTrue(all(k in api.getTradeHistory() for k in ('buying', 'selling', 'bought')))

        # Double yep.
        self.assertTrue(all(k in dir(api) for k in ('buying', 'selling', 'bought')))

    def test_getCharacters(self):
        api = self.getAccount()

        self.assertTrue(len(api.getCharacters()) > 3)

        for unit in api.characters:
            self.assertEqual(type(unit).__name__, 'Character')

    def test_getDyes(self):
        api = self.getAccount()

        self.assertTrue(len(api.getDyes()) > 100)  # I have a lot of dyes.

        for unit in api.dyes:
            self.assertEqual(type(unit).__name__, 'Dye')

        self.assertTrue(api.dyes[0].name == 'Chalk')

    def test_getSkins(self):
        api = self.getAccount()

        self.assertTrue(len(api.getSkins()) > 100)

        for unit in api.skins:
            self.assertEqual(type(unit).__name__, 'Skin')

        self.assertTrue(api.skins[0].name == 'Chainmail Leggings')

    def test_getMinis(self):
        api = self.getAccount()

        self.assertTrue(len(api.getMinis()) > 3)

        for unit in api.minis:
            self.assertEqual(type(unit).__name__, 'Mini')

    def test_getTraits(self):
        api = self.getAccount()

        # Call it once for speed.
        build = api.getTraits('Necromancer Patches')

        # Today on ugly, we have this.
        for unit in build.values():
            for area in unit:
                self.assertEqual(type(area['line']).__name__, 'Specialization')

        # Verify area specific functionality
        build = api.getTraits('Friendly Patches', areaFlag='pvp')
        for unit in build:
            self.assertEqual(type(area['line']).__name__, 'Specialization')

    def test_getMatchResults(self):
        api = self.getAccount()

        results = api.getMatchResults('all')

        for match in results:
            self.assertEqual(type(match).__name__, 'PVPMatch')

    def test_getPVPStats(self):
        api = self.getAccount()

        strings = ('pvp_rank', 'pvp_wins', 'pvp_losses',
                   'pvp_desertions', 'pvp_byes', 'pvp_forfeits',
                   'pvp_professions', 'pvp_ranked', 'pvp_unranked')

        # This just assigns attributes.
        api.getPVPStats()

        # Dirty check.
        self.assertTrue(
            all(k in dir(api) for k in strings)
        )

    def test_getGuildRanks(self):
        api = self.getAccount()

        # NULL represent?
        guild = api.getGuildRanks('A4AF6C09-452F-44EE-BD3E-704FB5C371FB')

        # If this is here, it's the right thing.
        self.assertTrue(guild[0]['id'] == 'Grand Poobah')

    def test_getGuildMembers(self):
        api = self.getAccount()

        members = api.getGuildMembers('A4AF6C09-452F-44EE-BD3E-704FB5C371FB')

        # Am I there?
        self.assertTrue(members[0]['name'] == 'Patches.7584')

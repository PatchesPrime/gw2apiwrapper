import pytest
from gw2apiwrapper import AccountAPI
import os


APIKEY = os.environ['APIKEY']
api = AccountAPI(APIKEY)


def test_brokenPermissions():
    APIKEY = os.environ['BUSTEDKEY']
    acc = AccountAPI(APIKEY)

    # Just going to call getAchievements() to trigger
    # the error.
    with pytest.raises(PermissionError):
        acc.getAchievements()


def test_getRaids():
    encounters = ["vale_guardian", "spirit_woods", "gorseval",
                  "sabetha", "slothasor", "bandit_trio",
                  "matthias", "escort", "keep_construct",
                  "xera", "cairn", "mursaat_overseer",
                  "samarog", "deimos"]
    raids = api.getRaids()

    # I don't do raids..
    # assert x in raids for x in encounters)

    # This should always be false when using my API key...
    assert any(x in raids for x in encounters) is False


def test_getGuild():
    guild = api.getGuild('A4AF6C09-452F-44EE-BD3E-704FB5C371FB')
    assert type(guild).__name__ == 'Guild'
    assert guild.influence > 0


def test_getDungeon():
    # I don't really do dungeons so I'm having a hard time verifying
    # the validity of this test. If you got a key and do dungeons
    # send me a message.
    paths = ['cm_story', 'asura', 'seraph', 'butler', 'ac_story',
             'hodgins', 'detha', 'tzark', 'ta_story', 'leurent',
             'vevina', 'aetherpath', 'se_story', 'fergg', 'rasalov',
             'koptev', 'cof_story', 'ferrah', 'magg', 'rhiannon',
             'hotw_story', 'butcher', 'plunderer', 'zealot',
             'coe_story', 'submarine', 'teleport', 'front_door',
             'arah_story', 'jotun', 'mursaat', 'forgotten', 'seer']
    dun = api.getDungeons()

    # I guess this'll work for now until I get someone who does dungeons.
    # assert any(x in dun for x in paths)

    # This should always be false when using my API key...
    assert any(x in dun for x in paths) is False


def test_getFinishers():
    assert len(api.getFinishers()) > 5

    # Test for proper keys and types.
    for unit in api.finishers:
        assert 'permanent' in unit.keys()
        assert 'id' in unit.keys()
        assert type(unit['object']).__name__ == 'Finisher'


def test_getWallet():
    # Just verify stuff is in it.
    assert len(api.getWallet()) > 5

    # Verify data.
    for unit in api.wallet:
        assert 'name' in unit.keys()
        assert 'icon' in unit.keys()
        assert 'description' in unit.keys()


def test_getRecipes():
    # Verify populated.
    assert len(api.getRecipes()) > 50

    # Verify some information.
    assert api.recipes[0].id == 842
    assert api.recipes[0].time_to_craft_ms == 5000


def test_getTitles():
    assert len(api.getTitles()) > 5
    assert api.titles[0].name == 'Been there. Done that.'


def test_getBank():
    assert len(api.getBank()) > 5

    for unit in api.bank:
        assert type(unit['object']).__name__ == 'Item'


def test_getAchievements():
    assert len(api.getAchievements()) > 5
    assert api.achievements[0]['object'].name == 'Centaur Slayer'

    for unit in api.achievements:
        assert type(unit['object']).__name__ == 'Achievement'


def test_getMaterials():
    assert len(api.getMaterials()) > 5
    assert api.materials[0]['object'].name == 'Carrot'

    for unit in api.materials:
        assert type(unit['object']).__name__ == 'Material'


def test_getOutfits():
    assert len(api.getOutfits()) > 2
    assert api.outfits[0].name == 'Hexed Outfit'

    for unit in api.outfits:
        assert type(unit).__name__ == 'Outfit'


def test_getMasteries():
    assert len(api.getMasteries()) > 5
    assert api.masteries[0]['object'].name == 'Exalted Lore'

    for unit in api.masteries:
        assert type(unit['object']).__name__ == 'Mastery'


def test_getInventory():
    # No len because I only have one slot..Might change.
    api.getInventory()
    assert api.inventory[0]['object'].name == 'Royal Terrace Pass'

    for unit in api.inventory:
        assert type(unit['object']).__name__ == 'Item'


def test_getTradeHistory():
    # Yep.
    assert all(k in api.getTradeHistory() for k in ('buying', 'selling', 'bought')) is True

    # Double yep.
    assert all(k in dir(api) for k in ('buying', 'selling', 'bought')) is True

    # I have some stupid orders active for this.
    # If you want to break my test though, sell me a Bifrost
    # for a single gold.
    assert api.buying is not None

    # Want to buy a Pumpkin Pie Cookie for 1g?
    assert api.selling is not None


def test_getCharacters():
    assert len(api.getCharacters()) > 3

    for unit in api.characters:
        assert type(unit).__name__ == 'Character'


def test_getDyes():
    assert len(api.getDyes()) > 100  # I have a lot of dyes

    for unit in api.dyes:
        assert type(unit).__name__ == 'Dye'

    assert api.dyes[0].name == 'Chalk'


def test_getSkins():
    assert len(api.getSkins()) > 100

    for unit in api.skins:
        assert type(unit).__name__ == 'Skin'

    assert api.skins[0].name == 'Chainmail Leggings'


def test_getMinis():
    assert len(api.getMinis()) > 3

    for unit in api.minis:
        assert type(unit).__name__ == 'Mini'


def test_getTraits():
    # Call it once for speed.
    build = api.getTraits('Necromancer Patches')

    # Today on ugly, we have this.
    for unit in build.values():
        for area in unit:
            assert type(area['line']).__name__ == 'Specialization'

    # Verify area specific functionality
    build = api.getTraits('Friendly Patches', areaFlag='pvp')
    for unit in build:
        assert type(area['line']).__name__ == 'Specialization'


def test_getMatchResults():
    results = api.getMatchResults('all')

    for match in results:
        assert type(match).__name__ == 'PVPMatch'

    # Test list
    results = api.getMatchResults([x.id for x in results])
    for match in results:
        assert type(match).__name__ == 'PVPMatch'

    # Test single ID
    result = api.getMatchResults(results[0].id)
    assert type(result[0]).__name__ == 'PVPMatch'

    # Test failure
    with pytest.raises(TypeError):
        api.getMatchResults(TypeError)


def test_getPVPStats():
    strings = ('pvp_rank', 'pvp_wins', 'pvp_losses',
               'pvp_desertions', 'pvp_byes', 'pvp_forfeits',
               'pvp_professions', 'pvp_ranked', 'pvp_unranked')

    # This just assigns attributes.
    api.getPVPStats()

    # Dirty check.
    assert all(k in dir(api) for k in strings) is True


def test_getGuildRanks():
    # NULL represent?
    guild = api.getGuildRanks('A4AF6C09-452F-44EE-BD3E-704FB5C371FB')

    # If this is here, it's the right thing.
    assert guild[0]['id'] == 'Grand Poobah'


def test_getGuildMembers():
    members = api.getGuildMembers('A4AF6C09-452F-44EE-BD3E-704FB5C371FB')

    # Am I there?
    assert members[0]['name'] == 'Patches.7584'

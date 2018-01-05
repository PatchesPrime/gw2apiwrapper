import pytest
from gw2apiwrapper import GlobalAPI

# This object retains nothing, so it's fine for it
# to be reused.
gAPI = GlobalAPI()


def test_getMaterialCategories():
    material = gAPI.getMaterialCategories(38)
    assert type(material).__name__ == 'MaterialCategory'
    assert material.id == 38
    assert material.name == 'Festive Materials'
    assert all(x in material.items for x in [36060, 36061])


def test_getItemStats():
    itemstat = gAPI.getItemStats(1011)
    assert type(itemstat).__name__ == 'ItemStat'
    assert itemstat.id == 1011
    assert itemstat.name == 'Forsaken'
    assert 0.35 and 0.25 in itemstat.attributes.values()

    # str test
    itemstat = gAPI.getItemStats('1012')
    assert type(itemstat).__name__ == 'ItemStat'
    assert itemstat.id == 1012
    assert itemstat.name == 'Apostate\'s'
    assert 0.35 and 0.25 in itemstat.attributes.values()

    # list test
    itemstat = gAPI.getItemStats([1011, '1012'])
    for stat in itemstat:
        assert type(stat).__name__ == 'ItemStat'


def test_getRaid():
    raid = gAPI.getRaid('forsaken_thicket')
    assert type(raid).__name__ == 'Raid'
    assert raid.id == 'forsaken_thicket'


def test_getGuild():
    guild = gAPI.getGuild('116E0C0E-0035-44A9-BB22-4AE3E23127E5')
    assert type(guild).__name__ == 'Guild'
    assert guild.name == 'Edit Conflict'


def test_getDungeon():
    dungeon = gAPI.getDungeon('caudecus_manor')
    assert type(dungeon).__name__ == 'Dungeon'
    assert dungeon.paths[1]['id'] == 'asura'


def test_getSkill():
    # Test int()
    skill = gAPI.getSkill(14375)
    assert type(skill).__name__ == 'Skill'
    assert skill.name == 'Arcing Slice'

    # Test str()
    skill = gAPI.getSkill('5516')
    assert type(skill).__name__ == 'Skill'
    assert skill.name == 'Conjure Fiery Greatsword'

    # Test list()
    for unit in gAPI.getSkill([5516, 5517, '14375']):
        assert type(unit).__name__ == 'Skill'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getSkill({14375})


def test_getLegend():
    legend = gAPI.getLegend('Legend2')

    assert type(legend).__name__ == 'Legend'
    assert legend.heal == 26937

    # Test all
    assert len(gAPI.getLegend('all')) > 3


def test_getFinisher():
    # Test int()
    # I know for a fact finisher id 12 has an unlock item.
    finisher = gAPI.getFinisher(12)

    assert type(finisher).__name__ == 'Finisher'
    assert finisher.name == 'Whump the Giant Finisher'

    # Test str()
    # Finisher id 1 does not have a finisher item.
    finisher = gAPI.getFinisher('1')
    assert type(finisher).__name__ == 'Finisher'
    assert finisher.name == 'Rabbit Rank Finisher'

    # Test list()
    for unit in gAPI.getFinisher([1, 12]):
        assert type(unit).__name__ == 'Finisher'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getFinisher({1})

    # Test all
    assert len(gAPI.getFinisher('all')) > 10


def test_getTitle():
    # Test int()
    title = gAPI.getTitle(8)
    assert type(title).__name__ == 'Title'
    assert title.name == 'Flameseeker'
    assert title.achievement == 118

    # Test str()
    title = gAPI.getTitle('8')
    assert type(title).__name__ == 'Title'
    assert title.name == 'Flameseeker'
    assert title.achievement == 118

    # Test list()
    for unit in gAPI.getTitle([8, 9]):
        assert type(unit).__name__ == 'Title'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getTitle({8})

    # Test all
    assert len(gAPI.getTitle('all')) > 20


def test_getOutfit():
    # Test int()
    outfit = gAPI.getOutfit(8)
    assert type(outfit).__name__ == 'Outfit'
    assert outfit.name == 'Shadow Assassin Outfit'
    assert outfit.unlock_items[0] == 66658

    # Test str()
    outfit = gAPI.getOutfit('10')
    assert type(outfit).__name__ == 'Outfit'
    assert outfit.name == 'Ceremonial Plated Outfit'
    assert outfit.unlock_items[0] == 67040

    # Test list()
    for unit in gAPI.getOutfit([8, 10]):
        assert type(outfit).__name__ == 'Outfit'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getOutfit({8})

    # Test all
    assert len(gAPI.getOutfit('all')) > 20


def test_getMasteries():
    # Test int()
    mastery = gAPI.getMasteries(1)
    assert type(mastery).__name__ == 'Mastery'
    assert mastery.region == 'Maguuma'

    # Test str()
    mastery = gAPI.getMasteries('2')
    assert type(mastery).__name__ == 'Mastery'
    assert mastery.region == 'Maguuma'

    # Test list()
    for unit in gAPI.getMasteries([8, 10]):
        assert type(mastery).__name__ == 'Mastery'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getMasteries({1})

    # Test all
    assert len(gAPI.getMasteries('all')) > 10


def test_getPet():
    # Test int()
    pet = gAPI.getPet(33)
    assert type(pet).__name__ == 'Pet'
    assert pet.name == 'Juvenile Forest Spider'

    # Test str()
    pet = gAPI.getPet('42')
    assert type(pet).__name__ == 'Pet'
    assert pet.name == 'Juvenile Red Jellyfish'

    # Test list()
    for unit in gAPI.getPet([33, 42]):
        assert type(pet).__name__ == 'Pet'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getPet({42})

    # Test all
    assert len(gAPI.getPet('all')) > 20


def test_getRace():
    # This works a bit different.
    race = gAPI.getRace('Asura')
    assert type(race).__name__ == 'Race'

    # Check its skills.
    assert len(race.skills) == 7

    # Test all
    assert len(gAPI.getRace('all')) > 3


def test_getProfession():
    # Same thing. Different input.
    prof = gAPI.getProfession('Engineer')
    assert type(prof).__name__ == 'Profession'


def test_getGuildUpgrade():
    upgrade = gAPI.getGuildUpgrade(55)
    assert type(upgrade).__name__ == 'GuildUpgrade'
    assert upgrade.name == 'Guild Treasure Trove'

    assert 58 in upgrade.prerequisites

    # Test all
    assert len(gAPI.getGuildUpgrade('all')) > 20


def test_getGuildPermission():
    perm = gAPI.getGuildPermission('Admin')
    assert type(perm).__name__ == 'GuildPermission'
    assert perm.name == 'Admin Lower Ranks.'

    # Test all
    assert len(gAPI.getGuildPermission('all')) > 20


def test_getAchievement():
    # Test int()
    achieve = gAPI.getAchievement(1840)
    assert type(achieve).__name__ == 'Achievement'
    assert achieve.name == 'Daily Completionist'

    # Test str()
    achieve = gAPI.getAchievement('910')
    assert type(achieve).__name__ == 'Achievement'
    assert achieve.name == 'Tequatl the Sunless'

    # Test list()
    for unit in gAPI.getAchievement([1840, 910, 2258]):
        assert type(achieve).__name__ == 'Achievement'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getAchievement({910})


def test_getAchievementGroup():
    # Weird IDs.
    ag = gAPI.getAchievementGroup('65B4B678-607E-4D97-B458-076C3E96A810')
    assert type(ag).__name__ == 'AchievementGroup'
    assert ag.name == 'Heart of Thorns'

    # Test all
    assert len(gAPI.getAchievementGroup('all')) > 5


def test_getAchievementCategory():
    # Test int()
    ac = gAPI.getAchievementCategory(1)
    assert type(ac).__name__ == 'AchievementCategory'
    assert ac.name == 'Slayer'

    # Test str()
    ac = gAPI.getAchievementCategory('2')
    assert type(ac).__name__ == 'AchievementCategory'
    assert ac.name == 'Hero'

    # Test list()
    for unit in gAPI.getAchievementCategory([1, 2]):
        assert type(unit).__name__ == 'AchievementCategory'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getAchievementCategory({1})

    # Test all
    assert len(gAPI.getAchievementCategory('all')) > 20


def test_getSkin():
    # Test int()
    skin = gAPI.getSkin(10)
    assert type(skin).__name__ == 'Skin'
    assert skin.name == 'Seer Pants'

    # Test str()
    skin = gAPI.getSkin('1')
    assert type(skin).__name__ == 'Skin'
    assert skin.name == 'Chainmail Leggings'

    # Test list()
    for unit in gAPI.getSkin([1, 2]):
        assert type(skin).__name__ == 'Skin'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getSkin({10})


def test_getItem():
    # Test int()
    item = gAPI.getItem(28445)
    assert type(item).__name__ == 'Item'
    assert item.name == 'Strong Soft Wood Longbow of Fire'

    # Test str()
    item = gAPI.getItem('12452')
    assert type(item).__name__ == 'Item'
    assert item.name == 'Omnomberry Bar'

    # Test list()
    gAPI.getItem([1])
    for unit in gAPI.getItem([1, 2]):
        assert type(unit).__name__ == 'Item'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getItem({28445})


def test_getDye():
    # Test int()
    dye = gAPI.getDye(10)
    assert type(dye).__name__ == 'Dye'
    assert dye.name == 'Sky'

    # Test str()
    dye = gAPI.getDye('11')
    assert type(dye).__name__ == 'Dye'
    assert dye.name == 'Starry Night'

    # Test list()
    for unit in gAPI.getDye([1, 2]):
        assert type(dye).__name__ == 'Dye'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getDye({10})


def test_getRecipe():
    # Test int()
    recipe = gAPI.getRecipe(7319)
    assert type(recipe).__name__ == 'Recipe'
    assert recipe.output_item_id == 46742

    # Test str()
    recipe = gAPI.getRecipe('7419')
    assert type(recipe).__name__ == 'Recipe'
    assert recipe.output_item_id == 46944

    # Test list()
    for unit in gAPI.getRecipe([1, 2]):
        assert type(recipe).__name__ == 'Recipe'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getRecipe({7319})


def test_getMini():
    # Test int()
    mini = gAPI.getMini(1)
    assert type(mini).__name__ == 'Mini'
    assert mini.name == 'Miniature Rytlock'

    # Test str()
    mini = gAPI.getMini('2')
    assert type(mini).__name__ == 'Mini'
    assert mini.name == 'Miniature Servitor Golem'

    # Test list()
    for unit in gAPI.getMini([1, 2]):
        assert type(mini).__name__ == 'Mini'

    # Test unsupported type
    with pytest.raises(NotImplementedError):
        gAPI.getMini({2})


def test_getWVWObjective():
    wvwobjid = gAPI.getWVWObjective('all')
    assert len(wvwobjid) > 100

    # Test for list functionality.
    wvwids = [x.id for x in wvwobjid]
    wvwobjid = gAPI.getWVWObjective(wvwids)

    wvwobjid = gAPI.getWVWObjective(wvwids[0])
    assert type(wvwobjid).__name__ == 'WVWObjective'


def test_getWVWMatches():
    wvwmatches = gAPI.getWVWMatches('all')
    assert len(wvwmatches) > 5

    # Test list functionality.
    matchIDs = [x.id for x in wvwmatches]
    wvwmatches = gAPI.getWVWMatches(matchIDs)

    # Test specific ID
    wvwmatch = gAPI.getWVWMatches(matchIDs[0])
    assert type(wvwmatch).__name__ == 'WVWMatch'

    for unit in wvwmatches:
        assert type(unit).__name__ == 'WVWMatch'


def test_getDailies():
    dailies = gAPI.getDailies()
    assert len(dailies) > 10

    dailies = gAPI.getDailies(tomorrow=True)

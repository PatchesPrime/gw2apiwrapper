import pytest
import os
from gw2apiwrapper import functions, AccountAPI


def test_badUrl():
    api = AccountAPI(os.environ['APIKEY'])

    # Test bad ID
    with pytest.raises(ValueError):
        api.getGuild('ERROR')

    # Test for invalid permission exception
    with pytest.raises(TypeError):
        api = AccountAPI('NOT A REAL KEY')


def test_getGuildID():
    test = functions.getGuildID('Edit Conflict')

    assert test == '116E0C0E-0035-44A9-BB22-4AE3E23127E5'


def test_getBuild():
    assert type(functions.getBuild()) is int


def test_getAssets():
    assets = functions.getAssets()

    assert type(assets) is list

    for thing in assets:
        assert type(thing) is dict
        assert len(thing.keys()) == 2


def test_isMaterial():
    assert functions.isMaterial(12134) is True
    assert len(functions.isMaterial([12134, 24876, 12])) == 2

    assert functions.isMaterial(12) is False


def test_recipeSearch():
    search = functions.recipeSearch('input', 46731)

    assert len(search) > 5
    assert 7314 in search

    with pytest.raises(ValueError):
        functions.recipeSearch('Failure', 46731)


def test_getWorldName():
    world = functions.getWorldName(1001)

    assert type(world) is list
    assert len(world[0]) >= 3

    # Test list

    worlds = functions.getWorldName([1001, 1002])

    assert type(worlds) is list

    for world in worlds:
        assert type(world) is dict
        assert len(world) >= 3


def test_getEmblem():
    fg = functions.getEmblem(1, layer='fg')

    assert type(fg) is list
    assert len(fg[0]) >= 2
    assert len(fg[0]['layers']) == 3

    # Get both fg and bg
    getEm = functions.getEmblem(1)

    assert type(getEm) is list

    for layer in getEm:
        assert type(layer) is dict
        assert len(layer) >= 2

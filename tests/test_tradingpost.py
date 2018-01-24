import pytest
from gw2apiwrapper.tradingpost import GW2TP

# Our Object for interacting with TP
tp = GW2TP()


def test_getListings():
    # Test single ID
    listings = tp.getListings(19684)

    assert type(listings).__name__ == 'TPListing'
    assert listings.id == 19684
    assert 'buys', 'sells' in listings.keys()
    assert len(listings.buys) > 0
    assert len(listings.sells) > 0

    # Test list of IDs
    listings = tp.getListings([19684, 19709])

    assert type(listings) is list

    for item in listings:
        assert type(item).__name__ == 'TPListing'
        assert len(item.buys) > 0
        assert len(item.sells) > 0


def test_getPrices():
    prices = tp.getPrices(19684)

    assert type(prices).__name__ == 'TPPrice'
    assert prices.id == 19684
    assert prices.whitelisted is False

    assert len(prices.buys) > 0
    assert len(prices.sells) > 0

    prices = tp.getPrices([19684, 19709])

    for item in prices:
        assert type(item).__name__ == 'TPPrice'
        assert len(item.buys) > 0
        assert len(item.sells) > 0


def test_getExchange():
    exchange = tp.getExchange('coin', 100000)

    assert type(exchange) is dict
    assert len(exchange.keys()) == 2

    with pytest.raises(ValueError):
        tp.getExchange('error', 100000)

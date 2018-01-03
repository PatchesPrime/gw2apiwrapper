gw2apiwrapper |Build Status| |Coverage Status| |Requirements Status|
=====================================================================

Object Orientated GW2 API Wrapper

**2017-12-31 - Most of the refactor is done..most..**

Being dissatisfied with the current implementations of the Guild Wars 2
API written in python, I began this project.

It will eventually (as it’s released) implement all of the GW2 v2 API.

To install, you can use PyPi:

.. code:: bash

    pip install gw2apiwrapper

Then import it.

Example:

.. code:: python

    from gw2apiwrapper import AccountAPI, GlobalAPI

    # Get an account based object. Requires API Key.
    personal = AccountAPI("<APIKEY>")

    # Get a 'Global' api object. (Non-authed)
    workHorse = GlobalAPI()

    # This is iterable, as not only does it fill the personal.bank
    # attribute, it also returns that information.
    personal.getBank()

    bankIDs = [slot['id'] for slot in personal.bank if slot is not None]

    # GlobalAPI's getItem can take different types, all documented.
    itemObjects = workHorse.getItem(bankIDs)

    # Get the names of all items in bank.
    for item in itemObjects:
      print(item.name)

.. |Build Status| image:: https://travis-ci.org/PatchesPrime/gw2apiwrapper.svg?branch=master
   :target: https://travis-ci.org/PatchesPrime/gw2apiwrapper
.. |Coverage Status| image:: https://coveralls.io/repos/github/PatchesPrime/gw2apiwrapper/badge.svg?branch=master
   :target: https://coveralls.io/github/PatchesPrime/gw2apiwrapper?branch=master
.. |Requirements Status| image:: https://requires.io/github/PatchesPrime/gw2apiwrapper/requirements.svg?branch=master
   :target: https://requires.io/github/PatchesPrime/gw2apiwrapper/requirements/?branch=master

gw2apiwrapper |Build Status| |Coverage Status| |Requirements Status|
=====================================================================

gw2apiwrapper is a Python library designed to abstract away the overhead and complexity of interacting with the official Guild Wars 2 (GW2) API via Python.

The library aims to make it easy to write and read Python applications and tools with only a minimal knowledge of the GW2 API itself.

This is accomplished by abstracting away the standard JSON->dictionary mapping scheme that is so commonly used and replace it with an OOP-style (eg. item.name) notation.


Installation
------------
Simply install with pip/pipenv and you're good to go:

.. code:: bash

    pip install gw2apiwrapper


Example
-------

.. code:: python

    from gw2apiwrapper import AccountAPI, GlobalAPI

    # Get an account based object. Requires API Key.
    personal = AccountAPI("<APIKEY>")

    # Get a 'Global' api object. (Non-authed)
    workHorse = GlobalAPI()

    # This is iterable, as not only does it fill the personal.bank
    # attribute, it also returns that information allowing it to be
    # used in loops..even though we don't here.
    personal.getBank()

    # Should be self documenting, but demonstrates that the previous
    # getBank() call actually populated that object's 'bank' attribute.
    bankIDs = [slot['id'] for slot in personal.bank if slot is not None]

    # GlobalAPI's getItem can take different types, all documented.
    itemObjects = workHorse.getItem(bankIDs)

    # Get the names of all items in bank.
    for item in itemObjects:
      print(item.name)


NOTES
-----
This project is in semi-active development. The groundwork is laid, and most of the API is accounted for. If something you need is missing and you'd like it added feel free to open an issue (or a pull request!) on GitHub.


.. |Build Status| image:: https://travis-ci.org/PatchesPrime/gw2apiwrapper.svg?branch=master
   :target: https://travis-ci.org/PatchesPrime/gw2apiwrapper
.. |Coverage Status| image:: https://coveralls.io/repos/github/PatchesPrime/gw2apiwrapper/badge.svg?branch=master
   :target: https://coveralls.io/github/PatchesPrime/gw2apiwrapper?branch=master
.. |Requirements Status| image:: https://requires.io/github/PatchesPrime/gw2apiwrapper/requirements.svg?branch=master
   :target: https://requires.io/github/PatchesPrime/gw2apiwrapper/requirements/?branch=master

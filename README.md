# GW2API
Object Orientated GW2 API Wrapper

**This project is under heavy development and is not complete.**

Being dissatisfied with the current implementations of the Guild Wars 2 API written in python, I began this project.

It will eventually (as it's released) implement all of the GW2 v2 API.

Example:
``` python
import GW2API

# Get an account based object. Requires API Key.
personal = GW2API.AccountAPI("<APIKEY>")

# Get a 'Global' api object. (Non-authed)
workHorse = GW2API.GlobalAPI()

# This is iterable, as not only does it fill the personal.bank
# attribute, it also returns that information.
personal.getBank()

bankIDs = [slot['id'] for slot in personal.bank if slot is not None]

# GlobalAPI's getItem can take different types, all documented.
itemObjects = workHorse.getItem(bankIDs)

# Get the names of all items in bank.
for item in itemObjects:
  print(item.name)

```

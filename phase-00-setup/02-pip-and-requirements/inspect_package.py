from importlib.metadata import version, requires

import requests

print("requests version :", version("requests"))
print("loaded from      :", requests.__file__)

print("depends on       :")
for requirement in requires("requests"):
    if "extra ==" not in requirement:
        print("   -", requirement)

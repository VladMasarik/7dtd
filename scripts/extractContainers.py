from xml.dom.minidom import parse
import xml.dom.minidom



"""
This is a reST style.

:param param1: this is a first param
:param param2: this is a second param
:returns: this is a description of what is returned
:raises keyError: raises an exception
"""

blocks = "config/blocks.xml"
localization = "config/localization.txt"
loot = "config/loot.xml"


lootContainers = xml.dom.minidom.parse(blocks).documentElement.getElementsByTagName("lootcontainer")
lootGroups = xml.dom.minidom.parse(loot).documentElement.getElementsByTagName("lootgroup")

def buildJSON(lootContainers):
    result = {}
    for group in lootContainers:
        name = group.getAttribute("name")
        id = group.getAttribute("id")
        itemsAndGroups = group.getElementsByTagName("item")

        items = getItemNames(itemsAndGroups)
        childGroups = getGroupNames(itemsAndGroups)
        allItems = getItemsRecursive(group)
        allItems = list(set(allItems)) # Get rid of duplicates

        result[name] = {
            "id": id,
            "items": items,
            "groups": childGroups,
            "allItems": allItems
        }
    return result


buildJSON(lootContainers)

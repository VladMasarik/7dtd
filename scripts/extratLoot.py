from xml.dom.minidom import parse
import xml.dom.minidom
import csv



"""
This is a reST style.

:param param1: this is a first param
:param param2: this is a second param
:returns: this is a description of what is returned
:raises keyError: raises an exception
"""

blocks = "config/blocks.xml"
localization = "config/Localization.txt"
loot = "config/loot.xml"


lootContainers = xml.dom.minidom.parse(loot).documentElement.getElementsByTagName("lootcontainer")
lootGroups = xml.dom.minidom.parse(loot).documentElement.getElementsByTagName("lootgroup")
blocks = xml.dom.minidom.parse(blocks).documentElement.getElementsByTagName("block")

def getItemNames(itemsAndGroups):
    """
    :param itemsAndGroups: list of XML elements in a lootgroup
    :returns: list of strings for just items
    """
    itemNames = list()
    for element in itemsAndGroups:
        if element.hasAttribute("name"):
            itemNames.append(element.getAttribute("name"))
    return itemNames


def getGroupNames(itemsAndGroups):
    """
    :param itemsAndGroups: list of XML elements in a lootgroup
    :returns: list of group name strings
    """
    groupNames = list()
    for element in itemsAndGroups:
        if element.hasAttribute("group"):
            groupNames.append(element.getAttribute("group"))
    return groupNames


def getItemsRecursive(group):
    """
    Flattens all of the groups, and returns just the items within the group.

    :param group: XML group element
    :returns: list of item names extracted from all the groups inside the given group + items of the given group
    """
    itemsAndGroups = group.getElementsByTagName("item")
    gg = group.getAttribute("name")

    items = getItemNames(itemsAndGroups) # items of the group
    childItems = list()

    childGroups = getGroupNames(itemsAndGroups)
    for groupName in childGroups:
        childItems = childItems + getItemsRecursive(findXMLGroup(groupName)) # all items of the child groups
    return items + childItems



def findXMLGroup(groupName):
    """
    :param groupName: name of the group
    :returns: group XML element
    """
    for group in lootGroups:
        if group.getAttribute("name") == groupName:
            return group
        


def buildJSONContainers(lootContainers):
    result = {}
    for group in lootContainers:
        id = group.getAttribute("id")
        itemsAndGroups = group.getElementsByTagName("item")

        items = getItemNames(itemsAndGroups)
        childGroups = getGroupNames(itemsAndGroups)
        allItems = getItemsRecursive(group)
        allItems = list(set(allItems)) # Get rid of duplicates

        result[id] = {
            "items": items,
            "groups": childGroups,
            "allItems": allItems
        }
    return result


def buildJSONLootGroups(lootGroups):
    result = {}
    for group in lootGroups:
        name = group.getAttribute("name")
        itemsAndGroups = group.getElementsByTagName("item")

        items = getItemNames(itemsAndGroups)
        childGroups = getGroupNames(itemsAndGroups)
        allItems = getItemsRecursive(group)
        allItems = list(set(allItems)) # Get rid of duplicates

        result[name] = {
            "items": items,
            "groups": childGroups,
            "allItems": allItems
        }
    return result



def buildJSONBlocks(blocks):
    result = {}
    for block in blocks:
        name = block.getAttribute("name")
        blockContents = getLootPerBlock(block)
        if blockContents is None:
            continue
        else:
            result[name] = blockContents.copy() # We cant use the same object, as we are later adding human readable names to all of them
    return result


def getLootPerBlock(block):
    """
    :param groupName: block XML element
    :returns: dictionary of what loot belongs to this block
    """
    id = None
    properties = block.getElementsByTagName("property")
    for element in properties:
        if element.getAttribute("name") == "LootList":
            id = element.getAttribute("value")
            return containers[id]
    return None






allGroups = buildJSONLootGroups(lootGroups)

containers = buildJSONContainers(lootContainers)

blocks = buildJSONBlocks(blocks)



with open(localization,'r') as f: # input csv file
    reader = csv.DictReader(f, delimiter=',') # Key,File,Type,UsedInMainMenu,NoTranslate,english,
    keys = blocks.keys()
    for row in reader:
        if row["Key"] in keys:
            blocks[row["Key"]]["humanName"] = row["english"]


x = 1

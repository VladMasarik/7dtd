from xml.dom.minidom import parse
import xml.dom.minidom
import csv
import json


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

extractedContainersFile = "extractedLoot/containers.json"
extractedBlocksFile = "extractedLoot/blocks.json"
extractedItemsFile = "extractedLoot/items.json"


lootContainers = xml.dom.minidom.parse(loot).documentElement.getElementsByTagName("lootcontainer")
lootGroups = xml.dom.minidom.parse(loot).documentElement.getElementsByTagName("lootgroup")
blocks = xml.dom.minidom.parse(blocks).documentElement.getElementsByTagName("block")


def getHumanNames():
    """
    :returns: Dictionary of names and human readable names; names being object names used in the developers code
    """
    names = {}
    with open(localization,'r') as f: # input csv file
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            names[row["Key"]] = row["english"]
    return names

def getItemNames(itemsAndGroups):
    """
    :param itemsAndGroups: list of XML elements in a lootgroup
    :returns: list of strings for just items
    """
    itemNames = {}
    for element in itemsAndGroups:
        if element.hasAttribute("name"):
            if element.getAttribute("name") in humanNames.keys():
                itemNames[element.getAttribute("name")] = humanNames[element.getAttribute("name")]
            else:
                print("The following item doesn't have a human readable name:", element.getAttribute("name")) # These are usually Development items
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
    Flattens all of the groups, and returns just the items within the group. Meaning that if the lootContainer has a tree strucutre of what it containes, with Items being the leafs, and nodes being lootGroups, we try to extract only the items.

    :param group: XML group element
    :returns: list of item names extracted from all the groups inside the given group + items of the given group
    """
    itemsAndGroups = group.getElementsByTagName("item")
    gg = group.getAttribute("name")

    items = getItemNames(itemsAndGroups) # items of the group

    childGroups = getGroupNames(itemsAndGroups)
    for groupName in childGroups:
        childItems = getItemsRecursive(findXMLGroup(groupName))
        items.update(childItems) # all items of the child groups
    return items



def findXMLGroup(groupName):
    """
    :param groupName: name of the group
    :returns: group XML element
    """
    for group in lootGroups:
        if group.getAttribute("name") == groupName:
            return group
        


def buildJSONContainers(lootContainers):
    """
    :param lootContainers: all XML elements of type "lootContainers", basically anything that can be looted
    :returns: Dictionary of items, groups, and "allItems" that the loot container provides
    """
    result = {}
    for group in lootContainers:
        id = group.getAttribute("id")
        itemsAndGroups = group.getElementsByTagName("item")

        items = getItemNames(itemsAndGroups)
        childGroups = getGroupNames(itemsAndGroups)
        allItems = getItemsRecursive(group)

        result[id] = {
            "items": items,
            "groups": childGroups,
            "allItems": allItems
        }
    return result


def buildJSONLootGroups(lootGroups):
    """
    :param lootGroups: all XML elements of type "lootGroups", so every grouping of items
    :returns: Dictionary of items, groups, and "allItems" that the loot group contains
    """
    result = {}
    for group in lootGroups:
        name = group.getAttribute("name")
        itemsAndGroups = group.getElementsByTagName("item")

        items = getItemNames(itemsAndGroups)
        childGroups = getGroupNames(itemsAndGroups)
        allItems = getItemsRecursive(group)

        result[name] = {
            "items": items,
            "groups": childGroups,
            "allItems": allItems
        }
    return result



def buildJSONBlocks(blocks):
    """
    :param blocks: all XML elements of type "blocks", so every block that is in the game
    :returns: Dictionary of items, groups, and "allItems" that the loot group contains
    """
    result = {}
    for block in blocks:
        blockName = block.getAttribute("name")
        blockContents = getLootPerBlock(block)
        if blockContents is None:
            continue
        else:
            result[blockName] = blockContents.copy() # We cant use the same object, as we are later adding human readable names to all of them
            if blockName in humanNames.keys():
                result[blockName]["humanName"] = humanNames[blockName]
            else:
                print("Following block that contains loot doesn't have a human readable name:", blockName) # Possibly parent blocks from which some blocks inherit the loot
    return result


def getLootPerBlock(block):
    """
    :param groupName: block XML element
    :returns: dictionary of what loot belongs to this block OR "None" if the block has no loot
    """
    id = getLootListID(block)
    if id is None:
        return None
    return containers[id]

def getLootListID(block):
    """
    :param block: block XML element
    :returns: "None" if the block doenst have a loot OR "LootList" value, which is basically the ID of the loot that it is supposed to contain
    """
    properties = block.getElementsByTagName("property")
    for element in properties:
        if element.getAttribute("name") == "LootList": # Only consider blocks that have loot
            return element.getAttribute("value")
    return None

def getAllGameItems(containers):
    """
    :param containers: dictionary of containers
    :returns: Dictionary of all the possible items within those containers
    """
    allItems = {}
    for name in containers:
        allItems.update(containers[name]["allItems"])
    return allItems




def writeData(data, fileName):
    with open(fileName,'w') as f:
        json.dump(data, f, sort_keys=True, indent=2)

humanNames = getHumanNames()

allGroups = buildJSONLootGroups(lootGroups)

containers = buildJSONContainers(lootContainers)

blocks = buildJSONBlocks(blocks)

allGameItems = getAllGameItems(containers)



## Comment out when not actually needed.

# writeData(allGameItems, extractedItemsFile)
# writeData(blocks, extractedBlocksFile)


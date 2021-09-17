# 7dtd

There are quite a few duplicates;
as in there are different objects, but they can have the same loot, but there are also pretty much identical objects except for they have different names. So am I supposed to divide them based on the loot, name, or human readable name?


# Search
## Based on container name
Write human readable name, you get to choose a real name, and click on that to get the loot. The loot is free of duplicates

## Get containers where you can find this item
Write the human readable name, choose real name, than you get to show the human readable block names which are free of duplicates that contain that item

## Get groups where this item is contained

## Get containers where you can find this group

## Be able to click on another item / group / container, and autofill the search field

## Have the search in the website parameters, so that you can always return to the previous result

# Notes
## Missing containers
There are cases where the contianers, eg. cars have multiple versions, and all of them have the same "master" class from which they inherit the loot. In this case the children versions have the localization names, although they dont have loot. While the parent that does have loot has no human readable name so they dont show in the search. Getting the children names and assigning it to parent is not that simple, but doable, and getting parent items from the child XML element is not that straight forward either, and creates quite a few duplicates. So for now, I will just post here things that I noticed.

```
cntCar03SedanDamage0Master
cntCar03SedanDamage1Master
```
are a parent loot containers for most of the cars, but they have identical loot AFAIK
#FLM: MM Generator
#Version 1.2
#
# Generates as many instances as one wants of a MM font for testing. This script
# is not for producing final production fonts, rather it is an aid for development.
#
# Version History
# 1.2 Added OpenType Feature and Class Export, May 10, 2005
# 1.1 Added OpenType Naming, May 8, 2005
# 1.0 First release
#
# Copyright Ben Kiel, 2005
# Licensed for use by a Creative Commons Attribution-NonCommercial-ShareAlike license
# See http://creativecommons.org/licenses/by-nc-sa/2.0/
# Most recent version of this script can be found at http://www.benkiel.com/

#Imports
from robofab.interface.all.dialogs import GetFolder, AskString, OneList, Message, TwoChecks, AskYesNoCancel
import os
import math

#Functions used

#asks for a number. if allowZeroOrLess is 0 it will not allow a number that is zero or less
def getNumber(message, allowZeroOrLess):
	userInput = AskString(message)
	if userInput is not None:
		try:
			int(userInput)
		except ValueError:
			userInput = getNumber('Please enter a number', allowZeroOrLess)
		if (userInput <= 0) and (allowZeroOrLess == 0):
			userInput = getNumber('Please enter a number greater than 0', 0)
		return int(userInput)
		
def getInstances(axisType):
	axis = []
	numberOfInstances = getNumber('How many instances on the ' + axisType + ' axis would you like?', 0)		
	if numberOfInstances is not None:
		if numberOfInstances >= 10:
			result = AskYesNoCancel('Did you really want ' + str(numberOfInstances))
			if result is 1:
				pass
			if result is 0:
				numberOfInstances = getNumber('How many instances on the ' + axisType + ' axis would you like?', 0)		
			if result is -1:
				numberOfInstances = 0
		for count in range(numberOfInstances):
			instance = getNumber('The ' + str(count+1) + ' value for the ' + axisType + ' instance', 1)
			if instance is not None:
				axis.append(instance)
		return axis

#From Kevin Altis at the ASPN Python Cookbook, http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/170242
def caseinsensitive_sort(stringList):
    """case-insensitive string comparison sort
    doesn't do locale-specific compare
    though that would be a nice addition
    usage: stringList = caseinsensitive_sort(stringList)"""

    tupleList = [(x.lower(), x) for x in stringList]
    tupleList.sort()
    return [x[1] for x in tupleList]


#From Alex Martelli on the python-list
def combinations(*lists):
    if not lists: return [ [] ]
    more = combinations(*lists[1:])
    return [ [i]+js for i in lists[0] for js in more ]

def buildFamilyName(family, axisTypes, styles):
	family = family + '_'
	for count in range(len(styles)):
		family = family + axisTypes[count] + str(styles[count])
	return family

def generateInstance(style, numberOfTypes, family, axisTypesInOrder, fontMM):
	f = Font(fontMM, tuple(style))
	
	# assignment of details
	f.family_name = buildFamilyName(family, axisTypesInOrder, style)
	f.full_name = f.family_name
	f.font_name = f.family_name
	f.menu_name = f.family_name
	f.apple_name = f.family_name
	f.pref_family_name = f.family_name
	f.mac_compatible = f.family_name
	f.weight = 'normal'
	
	# cleaning the glyphs
	for g in f.glyphs:
		g.Decompose()
		g.SelectAll()
		g.RemoveOverlap()  
	
	return f
	
def getFontFileType():
	fontTypes = {'Mac TrueType font':ftMACTRUETYPE, 'Mac Type 1 font':ftMACTYPE1, 'Mac TrueType DFONT':ftMACTRUETYPE_DFONT, 'PC TrueType/TT OpenType font (TTF)':ftTRUETYPE, 'OpenType (PS) font (OTF)':ftOPENTYPE, 'PC Type 1 font (binary/PFB)':ftTYPE1, 'PC MultipleMaster font (PFB)':ftTYPE1_MM, 'PC Type 1 font (ASCII/PFA)':ftTYPE1ASCII, 'PC MultipleMaster font (ASCII/PFA)':ftTYPE1ASCII_MM}
	keysSorted = caseinsensitive_sort(fontTypes.keys())
	fontType = OneList(keysSorted, 'What type of font do you want?')
	return fontTypes[fontType]

def addOpenTypeFeatures(orignalFont, newFont):
	if orignalFont.ot_classes:
		otClasses = orignalFont.ot_classes
	if orignalFont.features:
		otFeatures = orignalFont.features
		for fontFeature in otFeatures:			
			newFont.features.append(Feature(fontFeature))

#Pre-assigned variables
englishNumbers = {1 : 'first', 2 : 'second', 3 : 'third', 4 : 'fourth', 5 : 'fifth', 6 : 'sixth', 7 : 'seventh', 8 : 'eighth', 9 : 'ninth', 10 : 'tenth'}
axisTypes = ['weight', 'width', 'optical', 'serif']
axisInFont = {}
axisTypesInOrder = []
numberOfAxis = 0

if fl.count == 0:
	Message('A MM Font needs to be open to run this macro')

else:
	fontMM = fl.font        #the MM Font

if fontMM[0].layers_number == 1:
	Message('This Font does not have a MM axis')

else:
	
	#Get the family name
	family = AskString('Family Name')
	if family is None:
		family = AskString('Please enter a Family Name')

	#Get number of axis
	numberOfAxis = math.log(fontMM[0].layers_number, 2)
	numberOfAxis = int(numberOfAxis)
	
	#Get the axis info
	if numberOfAxis >= 1:
		firstAxisType = OneList(axisTypes, 'What type is the first axis?')
		if firstAxisType is not None:
			axisTypes.remove(firstAxisType)
			axisInFont[firstAxisType] = getInstances(firstAxisType)
			axisTypesInOrder.append(firstAxisType)
		
	if numberOfAxis >= 2:
		secondAxisType = OneList(axisTypes, 'What type is the second axis?')
		if secondAxisType is not None:
			axisTypes.remove(secondAxisType)
			axisInFont[secondAxisType] = getInstances(secondAxisType)
			axisTypesInOrder.append(secondAxisType)
		
	if numberOfAxis >= 3:
		thirdAxisType = OneList(axisTypes, 'What type is the third axis?')
		if thirdAxisType is not None:
			axisTypes.remove(thirdAxisType)
			axisInFont[thirdAxisType] = getInstances(thirdAxisType)
			axisTypesInOrder.append(thirdAxisType)
		
	if numberOfAxis == 4:
		axisInFont.append(axisTypes[0])
		axisInFont[axisTypes[0]] = getInstances(axisTypes[0])
		axisTypesInOrder.append(axisTypes[0])
	
	#Build the fonts
	if numberOfAxis is 1:
		style = combinations(axisInFont[axisTypesInOrder[0]])
	if numberOfAxis is 2:
		style = combinations(axisInFont[axisTypesInOrder[0]], axisInFont[axisTypesInOrder[1]])
	if numberOfAxis is 3:
		style = combinations(axisInFont[axisTypesInOrder[0]], axisInFont[axisTypesInOrder[1]], axisInFont[axisTypesInOrder[2]])
	if numberOfAxis is 4:
		style = combinations(axisInFont[axisTypesInOrder[0]], axisInFont[axisTypesInOrder[1]], axisInFont[axisTypesInOrder[2]], axisInFont[axisTypesInOrder[3]])
	
	
	#location for generated fonts
	howManyFiles = TwoChecks('Generate Font File', 'Generate Fontlab File')
	if howManyFiles is not 2:
		fontType = getFontFileType()
	path = GetFolder("Pick a directory...")
	if path:
		if os.path.isfile(path):
			dir, fileName = os.path.split(path)
		else:
			dir = path
		for i in style:
			f = generateInstance(i, len(axisTypesInOrder), family, axisTypesInOrder, fontMM)
			addOpenTypeFeatures(fontMM, f)
			fl.Add(f)
			# Export
			if howManyFiles is 1:
				path = os.sep.join([dir, f.font_name])
				fl.GenerateFont(fontType, path)
				f.modified = 0
				fl.Close(fl.ifont)
			if howManyFiles is 2:
				path = os.sep.join([dir, f.font_name])
				fl.Save((path + '.vfb'))
				f.modified = 0
			if howManyFiles is 3:
				path = os.sep.join([dir, f.font_name])
				fl.GenerateFont(fontType, path)
				fl.Save((path + '.vfb'))
				f.modified = 0
			if howManyFiles is 0:
				Message('No Font Generated')
	else:
		Message('Please pick a valid path')
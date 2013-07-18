#FLM: Dump or Fuse
# Version 1.3
# (c) 2006 Ben Kiel
#
# Allows one to dump out a comma seperated list of composite glyphs, and also
# re-imports said list and makes changes to the composites based on changes to
# the file. Useful for tracking and changing composites in Excel
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#Imports
import os
import os.path
import robofab.world
from robofab.world import CurrentFont
from robofab.objects.objectsRF import RFont as _RFont
from robofab.pens.digestPen import DigestPointPen
from robofab.interface.all.dialogs import PutFile, GetFile, Message, OneList, TwoChecks, AskYesNoCancel, ProgressBar

#Functions
def _findFile(fontPath, message):
	dir, fileName = os.path.split(fontPath)
	fileList = []
	names = os.listdir(dir)
	for n in names:
		if n[-4:] != '.ufo' or n[-4:] != '.vfb' or n[-4:] != '.bak':
			fileList.append(n)
	fileList.append('Look elsewhere')
	f = OneList(fileList, message)
	if f == 'Look elsewhere':
		filePath = GetFile(message)
	elif f == None:
		filePath = None
	else:
		filePath = os.path.join(dir, f)
	return filePath

"""
getDataFile opens a semi-colon seperated file of the format:
glyph name;glyph advance width;first component name;glyph component x-position;glyph component y-position
The method takes in a message for the open file dialog.
It returns a list of the glyphs in this format:
(glyphname, width, [(component, x-position, y-position)]
"""
def getDataFile(fontPath, message):
	#List of glyphs in semi-colon seperated file
	importedGlyphList = []
	
	#Get file
	filePath = _findFile(fontPath, message)
	
	if filePath is None:
		return None
	
	else:
		file = open(filePath, 'r')
		for line in file:
			# Split line at semi-colon
			rawData = line.split(';')
			
			# First bit is the glyph name
			finalName = rawData[0]
			# Second bit is the advance width
			width = int(rawData[1])
			
			# Figure out how many components are in a glyph
			numberOfComponents = (len(rawData)-2) / 3
			componentList = []
			
			# Build component list
			count = 0
			while count < numberOfComponents:
				startIndex = 2 + (3 * count)
				componentList.append((rawData[startIndex], int(rawData[startIndex+1]), int(rawData[startIndex+2])))
				count = count+1
			importedGlyphList.append((finalName, width, componentList))
		file.close()
		return importedGlyphList

"""
makeGlyph takes in a list of of glyphs, a font object, a message for the progress bar, and a mark value.
It also pops up a helpful progess bar, because things are better with progress bars.
"""
def makeGlyph(glyphList, font, message, mark, saveBackup):
	# Initialize the progress bar
	tickCount = len(glyphList)
	bar = ProgressBar(message, tickCount)
	tick = 0
	
	testingFont = _RFont()
	
	for item in glyphList:
		glyphName, advanceWidth, components = item
		
		# If the font has the glyph, lots of checking is required to see if changes have been made
		if font.has_key(glyphName):
			glyph = font[glyphName]
			
			#Build new glyph for comparisons
			testingFont.newGlyph(glyphName, clear=True)
			newGlyph = testingFont[glyphName]
			newGlyphCount = 0
			while newGlyphCount < len(components):
				component, x, y = components[newGlyphCount]
				newGlyph.appendComponent(component, offset=(x,y))
				newGlyphCount = newGlyphCount+1			
			newGlyph.width = advanceWidth
			newGlyph.round()
			
			# Make digest of the new glyph
			pointPen = DigestPointPen()
			newGlyph.drawPoints(pointPen)
			newDigest = pointPen.getDigest()
			
			# Make digest of the old glyph
			pointPen = DigestPointPen()
			glyph.drawPoints(pointPen)
			oldDigest = pointPen.getDigest()
			
			# Check the advance width
			if glyph.width != advanceWidth:
				glyph.width = advanceWidth
				if mark == 1:
					glyph.mark = 200
			
			# If the digests don't match, rebuild components
			if oldDigest != newDigest:
				if saveBackup == 1:
					backupName = glyph.name + '.bkup'
					font.insertGlyph(glyph, as=backupName)
					font[backupName].update()
				glyph.clearComponents()
				count = 0
				while count < len(components):
					component, x, y = components[count]
					glyph.appendComponent(component, offset=(x,y))
					count = count+1
				if mark == 1:
					glyph.mark = 200
			
			# Clean up things
			glyph.update()
			bar.tick(tick)
			tick = tick+1
		
		# If the glyph is not in the font, build a new glyph
		else:
			font.newGlyph(glyphName, clear=True)
			glyph = font[glyphName]
			glyph.width = advanceWidth
			count = 0
			while count < len(components):
				component, x, y = components[count]
				glyph.appendComponent(component, offset=(x,y))
				count = count+1
			if mark == 1:
				glyph.mark = 300
			glyph.update()
			bar.tick(tick)
			tick = tick+1
	
	font.update()
	testingFont.close()
	bar.close()

"""
checkGlyphs takes in a font and a glyphList. It checks to see if the the components in the glyph list are in the font. 
It returns a list of missing components. The list is empty if all components are present in a font.
"""
def checkGlyphs(font, glyphList):
	missingComponents = []
	for item in glyphList:
		glyphName, advanceWidth, components = item
		for piece in components:
			component, x, y = piece
			if font.has_key(component) != True:
				missingComponents.append(component)
	return missingComponents

def checkPath(path):
		count = 1
		while os.path.isfile(path):
			directory, fileName = os.path.split(path)
			if fileName[-1:] == str(count-1):
				fileName = fileName[:-1]
			fileName = fileName + str(count)
			path = os.sep.join([directory, fileName])
			count = count + 1
		return path
	
def dump(font):
	filePath = checkPath(font.path[:-4] + ".txt")

	if filePath is not None:
		tickCount = len(font)
		bar = ProgressBar('Writing dump file', tickCount)
		tick = 0
		outList = []
		for glyph in font:
			bar.tick(tick)
			tick = tick+1
			if len(glyph.components) != 0:
				output = glyph.name + ';' + str(glyph.width)
				componentNumber = 0
				while componentNumber < len(glyph.components):
					x, y = glyph.components[componentNumber].offset
					output = output + ';' + glyph.components[componentNumber].baseGlyph + ';' + str(x) + ';' + str(y)
					componentNumber = componentNumber + 1
				output = output + '\n'
				outList.append((glyph.index, output))

		# Create a dictionary for sorting the glyphs by GID
		outDictionary = dict(outList)
		outKeys = outDictionary.keys()
		outKeys.sort()
		
		# Write out the file
		file = open(filePath, 'w')
		keyCount = 0
		while keyCount < len(outKeys):
			file.write(outDictionary[outKeys[keyCount]])
			keyCount = keyCount + 1
		file.close()
		bar.close()
		Message('Dump file written')
		
def fuse(font):
	readGlyphList = getDataFile(font.path, 'Choose a dump file')
	if readGlyphList is not None:
		# Check to make sure that all compontents are present in the font
		checkedGlyphList = checkGlyphs(font, readGlyphList)
		if len(checkedGlyphList) == 0:
			mark = AskYesNoCancel('Do you wish to mark changed glyphs?')
			if mark != -1:
				saveBackup = AskYesNoCancel('Do you want a backup of changed glyphs?')
				if saveBackup != -1:
					makeGlyph(readGlyphList, font, 'Updating glyphs', mark, saveBackup)
					font.update()
					Message('Done updating glyphs')
		else:
			# Gives a list of the components missing from the VFB
			OneList(checkedGlyphList, 'Sorry, your VFB is missing:')

#Script
font = CurrentFont()
do = TwoChecks('Dump components', 'Fuse components', 0, 0, 'Fuse/Dump')
if do == 1:
	dump(font)
if do == 2:
	fuse(font)
if do == 3:
	dump(font)
	fuse(font)
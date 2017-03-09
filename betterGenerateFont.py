#FLM: Font Generator
# Version 1.6
#
# Provides a better method for generating test fonts. Makes a copy of the font,
# then removes overlaps, decomposes glyphs, and generates a font. It then closes
# the copy of the font, making sure that you haven't just destroyed the font you
# are working on.
#
# Version History 
# 1.6 Worked out problems with glyphs of many components, thanks to Claus Eggers S¿rensen. 
# I've also sped up the path direction correction, answering Rob Kellers complaints.
# 1.5 Fixed a bug with OT Classes that was either always there or introduced in FL5. Thanks to 
# David Brezina for finding and fixing that & Karsten Luecke for getting on me to post the new version
# 1.4 Added in correcting path direction. Takes longer but no longer will glyphs appear bolder than they are.
# 1.3 Took out the option for font type. Save a step, only PS OpenType now. December 15, 2006
# 1.2 Took out extra, often unused, font generation options, see note in code. April 13, 2006
# 1.1 Added OpenType Feature and Class Export, May 10, 2005
# 1.0 First release
#
# Opentype Features
# If you link your OpenType features or groups in external files, for this to work you will need to use the
# full path when including your files, or they won't be put into the test font.
#
# Copyright Ben Kiel, 2005
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
from robofab.world import CurrentFont
from robofab.interface.all.dialogs import GetFolder, Message, OneList, AskYesNoCancel, AskString, ProgressBar
import os.path

#Functions
def copyFont():
	tempFont = fl.font
	f = Font(tempFont)
	if tempFont.ot_classes:
		f.ot_classes = tempFont.ot_classes
	if tempFont.features:
		otFeatures = tempFont.features
		for fontFeature in otFeatures:			
			f.features.append(Feature(fontFeature))
	fl.Add(f)

def decomposeFont(font):
	nakedFont = font.naked()
	tickCount = len(nakedFont)
	tick = 0
	bar = ProgressBar('Cleaning up glyphs', tickCount)
	for g in font:
		nakedFont[g.name].Decompose()
		nakedFont[g.name].RemoveOverlap()
		bar.tick(tick)
		tick = tick+1
	bar.close()
	tickCount = len(font)
	tick = 0
	bar = ProgressBar('Correcting direction', tickCount)
	for g in font:
		fl.TransformGlyph(g.naked(), TR_CODE_REVERSE_ALL, '0002')
	bar.close()
	return nakedFont

def getFontFileType():
	# took the following out, add in as needed: 'Mac TrueType font':ftMACTRUETYPE, 'Mac Type 1 font':ftMACTYPE1, 'Mac TrueType DFONT':ftMACTRUETYPE_DFONT, 'PC Type 1 font (binary/PFB)':ftTYPE1, 'PC MultipleMaster font (PFB)':ftTYPE1_MM, 'PC Type 1 font (ASCII/PFA)':ftTYPE1ASCII, 'PC MultipleMaster font (ASCII/PFA)':ftTYPE1ASCII_MM
	fontTypes = {'PC TrueType/TT OpenType font (TTF)':ftTRUETYPE, 'PS OpenType (CFF-based) font (OTF)':ftOPENTYPE}
	fontType = OneList(fontTypes.keys(), 'What type of font do you want?')
	if fontType is not None:
		return fontTypes[fontType]
	else:
		return None
		
def closeFont(font):
	font.modified = 0
	fl.Close(fl.ifont)

def renameFont(font):
	family = AskString('New font family name:')
	font.family_name = family
	font.full_name = font.family_name
	font.font_name = font.family_name
	font.menu_name = font.family_name
	font.apple_name = font.family_name
	return font

def checkPath(path, fontType):
		if os.path.isfile(path):
			dir, fileName = os.path.split(path)
		else:
			dir = path
		fontName = addExtension(fontType, font.font_name)
		path = os.sep.join([dir, fontName])
		if os.path.isfile(path):
			overwrite = AskYesNoCancel('Font exists, do you want to rename the font?', default=1)
			if overwrite is 1:
				f = renameFont(font)
				fontName = addExtension(fontType, version, f.font_name)
				dir, fileName = os.path.split(path)
				path = os.sep.join([dir, fontName])
			elif overwrite is -1:
				closeFont(font)
			else:
				pass
		return path

def getSaveLocation(font, fontType):
	path = GetFolder("Pick a directory...")
	if path:
		return checkPath(path, fontType)
	else:
		closeFont(font)
		return None

def addExtension(fontType, fontName):
	if fontType == ftMACTRUETYPE:
		fontName = fontName + '.ttf'
	if fontType == ftOPENTYPE:
		fontName = fontName + '.otf'
	return fontName

#Program
copyFont()
rfFont = CurrentFont()
font = decomposeFont(rfFont)
fontType = ftOPENTYPE
if fontType is None:
	closeFont(font)
elif font.font_name is None:
	Message("Error: No font naming information. Please set the font names first in Font > Info > Names and Copyright")
	closeFont(font)
else:
	path = getSaveLocation(font, fontType)
	if path is not None:
		fl.GenerateFont(fontType, path)
		closeFont(font)

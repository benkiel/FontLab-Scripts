#FLM: Place Anchor
# Version 1.2 Final
# (c) Ben Kiel
# Updates can be found at http://www.benkiel.com/
#
# Places anchors at a specified height on selected glyphs

from robofab.world import CurrentFont
from robofab.interface.all.dialogs import SearchList, AskString, Message

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

def getGlyphWidth(glyph):
	box = glyph.box
	width = box[2] - box[0]
	return width

#Program
font = CurrentFont()
glyphs = font.selection
y = getNumber('Vertical Position?', 1)
name = AskString('Name of anchors')
for glyph in glyphs:
	x = int(getGlyphWidth(font[glyph])/2) + font[glyph].leftMargin
	font[glyph].appendAnchor(name, (x,y))
font.update()
Message('All done!')
	

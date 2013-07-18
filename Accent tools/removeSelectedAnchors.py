#FLM: Remove Selected Anchors
# Removes anchors on selected glyphs

from robofab.world import CurrentFont
from robofab.interface.all.dialogs import SearchList, AskString, Message

#Program
font = CurrentFont()
glyphs = font.selection
for glyph in glyphs:
	glyph.clearAnchors()
font.update()
Message('All done!')
	

#FLM: Remove Anchors
# Removes all anchors from a font

from robofab.world import CurrentFont
from robofab.interface.all.dialogs import SearchList, AskString, Message

#Program
font = CurrentFont()
for glyph in font:
	glyph.clearAnchors()
font.update()
Message('All done!')
	

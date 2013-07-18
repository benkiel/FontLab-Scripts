#FLM: Lowercase Guides
# Version 0.1
# Sample script, demostrating how to add and remove guidelines. Useful for only
# looking at guidelines for the type of glyphs one is working on, and not the
# other types.
from robofab.world import CurrentFont

def clearAllGuides(font):
	font.clearHGuides()
	font.clearVGuides()

font = CurrentFont()
clearAllGuides(font)
font.appendHGuide(460)
font.appendHGuide(407)
font.appendHGuide(45)
font.appendHGuide(36)
font.appendHGuide(-11)
font.update()
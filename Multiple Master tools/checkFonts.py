#FLM: Check unopened font glyphs for MM
#
# Useful for testing to see if two fonts are compatible as as MM font

# First import OpenFont, which allows the user open a font file
# Also import RFont, so that a new font can be created
from robofab.world import OpenFont, RFont

# Get the two masters for the interpolated font
minFont = OpenFont(None, "First font")
maxFont = OpenFont(None, "Second font")

for glyph in minFont:
	data = glyph.isCompatible(maxFont.getGlyph(glyph.name), report=True)
	print glyph
	print data
print 'all done'
#FLM: Copy Font Sidebearing
# (c) Ben Kiel
#
# Copys one font's sidebearing values to another font

#Imports
from robofab.world import OpenFont, CurrentFont
from robofab.interface.all.dialogs import Message

fontToChange = CurrentFont()
orignalMetricsFont = OpenFont(None, "Which font's sidebearings do you want?")
orignalMetrics = {}

for glyph in orignalMetricsFont:
	orignalMetrics[glyph.name] = [glyph.leftMargin, glyph.rightMargin]
orignalMetricsFont.close()

for name, metrics in orignalMetrics.iteritems():
	if fontToChange.has_key(name):
		fontToChange[name].leftMargin = metrics[0]
		fontToChange[name].rightMargin = metrics[1]
fontToChange.update()
Message('Done changing sidebearings')
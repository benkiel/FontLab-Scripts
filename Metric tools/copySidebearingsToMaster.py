#FLM: Copy Font Sidebearing to Master
# (c) Ben Kiel
# Updates can be found at http://www.benkiel.com/
#
# Copys the sidebearing values of one font to a specified master in another font.
# Useful when combining two different fonts into a MM font for production.

#Imports
from robofab.world import OpenFont, CurrentFont
from robofab.interface.all.dialogs import Message, OneList, ProgressBar

def hasMM(nakedFont):
	if nakedFont[0].layers_number == 1:
		return False
	else:
		return True
	
def getLayer(nakedFont, message):
	numberOfLayers = nakedFont[0].layers_number - 1
	layers = []
	while numberOfLayers >= 0:
		layers.append(numberOfLayers)
		numberOfLayers = numberOfLayers - 1
	whichLayer = OneList(layers, message)
	return int(whichLayer)
	
fontToChange = CurrentFont()
if not hasMM(fontToChange.naked()):
	Message('Font needs to be MM')
else:
	orignalMetricsFont = OpenFont(None, "Which font's sidebearings do you want?")
	orignalMetrics = {}
	tickCount = len(orignalMetricsFont)
	bar = ProgressBar('Getting metrics', tickCount)
	tick = 0	
	
	if hasMM(orignalMetricsFont.naked()):
		layer = getLayer(orignalMetricsFont.naked(), 'Which layer do you want?')
		for glyph in orignalMetricsFont:
			advanceWidth = int(glyph.naked().GetMetrics(layer).x)
			glyphWidth = int(glyph.naked().GetBoundingRect(layer).width)
			glyphLeft = int(glyph.naked().GetBoundingRect(layer).x)
			glyphRight = advanceWidth - (glyphWidth + glyphLeft)
			orignalMetrics[glyph.name] = [glyphLeft, glyphRight]
			bar.tick(tick)
			tick = tick+1
		bar.close()
		orignalMetricsFont.close()
	else:
		for glyph in orignalMetricsFont:
			orignalMetrics[glyph.name] = [glyph.leftMargin, glyph.rightMargin]
			bar.tick(tick)
			tick = tick+1
		bar.close()
		orignalMetricsFont.close()
	
	layer = getLayer(fontToChange.naked(), 'Which layer to change?')
	tickCount = len(fontToChange)
	bar = ProgressBar('Changing Metrics', tickCount)
	tick = 0	
	for name, metrics in orignalMetrics.iteritems():
		if fontToChange.has_key(name):
			glyphWidth = int(fontToChange[name].naked().GetBoundingRect(layer).width)
			oldLeft = int(fontToChange[name].naked().GetBoundingRect(layer).x)
			newAdvanceWidth = glyphWidth + metrics[0] + metrics[1]
			leftShift = metrics[0] - oldLeft
			shiftPoint = Point(leftShift, 0)
			widthPoint = Point(newAdvanceWidth, 0)
			fontToChange[name].naked().SetMetrics(widthPoint, layer)
			fontToChange[name].naked().Shift(shiftPoint, layer)
			bar.tick(tick)
			tick = tick+1
	bar.close()
	fontToChange.update()
	Message('Done changing sidebearings')
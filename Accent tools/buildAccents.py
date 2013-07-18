#FLM: Build Accents
# (c) ben kiel
# version 0.4
# 
# Version History
# version 0.4: fixed bug copy bug for the tcommaacents and dotlessi.sc
# version 0.3: now asks for info about how things are named in your font so
#			   the user can have any combination of specially designed glyphs
#			   in the font. Also fixes a couple of missing glyphs and adds the
#			   duplicate characters with differnt unicode values
# version 0.2: now checks to see if glyph is already in font, gives option
# 			   to leave it in or build a new glyph
# version 0.1: first release
#
# Updates can be found at http://www.benkiel.com/

from robofab.world import CurrentFont
from robofab.interface.all.dialogs import Message, ProgressBar, AskYesNoCancel, TwoChecks, AskString
import string

"""
Builds accents for lowercase, uppercase, and small caps.
Will not build accents for characters that need a lot of tweaking, such as
lcaron, and the slash accents.
"""

#Lists of accents
lowerCaseList = [
	('a', 'aacute', [('acute', 'top')]),
	('a', 'abreve', [('breve', 'top')]),
	('a', 'acircumflex', [('circumflex', 'top')]),
	('a', 'adieresis', [('dieresis', 'top')]),
	('ae', 'aeacute', [('acute', 'top')]),
	('a', 'agrave', [('grave', 'top')]),
	('a', 'amacron', [('macron', 'top')]),
	('a', 'aogonek', [('ogonek', 'bottom')]),
	('a', 'aring', [('ring', 'top')]),
	('a', 'aringacute', [('ring', 'top'), ('acute', 'top')]),
	('a', 'atilde', [('tilde', 'top')]),
	('c', 'cacute', [('acute', 'top')]),
	('c', 'ccaron', [('caron', 'top')]),
	('c', 'ccedilla', [('cedilla', 'bottom')]),
	('c', 'ccircumflex', [('circumflex', 'top')]),
	('c', 'cdotaccent', [('dotaccent', 'top')]),
	('e', 'eacute', [('acute', 'top')]),
	('e', 'ebreve', [('breve', 'top')]),
	('e', 'ecaron', [('caron', 'top')]),
	('e', 'ecircumflex', [('circumflex', 'top')]),
	('e', 'edieresis', [('dieresis', 'top')]),
	('e', 'edotaccent', [('dotaccent', 'top')]),
	('e', 'egrave', [('grave', 'top')]),
	('e', 'emacron', [('macron', 'top')]),
	('e', 'eogonek', [('ogonek', 'bottom')]),
	('g', 'gbreve', [('breve', 'top')]),
	('g', 'gcircumflex', [('circumflex', 'top')]),
	('g', 'gcommaaccent', [('commaaccent', 'top')]),
	('g', 'gdotaccent', [('dotaccent', 'top')]),
	('h', 'hcircumflex', [('circumflex', 'top')]),
	('dotlessi', 'iacute', [('acute', 'top')]),
	('dotlessi', 'ibreve', [('breve', 'top')]),
	('dotlessi', 'icircumflex', [('circumflex', 'top')]),
	('dotlessi', 'idieresis', [('dieresis', 'top')]),
	('dotlessi', 'igrave', [('grave', 'top')]),
	('dotlessi', 'imacron', [('macron', 'top')]),
	('i', 'iogonek', [('ogonek', 'bottom')]),
	('dotlessi', 'itilde', [('tilde', 'top')]),
	('k', 'kcommaaccent', [('commaaccent', 'bottom')]),
	('l', 'lacute', [('acute', 'top')]),
	('l', 'lcommaaccent', [('commaaccent', 'bottom')]),
	('l', 'ldot', [('dotaccent', 'right')]),
	('n', 'nacute', [('acute', 'top')]),
	('n', 'ncaron', [('caron', 'top')]),
	('n', 'ncommaaccent', [('commaaccent', 'bottom')]),
	('n', 'ntilde', [('tilde', 'top')]),
	('o', 'oacute', [('acute', 'top')]),
	('o', 'obreve', [('breve', 'top')]),
	('o', 'ocircumflex', [('circumflex', 'top')]),
	('o', 'odieresis', [('dieresis', 'top')]),
	('o', 'ograve', [('grave', 'top')]),
	('o', 'ohungarumlaut', [('hungarumlaut', 'top')]),
	('o', 'omacron', [('macron', 'top')]),
	('oslash', 'oslashacute', [('acute', 'top')]),
	('o', 'otilde', [('tilde', 'top')]),
	('r', 'racute', [('acute', 'top')]),
	('r', 'rcaron', [('caron', 'top')]),
	('r', 'rcommaaccent', [('commaaccent', 'bottom')]),
	('s', 'sacute', [('acute', 'top')]),
	('s', 'scaron', [('caron', 'top')]),
	('s', 'scedilla', [('cedilla', 'bottom')]),
	('s', 'scircumflex', [('circumflex', 'top')]),
	('s', 'scommaaccent', [('commaaccent', 'bottom')]),
	('t', 'tcommaaccent', [('commaaccent', 'bottom')]),
	('u', 'uacute', [('acute', 'top')]),
	('u', 'ubreve', [('breve', 'top')]),
	('u', 'ucircumflex', [('circumflex', 'top')]),
	('u', 'udieresis', [('dieresis', 'top')]),
	('u', 'ugrave', [('grave', 'top')]),
	('u', 'uhungarumlaut', [('hungarumlaut', 'top')]),
	('u', 'umacron', [('macron', 'top')]),
	('u', 'uogonek', [('ogonek', 'bottom')]),
	('u', 'uring', [('ring', 'top')]),
	('u', 'utilde', [('tilde', 'top')]),
	('w', 'wacute', [('acute', 'top')]),
	('w', 'wcircumflex', [('circumflex', 'top')]),
	('w', 'wdieresis', [('dieresis', 'top')]),
	('w', 'wgrave', [('grave', 'top')]),
	('y', 'yacute', [('acute', 'top')]),
	('y', 'ycircumflex', [('circumflex', 'top')]),
	('y', 'ydieresis', [('dieresis', 'top')]),
	('y', 'ygrave', [('grave', 'top')]),
	('z', 'zacute', [('acute', 'top')]),
	('z', 'zcaron', [('caron', 'top')]),
	('z', 'zdotaccent', [('dotaccent', 'top')])
]

baseUpperCaseList = [
	('A', 'Aacute', [('acute', 'top')]),
	('A', 'Abreve', [('breve', 'top')]),
	('A', 'Acircumflex', [('circumflex', 'top')]),
	('A', 'Adieresis', [('dieresis', 'top')]),
	('AE', 'AEacute', [('acute', 'top')]),
	('A', 'Agrave', [('grave', 'top')]),
	('A', 'Amacron', [('macron', 'top')]),
	('A', 'Aogonek', [('ogonek', 'bottom')]),
	('A', 'Aring', [('ring', 'top')]),
	('A', 'Aringacute', [('ring', 'top'), ('acute', 'top')]),
	('A', 'Atilde', [('tilde', 'top')]),
	('C', 'Cacute', [('acute', 'top')]),
	('C', 'Ccaron', [('caron', 'top')]),
	('C', 'Ccedilla', [('cedilla', 'bottom')]),
	('C', 'Ccircumflex', [('circumflex', 'top')]),
	('C', 'Cdotaccent', [('dotaccent', 'top')]),
	('D', 'Dcaron', [('caron', 'top')]),
	('E', 'Eacute', [('acute', 'top')]),
	('E', 'Ebreve', [('breve', 'top')]),
	('E', 'Ecaron', [('caron', 'top')]),
	('E', 'Ecircumflex', [('circumflex', 'top')]),
	('E', 'Edieresis', [('dieresis', 'top')]),
	('E', 'Edotaccent', [('dotaccent', 'top')]),
	('E', 'Egrave', [('grave', 'top')]),
	('E', 'Emacron', [('macron', 'top')]),
	('E', 'Eogonek', [('ogonek', 'bottom')]),
	('G', 'Gbreve', [('breve', 'top')]),
	('G', 'Gcircumflex', [('circumflex', 'top')]),
	('G', 'Gcommaaccent', [('commaaccent', 'bottom')]),
	('G', 'Gdotaccent', [('dotaccent', 'top')]),
	('H', 'Hcircumflex', [('circumflex', 'top')]),
	('I', 'Iacute', [('acute', 'top')]),
	('I', 'Ibreve', [('breve', 'top')]),
	('I', 'Idotaccent', [('dotaccent', 'top')]),
	('I', 'Icircumflex', [('circumflex', 'top')]),
	('I', 'Idieresis', [('dieresis', 'top')]),
	('I', 'Igrave', [('grave', 'top')]),
	('I', 'Imacron', [('macron', 'top')]),
	('I', 'Iogonek', [('ogonek', 'bottom')]),
	('I', 'Itilde', [('tilde', 'top')]),
	('J', 'Jcircumflex', [('circumflex', 'top')]),
	('K', 'Kcommaaccent', [('commaaccent', 'bottom')]),
	('L', 'Lacute', [('acute', 'top')]),
	('L', 'Lcommaaccent', [('commaaccent', 'bottom')]),
	('L', 'Ldot', [('dotaccent', 'right')]),
	('N', 'Nacute', [('acute', 'top')]),
	('N', 'Ncaron', [('caron', 'top')]),
	('N', 'Ncommaaccent', [('commaaccent', 'bottom')]),
	('N', 'Ntilde', [('tilde', 'top')]),
	('O', 'Oacute', [('acute', 'top')]),
	('O', 'Obreve', [('breve', 'top')]),
	('O', 'Ocircumflex', [('circumflex', 'top')]),
	('O', 'Odieresis', [('dieresis', 'top')]),
	('O', 'Ograve', [('grave', 'top')]),
	('O', 'Ohungarumlaut', [('hungarumlaut', 'top')]),
	('O', 'Omacron', [('macron', 'top')]),
	('Oslash', 'Oslashacute', [('acute', 'top')]),
	('O', 'Otilde', [('tilde', 'top')]),
	('R', 'Racute', [('acute', 'top')]),
	('R', 'Rcaron', [('caron', 'top')]),
	('R', 'Rcommaaccent', [('commaaccent', 'bottom')]),
	('S', 'Sacute', [('acute', 'top')]),
	('S', 'Scaron', [('caron', 'top')]),
	('S', 'Scedilla', [('cedilla', 'bottom')]),
	('S', 'Scircumflex', [('circumflex', 'top')]),
	('S', 'Scommaaccent', [('commaaccent', 'bottom')]),
	('T', 'Tcommaaccent', [('commaaccent', 'bottom')]),
	('T', 'Tcaron', [('caron', 'top')]),
	('U', 'Uacute', [('acute', 'top')]),
	('U', 'Ubreve', [('breve', 'top')]),
	('U', 'Ucircumflex', [('circumflex', 'top')]),
	('U', 'Udieresis', [('dieresis', 'top')]),
	('U', 'Ugrave', [('grave', 'top')]),
	('U', 'Uhungarumlaut', [('hungarumlaut', 'top')]),
	('U', 'Umacron', [('macron', 'top')]),
	('U', 'Uogonek', [('ogonek', 'bottom')]),
	('U', 'Uring', [('ring', 'top')]),
	('U', 'Utilde', [('tilde', 'top')]),
	('W', 'Wacute', [('acute', 'top')]),
	('W', 'Wcircumflex', [('circumflex', 'top')]),
	('W', 'Wdieresis', [('dieresis', 'top')]),
	('W', 'Wgrave', [('grave', 'top')]),
	('Y', 'Yacute', [('acute', 'top')]),
	('Y', 'Ycircumflex', [('circumflex', 'top')]),
	('Y', 'Ydieresis', [('dieresis', 'top')]),
	('Y', 'Ygrave', [('grave', 'top')]),
	('Z', 'Zacute', [('acute', 'top')]),
	('Z', 'Zcaron', [('caron', 'top')]),
	('Z', 'Zdotaccent', [('dotaccent', 'top')])
]

def buildAccents(font, list, message, overwrite, preflight=False):
	"""
	Takes in a list of accents to build in the format of (baseGlyph, finalName, accentList)
	Marks glyphs that it has built, and updates the font
	"""
	tickCount = len(list)
	bar = ProgressBar(message, tickCount)
	tick = 0	
	for item in list:
		baseGlyph, outputName, accents = item
		if font.has_key(baseGlyph):
			if font.has_key(outputName):
				if overwrite == 1 or overwrite == 3:
					answer = AskYesNoCancel(outputName + ' exists in font, overwrite?')
					if answer == 1:
						font.compileGlyph(outputName, baseGlyph, accents, preflight=preflight)
						font[outputName].mark = 200
						font[outputName].autoUnicodes()
						font[outputName].update()
						font.update()
				if overwrite == 2:
					font.compileGlyph(outputName, baseGlyph, accents, preflight=preflight)
					font[outputName].mark = 200
					font[outputName].autoUnicodes()
					font[outputName].update()
					font.update()	
			else:
				font.compileGlyph(outputName, baseGlyph, accents, preflight=preflight)
				font[outputName].mark = 200
				font[outputName].autoUnicodes()
				font[outputName].update()
				font.update()
		bar.tick(tick)
		tick = tick+1
	bar.close()
 
def rewriteAccentNames(list, suffix):
	newList = []
	for item in list:
		baseGlyph, outputName, accents = item
		newAccentList = []
		for accent in accents:
			accentname, location = accent
			accentname = accentname + suffix
			newAccentList.append((accentname, location))
		newList.append((baseGlyph, outputName, newAccentList))
	return newList

def rewriteSmallCapList(list, suffix, accentSuffix):
	newList = []
	for item in list:
		baseGlyph, outputName, accents = item
		baseGlyph = baseGlyph + suffix
		outputName = outputName + suffix
		newAccentList = []
		for accent in accents:
			accentname, location = accent
			accentname = accentname + accentSuffix
			newAccentList.append((accentname, location))
		newList.append((baseGlyph, outputName, newAccentList))
	return newList
	
#Program
font = CurrentFont()
overwrite = TwoChecks('Ask to overwrite glyphs', 'Overwrite, do not ask', value1=0, value2=0)
whatToBuild = TwoChecks('Cap accents in font?', 'Small Caps in font?', value1=0, value2=0)
buildSmallCap = 0
if whatToBuild == 0:
	upperCaseList = baseUpperCaseList
if whatToBuild == 1:
	suffix = AskString('Suffix for cap accents')
	upperCaseList = rewriteAccentNames(baseUpperCaseList, suffix)
if whatToBuild == 2:
	scAccentSuffix = ''
	upperCaseList = baseUpperCaseList
	buildSmallCap = 1
	scAccentSuffix = ''
	scSuffix = AskString('Suffix for small caps?')
	specialSmallCapAccents = AskYesNoCancel('Special small cap accents?')
	if specialSmallCapAccents == 1:
		scAccentSuffix = AskString('Suffix for small cap accents', scSuffix)
	smallCapList = rewriteSmallCapList(baseUpperCaseList, scSuffix, scAccentSuffix)
if whatToBuild == 3:
	buildSmallCap = 1
	scAccentSuffix = ''
	suffix = AskString('Suffix for cap accents')
	upperCaseList = rewriteAccentNames(baseUpperCaseList, suffix)
	scSuffix = AskString('Suffix for small caps?')
	specialSmallCapAccents = AskYesNoCancel('Use lowercase accents for small caps?')
	if specialSmallCapAccents == 0:
		whatToDo = TwoChecks('Use cap accents', 'Use special accents', value1=0, value2=0)
		if whatToDo == 1:
			scAccentSuffix = suffix
		if whatToDo == 2:
			scAccentSuffix = AskString('Suffix for small cap accents', scSuffix)
	smallCapList = rewriteSmallCapList(baseUpperCaseList, scSuffix, scAccentSuffix)
	

buildAccents(font, lowerCaseList, 'Building lowercase accents', overwrite)
buildAccents(font, upperCaseList, 'Building uppercase accents', overwrite)
if buildSmallCap == 1:
	buildAccents(font, smallCapList, 'Building small cap accents', overwrite)

#Build a couple of accents that would be missed
font.newGlyph('uni021B', clear=True)
font.newGlyph('uni021A', clear=True)
font.newGlyph('Dotlessi.sc', clear=True)
dotlessisc = font['I.sc'].copy()
duplicatetcommaaccent = font['tcommaaccent'].copy()
duplicateTcommaaccent = font['Tcommaaccent'].copy()
font['Dotlessi.sc'].appendGlyph(dotlessisc)
font['uni021B'].appendGlyph(duplicatetcommaaccent)
font['uni021A'].appendGlyph(duplicateTcommaaccent)
font['uni021B'].width = duplicatetcommaaccent.width
font['uni021B'].leftMargin = duplicatetcommaaccent.leftMargin
font['uni021B'].rightMargin = duplicatetcommaaccent.rightMargin
font['uni021B'].mark = 200
font['uni021A'].width = duplicateTcommaaccent.width
font['uni021A'].leftMargin = duplicateTcommaaccent.leftMargin
font['uni021A'].rightMargin = duplicateTcommaaccent.rightMargin
font['uni021A'].mark = 200
font['Dotlessi.sc'].width = dotlessisc.width
font['Dotlessi.sc'].leftMargin = dotlessisc.leftMargin
font['Dotlessi.sc'].rightMargin = dotlessisc.rightMargin
font['Dotlessi.sc'].mark = 200

font.update()

Message('Done building accents')
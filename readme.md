FontLab Scripts
===============

These following scripts were developed in 2005, right at the point when FontLab changed from version 4 to version 5. They mostly still work, and are being kept here for those who still find them useful. These were produced to aid my workflow at the time. Bug reports are very welcome, especially if they come with a patch. If you find them useful, a [donation](http://www.benkiel.com/typeDesign/) is kindly appreciated.

**Note**: All of these scripts require that [RoboFab](http://robofab.org) be installed. The scripts should be placed in your Macro folder.


###[Scripts for Accents](Accent Tools)
These scripts will aid in building accents, placing anchors, and removing anchors. **placeAnchor** will place anchors on selected glyphs with a name and height of your choosing. **removeAnchors** and **removeSelectedAnchors** remove either all the anchors from a font or the anchors on selected glyphs in a font. **buildAccents** will build accented characters from glyphs which have anchors. The list of accented glyphs it will build is editable. If you have more than one accent design (say, accents for capital letters and accents for lowercase letters) the script allows the placement of each on the proper glyph.

###[Better Generate Font](betterGenerateFont.py)
This script will make a copy of the font you are working on, remove its overlaps and decompose its characters, then give you the choice of font type to generate. After the font is generated, it deletes the copy, leaving your orignal vfb file untouched. This is very useful if you are developing a design using overlaps, and are tired of having to make a duplicate font to remove overlaps when you want to test your design.

###[Script for dealing with Guidelines](lowercase.py)
This example script shows how one can add and remove guidelines to a vfb file. Useful for dealing with fonts with a large number of different types of glyphs (small caps, non-latins, expanded accented character sets, etc.) when one doesn't want to clutter the glyph window with guides that one isn't using.

###[Scripts for working with font metrics](Metric tools)
These scripts make it easy to copy the sidebearing values of one vfb file to another. **copySidebearings** will copy the sidebearing values from one vfb to another. **copySidebearingsToMaster** will copy the sidebearings from a font to a specified master in a MM vfb. This is handy for when two fonts are combined into one MM vfb.

###[Scripts for MultipleMaster VFBs](Multiple Master tools)
MultipleMaster faces are wonderful tools for testing a typeface design, but generating a large number of instances for testing is a time consuming process. This script will quickly generate any number of instances of a MM face, either as font files or vfb files (or both).

###[Test text generation](Text generation)
An extremely fiddly (AWK!) way of making test test based on word length patterns of input text, for the limited character set your working typeface may have
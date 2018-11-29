# makeMoney
Python Board Game Money Maker - create your own money for your favorite board game.

This script does not just put an image on a page, no! It adds a serial number as well!

![ONE bill, two-sided](https://github.com/foreachthing/makeMoney/blob/master/scrshot-000.png)
This is a preview of the first (and second) page. You can specify the range of the serial number (and/or location, font* and size) between 0 and 2^31-1. Then each bill gets a random number assigned and it will come out zero-padded.

* more fonts to come


## Instructions

1. Create your on bills _(I took those bills from here: http://www.gunook.com/das-monopol-des-zauberers-harry-potter-monopoly/)_
1. [Download](https://github.com/foreachthing/makeMoney/archive/master.zip) or [clone](https://github.com/foreachthing/makeMoney.git) and run the python script with or without parameters (see below).
1. Print `yourMoney.pdf` duplex over the short edge.
1. Cut 'em out and enjoy your money.


## Requirements
* Python (3.6)
* LaTeX installation (LuaTeX from MiKTeX or TeX Live)

## Usage
```
usage: make_money.py [-h] [-d] [-ps str] [-bpp int] [-width float]
                     [-height float] [-dupoff X Y] [-sns int] [-sn START END]
                     [-snoff X Y] [-fsize float] [-font FONTNAME]
                     [-nop [NOP [NOP ...]]] [-bv [BV [BV ...]]] [-rec]

** Board Game Money-Maker ** Make your own custom money for your favorite
board game. Use the different options to customize your money-set. Use the
images stored in the "./bills" sub-directory.

optional arguments:
  -h, --help            show this help message and exit
  -d                    For debugging or testing only! Use the dummy image in
                        the subdirectory, rather than the real ones. Fontsize
                        is 3 times default, label is centered to page.
                        (Default: False)

Page and bill settings:
  -ps str               Printed paper size (page for printing is set to
                        landscape). Type "-ps ?" for a list of options.
                        Default: a4paper
  -bpp int              Number of bills per page. Note: make sure that all
                        your bills fit on one tow-column page. Default: 6
  -width float          Width of bill in [mm]. Image will be stretched if
                        value doesn't match actual width. Default: 130 mm
  -height float         Height of bill in [mm]. Image will be stretched if
                        value doesn't match actual height. Default: 60 mm
  -dupoff X Y           X Y offset, in mm, for duplex printing. This setting
                        helps with missaligned duplex printer. Default: ('0',
                        '0') mm

Serial Number Settings:
  -sns int              Define seed for randomness of serial numbers. Default:
                        a random (right now: 1104122974 - will be different
                        next time) number will be used.
  -sn START END         Start and end value of serial number. Minimum = 0,
                        Maximum = 2'147'483'647, default: (1, 2147483647).
  -snoff X Y            X Y offset, in mm and starting from the center, of
                        serial number label (default: ('-44', '-0.2') mm)
  -fsize float          Font size in mm. Default: 3.2 mm
  -font FONTNAME        Font for serial number label. Using the "Emerald"
                        package. Type "-font ?" for a list of options.
                        Warning: Font names are case sensitive! Default:
                        standard

Number of Pages of bills of each value:
  Maximum of 500 pages per bill. Recommended values: 20, 4, 8, 4, 4, 16 and
  8 pages. Example: "-nop 5 7 -bv 10 20" will create a document of 12 pages.
  5 pages of 10s and 7 pages of 20s.

  -nop [NOP [NOP ...]]  Number of pages of all the bills. Default: ('1', '1',
                        '1', '1', '1', '1', '1')
  -bv [BV [BV ...]]     List of Bill Values. Changes also required in "-nop"
                        and make sure your bill-image exists in the sub-
                        directory. Default: ('1', '5', '10', '20', '50',
                        '100', '500')
  -rec                  Use recommended number of pages of each bill value
                        (see above). This will override both of the above
                        settings. (Default: False)
```

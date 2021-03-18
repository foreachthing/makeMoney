# makeMoney
Board-Game Money-Maker - create/print your own money for your favorite (board) game.
This script also adds a "unique" serial number as well!

I made this script to create Money for the Harry Potter Monopoly(R) Board-Game found here: http://www.gunook.com/das-monopol-des-zauberers-harry-potter-monopoly/
Unfortunately, the links are all dead and I still don't have permission to post the orginial, hi-res images of the bills... I guess you have to come up with your own design.

![ONE bill, two-sided](https://github.com/foreachthing/makeMoney/blob/master/scrshot-000.png)
This is a preview of the first and second (front and back) page. You can specify the range of the serial number (and/or location, font(&ast;) and size) between 0 and 2^31-1. Then each bill gets a random(&ast;&ast;) number assigned and it will come out zero-padded.

(&ast;) Using the [Emerald](http://www.pirbot.com/mirrors/ctan/fonts/emerald/) package

(&ast;&ast;) Tried it with >10'000 numbers and no duplicates found!

### What it can do:
* Use different layouts for the front and the back side
* print only one value (i.e. only 100s bills)
* define how many pages you need of each bill
* define how many columns your bills should appear in (best results, if all rows/columns are completly filled)
* define range for serial number
* set font and font-size of your s/n
* accurately place the s/n on the front and on the back side
* set size of bill and paper to print them on
* if your duplex has accuracy problems, adjust for that
* 


## Instructions

1. Create your on bills _(I took those bills from here: http://www.gunook.com/das-monopol-des-zauberers-harry-potter-monopoly/)_
1. [Download](https://github.com/foreachthing/makeMoney/archive/master.zip) or [clone](https://github.com/foreachthing/makeMoney.git) and run the python script with or without parameters (see below).
1. Print `yourMoney.pdf` duplex over the short edge.
1. Cut 'em out and enjoy your money.

## Requirements
* Python (3.6)
* LaTeX installation (LuaTeX from MiKTeX or TeX Live)
* LaTeX required packages:
  * geometry
  * fontenc
  * emerald
  * tikz, with positioning
  * forloop
  * fmtcount
  * lcg
  * pdfpages

## Examples
1. To print the default settings: `python make_money.py`
1. To print 5 pages of 500s and 2 pages of 10s, you can use this command: `python make_money.py -nop 5 2 -bv 500 10`
1. To print serial numbers between 50'000 and 900'000, duplex offset x = 1 mm and the recommended number of pages of each bill, use this: `python make_money.py -sns 50000 900000 -dupoff 1 0 -rec`
1. To print a different (default front: money; default back: money-b) image on the back: `python make_money.py -frontback`



## Usage
```
c:\dev\makeMoney>make_money.py -h
usage: make_money.py [-h] [-d] [-pc] [-ps str] [-bpp int] [-col int]
                     [-width float] [-height float] [-dupoff X Y] [-s] [-sb]
                     [-sns int] [-sn START END] [-snoff X Y] [-fsize float]
                     [-font FONTNAME] [-snh] [-frontback] [-front str]
                     [-back str] [-snboffset X Y] [-nop [NOP ...]]
                     [-bv [BV ...]] [-rec]

** Board Game Money-Maker ** Make your own custom money for your favorite
board game or your kids. Use the different options to customize your money-
set. Use the images stored in the "./bills" sub-directory.

optional arguments:
  -h, --help      show this help message and exit
  -d              For debugging or testing only! Use the dummy image in the
                  subdirectory, rather than the real ones. Fontsize is 3 times
                  default, label is centered to page. (Default: False)
  -pc             For printer calibration only. Will print serial number as
                  with -d on example-image-a and example-image-b background
                  (from graphicx package). -nop and -bv are
                  overridden.(Default: False)

Page and bill settings:
  -ps str         Printed paper size (page for printing is set to landscape).
                  Type "-ps ?" for a list of options. Default: a4paper
  -bpp int        Number of bills per page. Note: make sure that all your
                  bills fit on one page. Default: 6
  -col int        Number of columns of bills per page (1-100). Note: make sure
                  that all your bills fit on one page. Default: 2
  -width float    Width of bill in [mm]. Image will be stretched if value
                  doesn't match actual width. Default: 130 mm
  -height float   Height of bill in [mm]. Image will be stretched if value
                  doesn't match actual height. Default: 60 mm
  -dupoff X Y     X Y offset, in mm, for duplex printing. This setting helps
                  with missaligned duplex printer. Default: ('0', '0') mm

Serial Number Settings:
  -s              Turn serial numbers off. (Default: False)
  -sb             Turn serial numbers on the back side off. (Default: False)
  -sns int        Define seed for randomness of serial numbers. Default: a
                  random (right now: 1312696195 - will change with next run)
                  number will be used.
  -sn START END   Start and end value of serial number. Minimum = 0, Maximum =
                  2'147'483'647, default: (1, 2147483647).
  -snoff X Y      X Y offset, in mm and starting from the center, of serial
                  number label (default: ('-44', '-0.2') mm)
  -fsize float    Font size in mm. Default: 3.2 mm
  -font FONTNAME  Font for serial number label. Using the "Emerald" package.
                  Type "-font ?" for a list of options. Warning: Font names
                  are case sensitive! Default: standard
  -snh            Print serial number as HEX number. (Default: False)

Use these options to use a different image for the front and back side:
  -frontback      If set, you need to specify "-front" and "-back" as well.
                  (Default: False)
  -front str      Front image prefix. Default: money -> money-1, money-5 etc.
  -back str       Back image prefix. Default: money-b -> money-b-1, money-b-5
                  etc.
  -snboffset X Y  X Y offset, in mm and starting from the center, of serial
                  number label for the BACK side (default: ('-44', '-0.2') mm)

Number of Pages of bills of each value:
  Maximum of 1000 pages per bill. Recommended values: 20, 4, 8, 4, 4, 16 and
  8 pages. Example: "-nop 5 7 -bv 10 20" will create a document of 12 pages.
  5 pages of 10s and 7 pages of 20s.

  -nop [NOP ...]  Abount of pages of all the bills. Default: ('20', '6', '8',
                  '6', '6', '16', '8')
  -bv [BV ...]    List of Bill Values. Changes also required in "-nop" and
                  make sure your bill-image exists in the sub-directory.
                  Default: ('1', '5', '10', '20', '50', '100', '500')
  -rec            Use recommended number of pages of each bill value (see
                  above). This will override both of the above settings.
                  (Default: False)

NOTE: Best results are with complete rows and columns (i.e.: 81 bpp = 9x9, 6
bpp = 2x3, etc.). If a row is incomplete, it can happen that the serial
numbers won't match anymore!
```

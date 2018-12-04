"""
    Make your own Board Game Money
"""
#!/usr/bin/python

import os
from pathlib import Path
import codecs
import subprocess
from shutil import copyfile
import argparse
import random # for seed
from collections import deque

# define files
DIR_PATH = Path(__file__).resolve().parent

MAXIMUM = 2147483647 # 2**31 - 1

LIST_OF_FONTS = dict([('Apicturealphabet', r'\ECFAPictureAlphabet'), \
    ('Augie', r'\ECFAugie'), \
    ('Decadence', r'\ECFDecadence'), \
    ('DecadenceWithoutTheDiamonds', r'\ECFDecadenceWithoutTheDiamonds'), \
    ('DecadenceCondensed', r'\ECFDecadenceCondensed'), \
    ('DecadenceInTheDark', r'\ECFDecadenceInTheDark'), \
    ('DecadenceITDCondensed', r'\ECFDecadenceInTheDarkCondensed'), \
    ('DecadenceInADifferentLight', r'\ECFDecadenceInADifferentLight'), \
    ('DecadenceITDCondensedMarquee', r'\ECFDecadenceInTheDarkCondensedMarquee'), \
    ('Intimacy', r'\ECFIntimacy'), \
    ('IntimacyDeux', r'\ECFIntimacyDeux'), \
    ('JD', r'\ECFJD'), \
    ('Movieola', r'\ECFMovieola'), \
    ('Movieolatitletype', r'\ECFMovieolaTitleType'), \
    ('Pookie', r'\ECFPookie'), \
    ('PookieT', r'\ECFPookieType'), \
    ('Skeetch', r'\ECFSkeetch'), \
    ('SpankysBungalow', r'\ECFSpankysBungalow'), \
    ('SpankysBungalowItalico', r'\ECFSpankysBungalowItalico'), \
    ('SpankysBungalowBlanco', r'\ECFSpankysBungalowBlanco'), \
    ('SpankysBungalowBlancoItalico', r'\ECFSpankysBungalowBlancoItalico'), \
    ('Syriac', r'\ECFSyriac'), \
    ('TallPaul', r'\ECFTallPaul'), \
    ('Teenspirit', r'\ECFTeenSpirit'), \
    ('Webster', r'\ECFWebster')])

def argumentparser():
    """ ArgumentParser """
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description='** Board Game Money-Maker ** Make your own custom money for your favorite ' \
            'board game. Use the different options to customize your money-set. Use the images ' \
            'stored in the "./bills" sub-directory.',
        allow_abbrev=False,
        epilog='')

    parser.add_argument('-d', action='store_true', default=False, \
    help='For debugging or testing only! Use the dummy image in the subdirectory, rather than ' \
        'the real ones. Fontsize is 3 times default, label is centered to page. '\
        '(Default: %(default)s)')

    grp_page = parser.add_argument_group('Page and bill settings')
    list_of_paper_formats = ['a0paper', 'a1paper', 'a2paper', 'a3paper', 'a4paper', 'a5paper', \
        'a6paper', 'b0paper', 'b1paper', 'b2paper', 'b3paper', 'b4paper', 'b5paper', 'b6paper', \
        'c0paper', 'c1paper', 'c2paper', 'c3paper', 'c4paper', 'c5paper', 'c6paper', 'b0j', \
        'b1j', 'b2j', 'b3j', 'b4j', 'b5j', 'b6j', 'ansiapaper', 'ansibpaper', 'ansicpaper', \
        'ansidpaper', 'ansiepaper', 'letterpaper', 'executivepaper', 'legalpaper']
    grp_page.add_argument('-ps', metavar='str', type=str, choices=list_of_paper_formats, \
        default='a4paper', help='Printed paper size (page for printing is set to landscape). ' \
        'Type "-ps ?" for a list of options. Default: %(default)s')
    grp_page.add_argument('-bpp', metavar='int', type=int, default=6, help='Number of bills '\
        'per page. Note: make sure that all your bills fit on one tow-column page. '\
        'Default: %(default)s')
    grp_page.add_argument('-width', metavar='float', type=float, default=130, \
        help='Width of bill in [mm]. Image will be stretched if value doesn\'t match '\
        'actual width. Default: %(default)s mm')
    grp_page.add_argument('-height', metavar='float', type=float, default=60, \
        help='Height of bill in [mm]. Image will be stretched if value doesn\'t '\
        'match actual height. Default: %(default)s mm')

    # Duplex offset ... my printer does not print duplex accurately.
    # * HP M277dw: 1, 0
    grp_page.add_argument('-dupoff', action='store', nargs=2, metavar=('X', 'Y'), \
        default=('0', '0'), type=float, help='X Y offset, in mm, for duplex printing. '\
        'This setting helps with missaligned duplex printer. Default: %(default)s mm')

    # Serial number settings
    grp_sn = parser.add_argument_group('Serial Number Settings')
    grp_sn.add_argument('-sns', metavar='int', type=int, default=random.randint(0, MAXIMUM), \
        help='Define seed for randomness of serial numbers. Default: a random (right now: '\
        '%(default)s - will be different next time) number will be used.')
    grp_sn.add_argument('-sn', nargs=2, metavar=('START', 'END'), default=(1, MAXIMUM), \
        type=int, help='Start and end value of serial number. Minimum = 0, Maximum = ' + \
        str(format(MAXIMUM, ',')).replace(',', "'") + ', default: %(default)s.')
    grp_sn.add_argument('-snoff', nargs=2, metavar=('X', 'Y'), default=('-44', '-0.2'), \
        type=float, help='X Y offset, in mm and starting from the center, of serial number '\
        'label (default: %(default)s mm)')
    grp_sn.add_argument('-fsize', metavar='float', type=float, default=3.2, \
        help='Font size in mm. Default: %(default)s mm')

    grp_sn.add_argument('-font', metavar='FONTNAME', type=str, default='standard', \
        choices=LIST_OF_FONTS.keys(), help='Font for serial number label. Using the '\
        '"Emerald" package. Type "-font ?" for a list of options. Warning: Font names '\
        'are case sensitive! Default: %(default)s')

    grp_layout = parser.add_argument_group('Use these options to use a '\
        'different image for the front and back side')
    grp_layout.add_argument('-frontback', action='store_true', default=False, \
        help='If set, you need to specify "-fron" and "-back" as well. (Default: %(default)s)')
    grp_layout.add_argument('-front', metavar='str', type=str, default='money', \
        help='Front image prefix. Default: %(default)s -> money-1, money-5 etc.')
    grp_layout.add_argument('-back', metavar='str', type=str, default='money-b', \
        help='Back image prefix. Default: %(default)s -> money-b-1, money-b-5 etc.')
    grp_layout.add_argument('-snboff', nargs=2, metavar=('X', 'Y'), default=('-44', '-0.2'), \
        type=float, help='X Y offset, in mm and starting from the center, of serial number '\
        'label for the BACK side (default: %(default)s mm)')

    grp_bills = parser.add_argument_group('Number of Pages of bills of each value', \
        'Maximum of 500 pages per bill. Recommended values: 20, 4, 8, 4, 4, 16 and 8 pages. '\
        'Example: "-nop 5 7 -bv 10 20" will create a document of 12 pages. '\
        '5 pages of 10s and 7 pages of 20s.')
    # 1, 5, 10, 20, 50, 100, 500
    grp_bills.add_argument('-nop', nargs='*', type=int, \
        default=('1', '1', '1', '1', '1', '1', '1'), \
        help='Number of pages of all the bills. Default: %(default)s')
    grp_bills.add_argument('-bv', nargs='*', type=int, \
        default=('1', '5', '10', '20', '50', '100', '500'), \
        help='List of Bill Values. Changes also required in "-nop" and make sure your '\
        'bill-image exists in the sub-directory. Default: %(default)s')

    grp_bills.add_argument('-rec', action='store_true', default=False, \
        help='Use recommended number of pages of each bill value (see above). '\
        'This will override both of the above settings. (Default: %(default)s)')

    try:
        # Make ARGS global
        args = parser.parse_args()

        # To get all defaults:
        all_defargs = {}
        for key in vars(args):
            all_defargs[key] = parser.get_default(key)

        return [args, all_defargs]

    except IOError as msg:
        parser.error(str(msg))


def makevalid(value, mini, maxi):
    """
        Make the passed arguments within a valid range
        and return the result.
    """
    temp_value = 0
    if value < mini:
        temp_value = mini
    elif value > maxi:
        temp_value = maxi
    else:
        temp_value = value
    return temp_value


def create_xwm_file(file_bills, totalpages):
    """
        This creates a required xwm file (watermark)
    """
    xwm_file = open(DIR_PATH/(file_bills + '.xwm'), 'w')
    xwm_file.write(r'\relax' + '\n'\
        r'\xwmnewlabel{xwmlastpage}{{}{' + str(totalpages) + r'}{\relax}{Doc-Start}{}}' + '\n')
    xwm_file.close()


def args_validator(args, all_defargs):
    """
        Validates and rewrites the passed arguments
    """
    imin = 0
    imax = MAXIMUM

    if args.rec:
        args.bv = all_defargs.get('bv')
        args.nop = ('20', '4', '8', '4', '4', '16', '8')  # all_defargs.get('nop')

    sn0 = makevalid(int(args.sn[0]), imin, imax)
    if int(args.sn[1]) <= sn0:
        sn1 = max
    else:
        sn1 = makevalid(int(args.sn[1]), imin, imax)
    args.sn = (sn0, sn1)

    args.sns = makevalid(int(args.sns), imin, imax)

    iminb = 0
    imaxb = 500

    if len(args.bv) != len(args.nop):
        print('Number of parameters for "-bv" and "-nop" must match.')
        exit(1)

    list_nop = []
    for i in range(len(args.nop)):
        list_nop.append(makevalid(int(args.nop[i]), iminb, imaxb))

    args.nop = list_nop

    args.bpp = makevalid(args.bpp, 1, imaxb) # bills per page





def main(args, all_defargs):
    """ MAIN """

    args_validator(args, all_defargs)

    totalpages = 0
    for i in range(len(args.nop)):
        totalpages += int(args.nop[i])


    file_bills = '1-main'
    file_print = '2-print'
    files_ext_tex = '.tex'

    create_xwm_file(file_bills, totalpages) # create a required (watermark) file
    create_tex_main(file_bills + files_ext_tex)
    create_printable_doc(totalpages, file_bills, (file_print + files_ext_tex))

    cmd = ['lualatex', '-output-directory', str(DIR_PATH), '-interaction=nonstopmode', \
        str(DIR_PATH/(file_bills + files_ext_tex))]

    # make two runs because of serial numbers
    for i in range(2):
        proc = subprocess.Popen(cmd)
        proc.communicate()
        if proc.returncode != 0:
            print('Something went wrong with ' + (file_bills + files_ext_tex))
            exit(1)

    retcode = proc.returncode
    if retcode == 0:
        cmd = ['lualatex', '-output-directory', str(DIR_PATH), '-interaction=nonstopmode', \
        str(DIR_PATH/(file_print + files_ext_tex))]
        proc = subprocess.Popen(cmd)
        proc.communicate()

        retcode = proc.returncode
        if retcode == 0:
            copyfile(str(DIR_PATH/(file_print + '.pdf')), str(DIR_PATH/'yourMoney.pdf'))

        else:
            print('Something went wrong with ' + (file_print + files_ext_tex))
            exit(1)

        os.remove(DIR_PATH/(file_bills + '.aux'))
        os.remove(DIR_PATH/(file_print + '.aux'))

        print('')
        print('*** all done!')
        print('Your file (yourMoney.pdf) is ready to be duplex-printed along the short edge...')

    else:
        print('Something went wrong with ' + (file_bills + files_ext_tex))
        exit(1)



def create_tex_main(file_bills):
    """
        Creates the bills with the serial numbers. One bill per page.
    """

    lbillvalues = ARGS.bv

    # get values from arguments
    shiftx = ARGS.snoff[0]
    shifty = ARGS.snoff[1]
    shiftbx = ARGS.snboff[0]
    shiftby = ARGS.snboff[1]
    fontsize = ARGS.fsize

    if ARGS.d:
        fontsize = round(ARGS.fsize * 3, 2)
        shiftx = 0
        shifty = 0
        shiftbx = 0
        shiftby = 0

    out = codecs.open(DIR_PATH/file_bills, 'w', encoding='utf8')
    out.write(r'\documentclass{article}' + '\n')
    out.write('\\usepackage[paperheight={1}mm, paperwidth={0}mm, margin=0pt]'\
        .format(ARGS.width, ARGS.height) + '{geometry}' + '\n')
    out.write(r'\usepackage[T1]{fontenc}' + '\n')
    out.write(r'\usepackage{emerald}' + '\n')

    if ARGS.font != 'standard':
        out.write(r'\DeclareRobustCommand{\thisfontsfamily}{%' + '\n')
        out.write(r'  \fontsize{' + str(fontsize) + r'mm}{' + str(fontsize + 1) + r'mm}' + \
        str(LIST_OF_FONTS.get(ARGS.font)) + r'\fontseries{m}\fontshape{n}\selectfont}' + '\n')
    else:
        out.write(r'\DeclareRobustCommand{\thisfontsfamily}{\fontsize{' + \
        str(fontsize) + r'mm}{' + str(fontsize + 1) + r'mm}\rmfamily\selectfont}' + '\n')

    out.write(r'\usepackage{tikz}' + '\n')
    out.write(r'\usetikzlibrary{positioning}' + '\n')
    out.write(r'\usepackage{forloop}' + '\n')
    out.write(r'\usepackage{fmtcount}' + '\n')
    out.write(r'\usepackage[first=' + str(ARGS.sn[0]) + ', last=' + str(ARGS.sn[1]) + \
        r', seed=' + str(ARGS.sns) + ', counter=serialnumber]{lcg}' + '\n')

    strdebug = ''
    strcol1 = 'lightgray'
    strcol2 = 'lightgray'
    if ARGS.d:
        strdebug = r' \thisfontsfamily #3 -- '
        if ARGS.frontback:
            strcol2 = 'yellow'

    out.write(r'\newcommand{\mypics}[3]{\rand\begin{tikzpicture}[remember picture,overlay]'\
        r'\node (thispage) [shape=rectangle, fill=' + strcol1 + \
        r', minimum height=\paperheight, minimum width=\paperwidth, anchor=center] '\
        r'at (current page.center) {};\node at (thispage.center) '\
        r'{\includegraphics[width=\paperwidth, height=\paperheight]{#1}};\node[xshift=' + \
        str(shiftx) + r'mm, yshift=' + str(shifty) + r'mm] at (thispage.center) '\
        r'{\thisfontsfamily' + strdebug + r'\padzeroes[10]{\decimal{serialnumber}}};'\
        r'\end{tikzpicture}\newpage\begin{tikzpicture}[remember picture,overlay]\node '\
        r'(thispage) [shape=rectangle, fill=' + strcol2 + r', minimum height=\paperheight, '\
        r'minimum width=\paperwidth, anchor=center] at (current page.center) {};\node at '\
        r'(thispage.center) {\includegraphics[width=\paperwidth, height=\paperheight]{#2}};'\
        r'\node[xshift=' + str(shiftbx) + r'mm, yshift=' + str(shiftby) + r'mm] at '\
        r'(thispage.center) {\thisfontsfamily' + strdebug + r'\padzeroes[10]{'\
        r'\decimal{serialnumber}}};\end{tikzpicture}\newpage}' + '\n')


    out.write(r'\newcounter{numpages}' + '\n')
    out.write(r'\pagestyle{empty}' + '\n')
    out.write(r'\begin{document}' + '\n')

    for i in range(len(ARGS.nop)):

        out.write(r'% % % ' + str(lbillvalues[i]) + '\n')
        out.write(r'\forloop{numpages}{1}{\value{numpages} < '+ \
            str(ARGS.nop[i] * int(ARGS.bpp) + 1) +'}{%' + '\n')

        if ARGS.d:
            out.write(r' \mypics{bills/dummy}{bills/dummy}{' + str(lbillvalues[i]) + '}' + '\n')
        else:
            if ARGS.frontback:
                out.write(r' \mypics{bills/' + ARGS.front + '-' + str(lbillvalues[i]) + \
                    r'}{bills/' + ARGS.back + '-' + str(lbillvalues[i]) + r'}{}' + '\n')
            else:
                out.write(r' \mypics{bills/money-' + str(lbillvalues[i]) + r'}{bills/money-' + \
                    str(lbillvalues[i]) + r'}{}' + '\n')

        out.write(r'}' + '\n\n')

    out.write(r'\end{document}' + '\n')
    out.close()


def create_printable_doc(totalpages, file_bills, file_print):
    """
        Creates the pdf-document with all the bills for duplex printing
    """

    out = codecs.open(DIR_PATH/file_print, 'w', encoding='utf8')
    out.write(r'% !TeX TS-program = lualatex' + '\n') # TeXstudio magic comment!
    out.write(r'\documentclass['+ ARGS.ps +', landscape]{article}' + '\n')
    out.write(r'\usepackage{pdfpages}' + '\n')
    out.write(r'\begin{document}' + '\n')

    ibpp = ARGS.bpp
    icol = 2 # FIXED VALUE!!! I'm not that good at math ... I don't need anything else.

    billsize = 'width=' + str(round(ARGS.width, 2)) + 'mm, height=' + \
        str(round(ARGS.height, 2)) + 'mm, '

    #
    #
    pgoffset = 0
    for _ in range(totalpages):
        ibppcheck = 0
        front_page = deque()
        back_page = deque()
        for ibillnum in range(pgoffset * ibpp, (pgoffset * ibpp) + 2 * ibpp):
            ibillnum += 1
            if ibppcheck < ibpp:
                if ibillnum % 2 == 0:
                    back_page.append(ibillnum)
                    ibppcheck += 1
                else:
                    front_page.append(ibillnum)

        # makes {8,10,12,2,4,6} out of {2,4,6,8,10,12}
        back_page.rotate(int(ibpp/2))

        strpage1 = r'\includepdf[pages={' + ', '.join(str(x) for x in front_page) + r'}, '\
            r'offset=0.0mm 0.0mm, noautoscale, ' + billsize + 'nup=' + str(icol) + 'x' + \
            str(int(ibpp / icol)) + r', pagecommand={\thispagestyle{empty}}, column=true, '\
            r'columnstrict=true]{' + file_bills + '}'

        strpage2 = r'\includepdf[pages={' + ', '.join(str(x) for x in back_page) + \
            '}, offset=' + str(round(float(ARGS.dupoff[0]), 2)) + 'mm ' + \
            str(round(float(ARGS.dupoff[1]), 2)) + 'mm, noautoscale, ' + billsize + \
            r'nup=' + str(icol) + 'x' + str(int(ibpp / icol)) + \
            r', pagecommand={\thispagestyle{empty}}, column=true, '\
            r'columnstrict=true]{' + file_bills + '}'

        out.write(strpage1 + '\n')
        out.write(strpage2 + '\n')

        pgoffset += 2

    #
    #

    out.write(r'\end{document}' + '\n')
    out.close()


ARGS, ALL_DEFARGS = argumentparser()
main(ARGS, ALL_DEFARGS)

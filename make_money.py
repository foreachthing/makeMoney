"""
    Make your own Board-Game Money
"""
#!/usr/bin/python

import os
from pathlib import Path
import codecs
import subprocess
from shutil import copyfile
import argparse
from collections import deque
import random

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
            'board game or your kids. Use the different options to customize your money-set. ' \
            'Use the images stored in the "./bills" sub-directory.',
        allow_abbrev=False,
        epilog='NOTE: '\
            'Best results are with complete rows and columns '\
            '(i.e.: 81 bpp = 9x9, 6 bpp = 2x3, etc.). If a row is incomplete, '\
            'it can happen that the serial numbers won\'t match anymore!')

    parser.add_argument('-d', action='store_true', default=False, \
    help='For debugging or testing only! Use the dummy image in the subdirectory, rather than ' \
        'the real ones. Fontsize is 3 times default, label is centered to page. '\
        '(Default: %(default)s)')
    
    parser.add_argument('-pc', action='store_true', default=False, \
    help='For printer calibration only. Will print serial number as with -d on example-image-a '\
        'and example-image-b background (from graphicx package). -nop and -bv are overridden.'\
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
        'per page. Note: make sure that all your bills fit on one page. '\
        'Default: %(default)s')
    grp_page.add_argument('-col', metavar='int', type=int, default=2, help='Number of columns '\
        'of bills per page (1-100). Note: make sure that all your bills fit on one page. '\
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

    # -s # turn serial numbers off
    grp_sn.add_argument('-s', action='store_true', default=False, \
        help='Turn serial numbers off. (Default: %(default)s)')

    # -sb # no serial numbers on the back side
    grp_sn.add_argument('-sb', action='store_true', default=False, \
        help='Turn serial numbers on the back side off. (Default: %(default)s)')

    # serial number seed
    grp_sn.add_argument('-sns', metavar='int', type=int, default=random.randint(0, MAXIMUM), \
        help='Define seed for randomness of serial numbers. Default: a random (right now: '\
        '%(default)s - will change with next run) number will be used.')

    # serial number START -> END value
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
    grp_sn.add_argument('-snh', action='store_true', default=False, \
        help='Print serial number as HEX number. (Default: %(default)s)')

    grp_layout = parser.add_argument_group('Use these options to use a '\
        'different image for the front and back side')
    grp_layout.add_argument('-frontback', action='store_true', default=False, \
        help='If set, you need to specify "-front" and "-back" as well. (Default: %(default)s)')
    grp_layout.add_argument('-front', metavar='str', type=str, default='money', \
        help='Front image prefix. Default: %(default)s -> money-1, money-5 etc.')
    grp_layout.add_argument('-back', metavar='str', type=str, default='money-b', \
        help='Back image prefix. Default: %(default)s -> money-b-1, money-b-5 etc.')
    grp_layout.add_argument('-snboffset', nargs=2, metavar=('X', 'Y'), default=('-44', '-0.2'), \
        type=float, help='X Y offset, in mm and starting from the center, of serial number '\
        'label for the BACK side (default: %(default)s mm)')

    grp_bills = parser.add_argument_group('Number of Pages of bills of each value', \
        'Maximum of 1000 pages per bill. Recommended values: 20, 4, 8, 4, 4, 16 and 8 pages. '\
        'Example: "-nop 5 7 -bv 10 20" will create a document of 12 pages. '\
        '5 pages of 10s and 7 pages of 20s.')
    # 1, 5, 10, 20, 50, 100, 500
    grp_bills.add_argument('-nop', nargs='*', type=int, \
        default=('20', '6', '8', '6', '6', '16', '8'), \
        help='Abount of pages of all the bills. Default: %(default)s')
    grp_bills.add_argument('-bv', nargs='*', type=int, \
        default=('1', '5', '10', '20', '50', '100', '500'), \
        help='List of Bill Values. Changes also required in "-nop" and make sure your '\
        'bill-image exists in the sub-directory. Default: %(default)s')

    grp_bills.add_argument('-rec', action='store_true', default=False, \
        help='Use recommended number of pages of each bill value (see above). '\
        'This will override both of the above settings. (Default: %(default)s)')

    try:
        args = parser.parse_args()
        
        # To get all defaults:
        all_defargs = {}
        for key in vars(args):
            all_defargs[key] = parser.get_default(key)

        return [args, all_defargs]

    except IOError as msg:
        parser.error(str(msg))

class Serialnumber:
    """ pylint thinks this would be better ... to out-source such things """

    def __init__(self, args):

        self._shiftx = args.snoff[0]
        self._shifty = args.snoff[1]
        self._shiftbx = args.snboffset[0]
        self._shiftby = args.snboffset[1]
        self._fontsize = args.fsize
        if args.d:
            self._fontsize = round(args.fsize * 3, 2)
            self._shiftx = 0
            self._shifty = 0
            self._shiftbx = 0
            self._shiftby = 0

    @property
    def shiftx(self):
        """ get/set shift-x """
        return self._shiftx
    @property
    def shifty(self):
        """ get/set shift-y """
        return self._shifty
    @property
    def shiftbx(self):
        """ get/set back side shift-x """
        return self._shiftbx
    @property
    def shiftby(self):
        """ get/set back side shift-x """
        return self._shiftby
    @property
    def fontsize(self):
        """ get/set font size in mm """
        return self._fontsize


def set_validrange(value, mini, maxi):
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
    xwm_file.write(r'\relax'+'\n'\
        r'\xwmnewlabel{xwmlastpage}{{}{' + str(totalpages) + r'}{\relax}{Doc-Start}{}}'+'\n')
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

    sn0 = set_validrange(int(args.sn[0]), imin, imax)
    if int(args.sn[1]) <= sn0:
        sn1 = max
    else:
        sn1 = set_validrange(int(args.sn[1]), imin, imax)
    args.sn = (sn0, sn1)

    # s/n seed
    args.sns = set_validrange(int(args.sns), imin, imax)

    # number of columsn
    args.col = set_validrange(int(args.col), 1, 100)

    iminb = 0
    imaxb = 1000

    if len(args.bv) != len(args.nop):
        print('Number of parameters for "-bv" and "-nop" must match.')
        exit(1)

    list_nop = []
    for i in range(len(args.nop)):
        list_nop.append(set_validrange(int(args.nop[i]), iminb, imaxb))

    args.nop = list_nop
    args.bpp = set_validrange(args.bpp, 1, imaxb) # bills per page


def make_backside_array(args, deq_input, irow, icol):
    """
        Makes the required array for mulitcolumn printing.
        Derived from:
        https://www.geeksforgeeks.org/python-slicing-reverse-array-groups-given-size/
    """

    # convert deque to list
    lst = list()
    for deq in deq_input:
        lst.append(deq)
    deq_input = lst

    # set starting index at 0
    start = int(0)

    # run a while loop len(input)/irow times
    # because there will be len(input)/k number
    # of groups of size irow
    result = []
    while start < len(deq_input):

        # if length of group is less than irow
        # that means we are left with only last
        # group reverse remaining elements
        if len(deq_input[start:]) < int(irow):
            result += list(reversed(deq_input[start:]))
            break

        # select current group of size of k
        # reverse it and concatenate
        result += list(reversed(deq_input[start:start + irow]))
        start += irow

    if args.bpp % icol != 0:
        dq_tmp = deque()
        [dq_tmp.append(i) for i in result] # DAMN YOU, pylint!
        dq_tmp.rotate(int(irow))
        result = dq_tmp
    else:
        result = reversed(result)

        dq_tmp = deque()
        [dq_tmp.append(i) for i in result] # pylint, you do like a vacuum does!
        result = dq_tmp

    return result


def create_printable_doc(args, totalpages, file_bills, file_print):
    """
        Creates the pdf-document with all the bills for duplex printing
    """

    out = codecs.open(DIR_PATH/file_print, 'w', encoding='utf8')
    out.write(r'% !TeX TS-program = lualatex'+'\n') # TeXstudio magic comment!
    out.write(r'\documentclass{article}'+'\n')
    out.write(r'\usepackage[landscape,'+ args.ps +']{geometry}'+'\n')    
    out.write(r'\usepackage{pdfpages}'+'\n')
    out.write(r'\begin{document}'+'\n')

    billsize = 'width=' + str(round(args.width, 2)) + 'mm, height=' + \
        str(round(args.height, 2)) + 'mm, '

    # Not every combination of rows/columns seem to work.
    # I'm not that good at math ...
    # It works best, if all rows and columns are completely filled.
    icol = int(args.col)
    ibpp = int(args.bpp)

    # number of rows in final pdf
    irow = int(args.bpp / icol)

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
                    # add all odd numbers
                    front_page.append(ibillnum)

        back_page = make_backside_array(args, back_page, irow, icol)

        # needs to add a place holder if the last row is incomplete
        if ibpp % icol != 0:
            irow = int((ibpp + 1) / icol)
            back_page.insert(irow - 1, '')
            front_page.insert(ibpp, '')

        out.write(r'\includepdf[pages={'+', '.join(str(x) for x in front_page) + r'}, '\
            r'offset=0.0mm 0.0mm, noautoscale, ' + billsize + 'nup=' + str(icol) + 'x' + \
            str(irow) + r', pagecommand={\thispagestyle{empty}}, column=true, '\
            r'columnstrict=true]{' + file_bills + '}'+'\n')

        out.write(r'\includepdf[pages={'+', '.join(str(x) for x in back_page) + \
            '}, offset=' + str(round(float(args.dupoff[0]), 2)) + 'mm ' + \
            str(round(float(args.dupoff[1]), 2)) + 'mm, noautoscale, ' + billsize + \
            r'nup=' + str(icol) + 'x' + str(irow) + \
            r', pagecommand={\thispagestyle{empty}}, column=true, '\
            r'columnstrict=true]{' + file_bills + '}'+'\n')

        pgoffset += 2
    #
    #

    out.write(r'\end{document}'+'\n')
    out.close()


def main(args, all_defargs):
    """
        MAIN
    """

    args_validator(args, all_defargs)
    
    # If user wants to calibrate his/her printer:
    if args.pc:
        args.d = True
        args.nop = [1]
        args.bv = [1]

    totalpages = 0
    for i in range(len(args.nop)):
        totalpages += int(args.nop[i])

    file_bills = '1-main'
    file_print = '2-print'
    files_ext_tex = '.tex'

    create_xwm_file(file_bills, totalpages) # create a required (watermark) file
    create_tex_main(args, file_bills + files_ext_tex)
    create_printable_doc(args, totalpages, file_bills, (file_print + files_ext_tex))

    cmd = ['lualatex', '-output-directory', str(DIR_PATH), '-interaction=nonstopmode', \
        str(DIR_PATH/(file_bills + files_ext_tex))]

    # make two runs because of some weird sht with the bills....?!?
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

        remove_files = ["aux", "pdf", "log", "tex", "xwm"]
        for rmfile in remove_files:
            try:              
                os.remove(DIR_PATH/(file_bills + '.' + rmfile))
                os.remove(DIR_PATH/(file_print + '.' + rmfile))
            except OSError as e:
                print('')
            
        print('')
        print('*** all done!')
        print('Your file (yourMoney.pdf) is ready to be duplex-printed along the short edge...')

    else:
        print('Something went wrong with ' + (file_bills + files_ext_tex))
        exit(1)


# Print iterations progress
def print_progress_bar(iteration, total, prefix=''):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    suffix = ''
    decimals = 1
    length = 50 # int((os.get_terminal_size(1).columns - 20) / 2)
    fill = '█'

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledlength = int(length * iteration // total)
    pbar = fill * filledlength + '-' * (length - filledlength)
    print('\r%s |%s| %s%% %s' % (prefix, pbar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def get_random_list(args):
    """
        pylint ... I don't like you anymore
    """
    itotalallbills = 0
    for i in range(len(args.nop)):
        itotalallbills += args.nop[i] * args.bpp
    print('\n### Total Bills: {0}\n'.format(str(itotalallbills)))

    random.seed(args.sns)
    lstserial = list()
    newmaxsn = args.sn[1]
    if itotalallbills > (args.sn[1] - args.sn[0]):
        newmaxsn = args.sn[1] + args.sn[0] + itotalallbills

    print()

    cnt = 0
    while len(lstserial) < itotalallbills:
        rnd = random.randint(args.sn[0], newmaxsn)
        if rnd not in lstserial:
            lstserial.append(rnd)
            cnt += 1
            if itotalallbills > 2000:
                print_progress_bar(cnt, itotalallbills, prefix='Randomizing: ')

    return lstserial


def create_tex_main(args, file_bills):
    """
        Creates the bills with the serial numbers. One bill per page.
    """

    out = codecs.open(DIR_PATH/file_bills, 'w', encoding='utf8')
    out.write(r'\documentclass{article}'+'\n')
    out.write('\\usepackage[paperheight={1}mm, paperwidth={0}mm, margin=0pt]'\
        .format(args.width, args.height) + '{geometry}'+'\n')

    out.write(r'\usepackage{tikz}'+'\n')
    out.write(r'\usetikzlibrary{positioning}'+'\n')

    get_serialnumber_setting(args, out)

    out.write(r'\pagestyle{empty}'+'\n')
    out.write(r'\begin{document}'+'\n')

    lbillvalues = args.bv

    lstserial = get_random_list(args)

    print('\n')

    cnt = 0
    snum = ''
    padlen = len(str(args.sn[1]))

    for i in range(len(args.nop)):

        out.write(r'% % % ' + str(lbillvalues[i]) + '\n')

        itotalbills = args.nop[i] * args.bpp # total bills of current value
        itb = range(0, itotalbills)
        scnt = 0

        while scnt < len(itb):

            if args.snh:
                snum = '{:02X}'.format(lstserial[cnt])
            else:
                snum = str(lstserial[cnt]).zfill(padlen)

            if args.d:
                out.write(r'\mypics{example-image-a}{example-image-b}{' + \
                    str(lbillvalues[i]) + '}{' + (snum) + r'}'+'\n')
            else:
                if not args.s:
                    if args.frontback:
                        out.write(r' \mypics{bills/' + args.front + '-' + str(lbillvalues[i]) +\
                            r'}{bills/' + args.back + '-' + str(lbillvalues[i]) +\
                            r'}{}{' + snum + r'}'+'\n')
                    else:
                        out.write(r' \mypics{bills/money-' + str(lbillvalues[i]) + r'}'\
                            r'{bills/money-' + str(lbillvalues[i]) + r'}{}{' + snum + r'}'+'\n')
                else:
                    if args.frontback:
                        out.write(r' \mypics{bills/' + args.front + '-' + str(lbillvalues[i]) +\
                            r'}{bills/' + args.back + '-' + str(lbillvalues[i]) + r'}{}{}'+'\n')
                    else:
                        out.write(r' \mypics{bills/money-' + str(lbillvalues[i]) + r'}'\
                            r'{bills/money-' + str(lbillvalues[i]) + r'}{}{}'+'\n')
            scnt += 1
            cnt += 1

        out.write('\n\n')

    out.write(r'\end{document}'+'\n')
    out.close()


def print_serialnumbers(args, out, xyf, strdebug):
    """
        do this, if the user wants serial numbers on front and back
    """

    debugtext = ''
    debugnode = ''
    if args.d:
        debugtext = r', text=black, font=\bfseries'
        debugnode = '\t'+r'\node[opacity=.35] at (thispage.center) '
    else:
        debugnode = '\t'+r'\node at (thispage.center) '

    out.write(r'\newcommand{\mypics}[4]{'+'\n'\
        r'  \begin{tikzpicture}[remember picture,overlay]'+'\n'\
        '\t'+r'\node (thispage) [shape=rectangle'\
        r', minimum height=\paperheight, minimum width=\paperwidth, anchor=center] '\
        r'at (current page.center) {};'+'\n')

    out.write(debugnode)
    out.write(r'{\includegraphics[width=\paperwidth, height=\paperheight]{#1}};'+'\n'\
        '\t'+r'\node[xshift='+\
        str(xyf.shiftx) + r'mm, yshift=' + str(xyf.shifty) + r'mm' + debugtext +\
        r'] at (thispage.center) '\
        r'{\thisfontsfamily' + strdebug + r'#4};'+'\n'\
        r'  \end{tikzpicture}'+'\n'\
        r'  \newpage'+'\n'\
        r'  \begin{tikzpicture}[remember picture, overlay]'+'\n'\
        '\t'+r'\node (thispage) [shape=rectangle, minimum height=\paperheight, '\
        r'minimum width=\paperwidth, anchor=center] at (current page.center) {};'+'\n')

    out.write(debugnode)
    out.write(r'{\includegraphics[width=\paperwidth, height=\paperheight]{#2}};'+'\n'\
        '\t'+r'\node[xshift=' + str(xyf.shiftbx) + r'mm, yshift=' + str(xyf.shiftby) + r'mm' +\
        debugtext + r'] at '\
        r'(thispage.center) {\thisfontsfamily' + strdebug + r'#4};'+'\n'\
        r'  \end{tikzpicture}'+'\n'+r'  \newpage'+'\n}'+'\n')


def print_no_serial_on_backside(out, xyf, strdebug):
    """
        do this, if the user doesn't want serial numbers on the back of the bills
    """
    # if serial number on front and back
    out.write(r'\newcommand{\mypics}[4]{'+'\n'\
        r'  \begin{tikzpicture}[remember picture,overlay]'+'\n'\
        '\t'+r'\node (thispage) [shape=rectangle'\
        r', minimum height=\paperheight, minimum width=\paperwidth, anchor=center] '\
        r'at (current page.center) {};'+'\n'\
        '\t'+r'\node at (thispage.center) '\
        r'{\includegraphics[width=\paperwidth, height=\paperheight]{#1}};'+'\n'\
        '\t'+r'\node[xshift='+\
        str(xyf.shiftx) + r'mm, yshift=' + str(xyf.shifty) + r'mm] at (thispage.center) '\
        r'{\thisfontsfamily' + strdebug + r'#4};'+'\n'\
        r'  \end{tikzpicture}'+'\n'\
        r'  \newpage'+'\n'\
        r'  \begin{tikzpicture}[remember picture,overlay]'+'\n'\
        '\t'+r'\node (thispage) [shape=rectangle, minimum height=\paperheight, '\
        r'minimum width=\paperwidth, anchor=center] at (current page.center) {};'+'\n'\
        '\t'+r'\node at '\
        r'(thispage.center) {\includegraphics[width=\paperwidth, height=\paperheight]{#2}};'+'\n'\
        r'  \end{tikzpicture}'+'\n'+r'  \newpage'+'\n}'+'\n')


def print_no_serial(args, out):
    """
        do this, if the user doesn't want serial numbers on hers/his bills
    """
    # if NO serial number on front AND back
    if args.d:
        out.write(r'\newcommand{\mypics}[3]')
    else:
        out.write(r'\newcommand{\mypics}[2]')

    out.write('{%'+'\n'+r'\begin{tikzpicture}[remember picture,overlay]'+'\n'\
        '\t' + r'\node (thispage) [shape=rectangle'\
        r', minimum height=\paperheight, minimum width=\paperwidth, anchor=center] '\
        r'at (current page.center) {};'+'\n'\
        '\t' + r'\node at (thispage.center) '\
        r'{\includegraphics[width=\paperwidth, height=\paperheight]{#1}};'+'\n')
    if args.d:
        out.write('\t'+r'\node [anchor=south] at (thispage.south) {\thectdebugger - #3};'+'\n')
    out.write(r'\end{tikzpicture}'+'\n')
    if args.d:
        out.write(r'\stepcounter{ctdebugger}'+'\n')
    out.write(r'\newpage'+'\n' \
        r'\begin{tikzpicture}[remember picture,overlay]'+'\n'\
        '\t' + r'\node (thispage) [shape=rectangle' + r', '\
        r'minimum height=\paperheight, '\
        r'minimum width=\paperwidth, anchor=center] at (current page.center) {};'+'\n'\
        '\t' + r'\node at (thispage.center) '\
        r'{\includegraphics[width=\paperwidth, height=\paperheight]{#2}};')

    if args.d:
        out.write(r'\node [anchor=south] at (thispage.south) {\thectdebugger - #3};'+'\n')

    out.write(r'\end{tikzpicture}'+'\n'+r'\newpage}'+'\n')


def get_serialnumber_setting(args, out):
    """
        silly pylint - too many branches ... don't like big trees?!
    """

    # get serialnumber settings from arguments
    xyf = Serialnumber(args)

    out.write(r'\usepackage[T1]{fontenc}'+'\n')
    out.write(r'\usepackage{emerald}'+'\n')

    if not args.s:
        if args.font != 'standard':
            out.write(r'\DeclareRobustCommand{\thisfontsfamily}{%'+'\n')
            out.write(r'  \fontsize{' + str(xyf.fontsize) + r'mm}{' + \
                str(xyf.fontsize + 1) + r'mm}' + str(LIST_OF_FONTS.get(args.font)) + \
                r'\fontseries{m}\fontshape{n}\selectfont}'+'\n')
        else:
            out.write(r'\DeclareRobustCommand{\thisfontsfamily}{\fontsize{' + \
            str(xyf.fontsize) + r'mm}{' + str(xyf.fontsize + 1) + \
                r'mm}\rmfamily\selectfont}'+'\n')

    strdebug = ''
    if args.d:
        strdebug = r' \thisfontsfamily #3 -- '
                
    if not args.s and not args.sb:
        # if serial number on front and back
        print_serialnumbers(args, out, xyf, strdebug)
    elif args.sb:
        # if serial number on front and back
        print_no_serial_on_backside(out, xyf, strdebug)
    else:
        # if NO serial number on front AND back
        print_no_serial(args, out)



ARGS, ALL_DEFARGS = argumentparser()
main(ARGS, ALL_DEFARGS)

# final endline

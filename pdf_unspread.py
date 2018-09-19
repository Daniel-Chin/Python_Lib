#!/usr/bin/env python

'''
Downloaded from: https://github.com/pmaupin/pdfrw
with minor modification by Daniel Chin for friendlier command-line calling

usage: py -m pdf_unspread my.pdf

Creates unspread.my.pdf

Chops each page in half, e.g. if a source were
created in booklet form, you could extract individual
pages.
'''

import sys
import os

from pdfrw import PdfReader, PdfWriter, PageMerge
from jdt import Jdt

def splitpage(src, ratio = .5):
    ''' Split a page into two (left and right)
    '''
    # Yield a result for each half of the page
    yield PageMerge().add(src, viewrect=(0, 0, ratio, 1)).render()
    yield PageMerge().add(src, viewrect=(ratio, 0, 1-ratio, 1)).render()

if __name__ == '__main__':
    inp = sys.argv[1:]
    if inp == []:
        inpfn = input('path/file.ext = ')
    else:
        inpfn, = inp
    outfn = os.path.join(os.path.dirname(inpfn), 'unspread.' + os.path.basename(inpfn))
    writer = PdfWriter(outfn)
    pages = PdfReader(inpfn).pages
    ratio = input('Ratio (default 0.5) = ')
    if ratio == '':
        mySplitpage = splitpage
    else:
        ratio = float(ratio)
        mySplitpage = lambda page : splitpage(page, ratio)
    jdt = Jdt(len(pages))
    for i, page in enumerate(pages):
        writer.addpages(mySplitpage(page))
        jdt.acc()
    writer.write()
    jdt.complete()

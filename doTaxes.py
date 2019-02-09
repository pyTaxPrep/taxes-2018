#! /usr/bin/python
#    Copyright (C) 2019 pyTaxPrep
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import forms.s_1040
import forms.s1_1040
import forms.s3_1040
import forms.s4_1040
import forms.s5_1040
import forms.a_1040
import forms.b_1040
import forms.se_1040
import forms.cez_1040
import forms.sep_ira
import forms.f_8606
import forms.s_1040v
import forms.tax_worksheet

from PyPDF2 import PdfFileMerger
import argparse
import sys
import os

def main():
            
    parser = argparse.ArgumentParser(description='A python based tax filing solution')
    fill_forms()

    print('Your tax forms are now filled out, and available in the filled directory.')

def fill_forms():
    forms.s_1040.fill_in_form()
    forms.s1_1040.fill_in_form()
    forms.s3_1040.fill_in_form()
    forms.s4_1040.fill_in_form()
    forms.s5_1040.fill_in_form()
    forms.a_1040.fill_in_form()
    forms.b_1040.fill_in_form()
    forms.se_1040.fill_in_form()
    forms.cez_1040.fill_in_form()
    forms.sep_ira.fill_in_form()
    forms.f_8606.fill_in_form()
    forms.s_1040v.fill_in_form()
    forms.tax_worksheet.fill_in_form()

    pdfs = [ os.path.join('filled', 'f1040.pdf'),
             os.path.join('filled', 'f1040s1.pdf'),
             os.path.join('filled', 'f1040s3.pdf'),
             os.path.join('filled', 'f1040s4.pdf'),
             os.path.join('filled', 'f1040s5.pdf'),
             os.path.join('filled', 'tax_worksheet.pdf'),
             os.path.join('filled', 'f1040sa.pdf'),
             os.path.join('filled', 'f1040sb.pdf'),
             os.path.join('filled', 'f1040sce.pdf'),
             os.path.join('filled', 'f1040sse.pdf'),
             os.path.join('filled', 'f8606.pdf'),
             os.path.join('filled', 'f1040v.pdf'),
             os.path.join('filled', 'SEP_IRA_Worksheet.pdf')]

    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(open(pdf, 'rb'))

    with open( os.path.join('filled', 'Tax_Return.pdf'), 'wb' ) as fd:
        merger.write(fd)


if __name__ == '__main__':
    main()

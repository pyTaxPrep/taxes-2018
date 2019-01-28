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
import forms.s4_1040
import forms.s5_1040
import forms.a_1040
import forms.b_1040
import forms.se_1040
import forms.cez_1040
import forms.sep_ira
import forms.f_8606
import argparse
import sys

def main():
            
    fill_forms()
    print('Your tax forms are now filled out and available in the filled directory.')

def fill_forms():
    forms.s_1040.fill_in_form()
    forms.s1_1040.fill_in_form()
    forms.s4_1040.fill_in_form()
    forms.s5_1040.fill_in_form()
    forms.a_1040.fill_in_form()
    forms.b_1040.fill_in_form()
    forms.se_1040.fill_in_form()
    forms.cez_1040.fill_in_form()
    forms.sep_ira.fill_in_form()
    forms.f_8606.fill_in_form()

if __name__ == '__main__':
    main()

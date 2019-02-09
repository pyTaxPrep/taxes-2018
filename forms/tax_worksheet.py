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
'''
Fills in the "Qualified Dividends and Capital Gains Tax Worksheet" to compute
tax due.

(Note: the version it fills in is from 2017; the same version is used for 2018,
just with different line numbers.)

Relies on the following forms:
    - Form 1040 (through line 10)
    - Schedule 1
'''


from . import utils
from . import s_1040
from . import s1_1040

data = utils.parse_values()

###################################


def build_data():

    form_1040  = s_1040.build_data(short_circuit = 'Tax Worksheet')
    schedule_1 = s1_1040.build_data()

    data_dict = {}

    line_1 = utils.dollars_cents_to_float(form_1040['taxable_income_dollars'],
                                          form_1040['taxable_income_cents'])
    data_dict['form1040_line10'] = line_1

    line_2 = utils.dollars_cents_to_float(form_1040['qualified_dividends_dollars'],
                                          form_1040['qualified_dividends_cents'])
    data_dict['form1040_line3a'] = line_2

    line_3 = utils.dollars_cents_to_float(schedule_1['capital_gain_dollars'],
                                          schedule_1['capital_gain_cents'])
    data_dict['filing_schedule_d_n'] = True
    data_dict['schedule1_line13'] = line_3

    line_4 = line_2 + line_3
    data_dict['line_4'] = line_4

    line_5 = 0
    data_dict['line_5'] = line_5

    line_6 = line_4 - line_5
    data_dict['line_6'] = line_6

    line_7 = line_1 - line_6
    data_dict['line_7'] = line_7

    line_8 = 38600
    data_dict['line_8'] = line_8

    line_9 = min(line_1, line_8)
    data_dict['line_9'] = line_9

    line_10 = min(line_7, line_9)
    data_dict['line_10'] = line_10

    line_11 = line_9 - line_10
    data_dict['line_11'] = line_11

    line_12 = min(line_1, line_6)
    data_dict['line_12'] = line_12

    line_13 = line_11
    data_dict['line_13'] = line_13

    line_14 = line_12 - line_13
    data_dict['line_14'] = line_14

    line_15 = 425800
    data_dict['line_15'] = line_15

    line_16 = min(line_1, line_15)
    data_dict['line_16'] = line_16

    line_17 = line_7 + line_11
    data_dict['line_17'] = line_17

    line_18 = line_16 - line_17
    if line_18 < 0:
        line_18 = 0
    data_dict['line_18'] = line_18

    line_19 = min(line_14, line_18)
    data_dict['line_19'] = line_19
    
    line_20 = line_19 * 0.15
    data_dict['line_20'] = line_20

    line_21 = line_11 + line_19
    data_dict['line_21'] = line_21

    line_22 = line_12 - line_21
    data_dict['line_22'] = line_22

    line_23 = line_22 * 0.20
    data_dict['line_23'] = line_23

    line_24 = utils.calculate_tax_due(line_7)
    data_dict['tax_table_amount_line7'] = line_24

    line_25 = line_20 + line_23 + line_24
    data_dict['line_25'] = line_25

    line_26 = utils.calculate_tax_due(line_1)
    data_dict['tax_table_amount_line1'] = line_26

    line_27 = min(line_25, line_26)
    data_dict['final_tax_on_income'] = line_27
    
    for k in data_dict:
        if type(data_dict[k]) == type(0.0):
            data_dict[k] = int( round(data_dict[k], 0) )

    data_dict['final_tax_on_income_unrounded'] = line_27
    return data_dict

def fill_in_form():
    data_dict = build_data()
    basename = 'tax_worksheet.pdf'
    utils.write_fillable_pdf(basename, data_dict, 'tax_worksheet.keys')


if __name__ == '__main__':
    fill_in_form()




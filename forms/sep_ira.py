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
Computes a SEP IRA contribution amount.

Relies on the Schedule SE and Schedule C forms.

Additionally, you must define 'sep_percentage' in data.json
with the percentage you want to contribute (up to 20).
'''

from . import utils
from . import se_1040
from . import cez_1040

data = utils.parse_values()

###################################

def build_data():

    schedule_se = se_1040.build_data()
    schedule_c = cez_1040.build_data()

    data_dict = {}

    data_dict['percentage']        = '%.2f' % (data['sep_percentage'])
    data_dict['factor']            = '%.2f' % (1 + data['sep_percentage'])
    
    profits = utils.dollars_cents_to_float(schedule_c['net_profit_dollars'],
                                           schedule_c['net_profit_cents'])
    se_deduction = utils.dollars_cents_to_float(schedule_se['_se_deduction_dollars'],
                                                schedule_se['_se_deduction_cents'])
    adj_profits = profits - se_deduction
    adj_earned = adj_profits / float(data_dict['factor'])
    max_earned = 280000.0
    final_earned = min(adj_earned, max_earned)
    prelim_contrib_amt = data['sep_percentage'] * final_earned
    max_contrib_amt = 56000.0
    final_contrib_amt = min(max_contrib_amt, prelim_contrib_amt)

    data_dict['profits']            = '%.2f' % (profits)
    data_dict['se_deduction']       = '%.2f' % (se_deduction)
    data_dict['adj_profits']        = '%.2f' % (adj_profits)
    data_dict['adj_earned']         = '%.2f' % (adj_earned)
    data_dict['max_earned']         = '%.2f' % (max_earned)
    data_dict['final_earned']       = '%.2f' % (final_earned)
    data_dict['prelim_contrib_amt'] = '%.2f' % (prelim_contrib_amt)
    data_dict['max_contrib_amt']    = '%.2f' % (max_contrib_amt)
    data_dict['final_contrib_amt']  = '%.2f' % (final_contrib_amt)

    return data_dict

def fill_in_form():
    data_dict = build_data()
    basename = 'SEP_IRA_Worksheet.pdf'

    for each in data_dict:
        data_dict[each] = data_dict[each].replace('.', '')

    utils.write_fillable_pdf(basename, data_dict, 'sep_ira.keys')


if __name__ == '__main__':
    fill_in_form()




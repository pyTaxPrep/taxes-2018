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
Fills in a Form 1040 Schedule 1.

Relies on the following forms:
    - Schedule C-EZ
    - Schedule SE
    - SEP IRA Worksheet

The following values must be defined in data.json (in addition to any
requirements for the forms listed above):
    => name
    => ssn

Currently, it'll fill in lines for business income and the
self-employment tax and SEP IRA contribution deductions.

'''

from . import utils
from . import cez_1040
from . import se_1040
from . import sep_ira

data = utils.parse_values()

###################################
    
def build_data():

    schedule_c  = cez_1040.build_data()
    schedule_se = se_1040.build_data()
    sep_calcs   = sep_ira.build_data()

    data_dict = {
        'name'             : data['name'],
        'ssn'              : data['ssn'],
        }

    # Set income and adjustment lines here
    data_dict['business_dollars'] = schedule_c['net_profit_dollars']
    data_dict['business_cents'] = schedule_c['net_profit_cents']

    data_dict['self_employment_dollars'] = schedule_se['_se_deduction_dollars']
    data_dict['self_employment_cents'] = schedule_se['_se_deduction_cents']

    if '1099_div' in data:
        utils.add_keyed_float( sum( [ x['total_capital_gain'] for x in data['1099_div'] ] ),
                               'capital_gain',
                               data_dict)

        data_dict['schedule_d_unneeded_y'] = True

    data_dict['sep_dollars'], data_dict['sep_cents'] =\
        utils.float_to_dollars_cents(float(sep_calcs['final_contrib_amt']))

    # Sum up the incomes and adjustments entered above.
    incomes = ['refund', 'alimony', 'business', 
               'capital_gain', 'other_gains',
               'rental', 'farm', 'unemployment',
               'other_income']

    utils.add_keyed_float(utils.add_fields(data_dict, incomes),
                          'sum_income',
                          data_dict)

    adjustments = ['educator', 'business_expenses',
                   'hsa', 'moving', 'self_employment',
                   'sep', 'se_health', 'early_penalty',
                   'alimony', 'ira', 'loan_interest']

    utils.add_keyed_float(utils.add_fields(data_dict, adjustments),
                          'adjustments',
                          data_dict)

    return data_dict

def fill_in_form():
    data_dict = build_data()
    basename = 'f1040s1.pdf'
    utils.write_fillable_pdf(basename, data_dict, 's1.keys')


if __name__ == '__main__':
    fill_in_form()




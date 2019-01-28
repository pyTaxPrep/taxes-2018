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
Fills in a Schedule B form.

Relies on portions of the Form 1040 (up to the line computing AGI).
Additionally, you must define the following keys in data.json:
    => name
    => ssn
    => 1099_div
    => 1099_int

Currently, the following lines are filled:
    => Interest lines 1, 2, and 4. (3 is filled but hard coded to 0.)
    => Dividends lines 5 and 6.
    => Lines 7a, 7b, and 8 are set to "No"
'''

from . import utils

data = utils.parse_values()

###################################

def build_data():

    data_dict = {
        'name'             : data['name'],
        'ssn'              : data['ssn']
        }

    interests = ['interest_' + str(x) for x in range(1, 15)]
    dividends = ['dividend_' + str(x) for x in range(1, 17)]

    for i, d in enumerate(data['1099_int']):
        utils.add_keyed_float(d['interest_income'], interests[i], data_dict)
        data_dict[interests[i] + '_name'] = d['institution']

    for i, d in enumerate(data['1099_div']):
        utils.add_keyed_float(d['total_ordinary'], dividends[i], data_dict)
        data_dict[dividends[i] + '_name'] = d['institution']

    total_interest = sum( [ x['interest_income'] for x in data['1099_int'] ] )
    utils.add_keyed_float(total_interest, 'interest_sum', data_dict)

    utils.add_keyed_float(0, 'interest_ex', data_dict)

    utils.add_keyed_float(total_interest, 'interest_total', data_dict)

    total_dividend = sum( [ x['total_ordinary'] for x in data['1099_div'] ] )
    utils.add_keyed_float(total_dividend, 'dividend_total', data_dict)

    data_dict['foreign_acct_n']  = True
    data_dict['fbar_needed_n']   = True
    data_dict['foreign_trust_n'] = True

    return data_dict

def fill_in_form():
    data_dict = build_data()
    basename = 'f1040sb.pdf'
    utils.write_fillable_pdf(basename, data_dict, 'sb.keys')


if __name__ == '__main__':
    fill_in_form()




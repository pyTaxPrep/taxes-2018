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
Fills in a Form 1040 Schedule 5.

The following values must be defined in data.json (in addition to any
requirements for the forms listed above):
    => name
    => ssn

Additionally, you can define 'estimated_fed' in data.json with details
about federal estimated tax payments.

Currently, it'll fill in the line for estimated federal tax payments.
'''

from . import utils

data = utils.parse_values()

###################################
    
def build_data():

    data_dict = {
        'name'             : data['name'],
        'ssn'              : data['ssn'],
        }

    # Set other payments / refundable credit lines here
    if 'estimated_fed' in data:
        estimated_federal = sum( [ x['amount'] for x in data['estimated_fed'] ] )
        utils.add_keyed_float(estimated_federal, 'estimated_tax', data_dict)

    # Sum other payments and refundable credits
    credits = ['estimated_tax', 'net_premium',
               'extension', 'excess_withheld',
               'fuel_credit',
               'credits']

    utils.add_keyed_float(utils.add_fields(data_dict, credits),
                          'total_credits',
                          data_dict)

    return data_dict

def fill_in_form():
    data_dict = build_data()
    basename = 'f1040s5.pdf'
    utils.write_fillable_pdf(basename, data_dict, 's5.keys')


if __name__ == '__main__':
    fill_in_form()




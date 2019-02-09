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
Fills in a Form 1040 Schedule 4.

Relies on the following forms:
    - Schedule SE

The following values must be defined in data.json (in addition to any
requirements for the forms listed above):
    => name
    => ssn

Currently, it'll fill in the line for the self employment tax.
'''


from . import utils
from . import se_1040

data = utils.parse_values()

###################################



    
def build_data():

    schedule_se = se_1040.build_data()

    data_dict = {
        'name'             : data['name'],
        'ssn'              : data['ssn'],
        }

    # Set tax lines here
    data_dict['se_tax_dollars'], data_dict['se_tax_cents'] =\
        schedule_se['_se_tax_dollars'], schedule_se['_se_tax_cents']

    # Sum up taxes
    taxes = ['se_tax', 'ss_medicare', 'retirements',
             'household_emp', 'homebuyer', 
             'healthcare',
             'additional_taxes',
             'net_tax_liability']

    utils.add_keyed_float(utils.add_fields(data_dict, taxes),
                          'total_other_taxes',
                          data_dict )

    return data_dict

def fill_in_form():
    data_dict = build_data()
    basename = 'f1040s4.pdf'
    utils.write_fillable_pdf(basename, data_dict, 's4.keys')


if __name__ == '__main__':
    fill_in_form()




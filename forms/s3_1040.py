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
Fills in a Form 1040 Schedule 3.

The following values must be defined in data.json (in addition to any
requirements for the forms listed above):
    => name
    => ssn

In addition, you can specify any foreign tax paid by including
1099_div's and setting the 'foreign_tax' key.
'''


from . import utils

data = utils.parse_values()

###################################



    
def build_data():

    data_dict = {
        'name'             : data['name'],
        'ssn'              : data['ssn'],
        }

    # Set tax lines here
    if '1099_div' in data:
        foreign_tax = 0.0
        for each in data['1099_div']:
            if 'foreign_tax' in each:
                foreign_tax += each['foreign_tax']
        utils.add_keyed_float(foreign_tax,
                              'foreign_tax_credit',
                              data_dict)

    # Sum up credits
    credits = ['foreign_tax_credit',
               'child_care',
               'education',
               'retirement',
               'energy',
               'other_credits']
    
    total = utils.add_fields(data_dict, credits)
    utils.add_keyed_float(total,
                          'nonrefundable_total',
                          data_dict )

    data_dict['_total_credits'] = total

    return data_dict

def fill_in_form():
    data_dict = build_data()
    data_dict['_width'] = 7
    basename = 'f1040s3.pdf'
    utils.write_fillable_pdf(basename, data_dict, 's3.keys')


if __name__ == '__main__':
    fill_in_form()




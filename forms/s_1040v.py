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
Fills in a Form 1040V (Payment Voucher)

Relies on a full Schedule 1040.
'''


from . import utils
from . import s_1040

data = utils.parse_values()

###################################

def build_data():

    form_1040 = s_1040.build_data()

    data_dict = {
        'ssn'              : data['ssn'],
        'first_and_initial' : data['name_first'] + ' ' + data['name_middle_i'],
        'last'              : data['name_last'],
        'address'           : data['address'],
        'city_state_zip'    : (data['address_city'] 
                               + ', ' + data['address_state'] 
                               + ' ' + data['address_zip']),
        }
    
    if 'apartment' in data:
        data_dict['apartment'] = data['apartment']

    utils.add_keyed_float(form_1040['_owed'],
                          'pay',
                          data_dict)

    return data_dict

def fill_in_form():
    data_dict = build_data()
    basename = 'f1040v.pdf'
    utils.write_fillable_pdf(basename, data_dict, 'f1040v.keys')


if __name__ == '__main__':
    fill_in_form()




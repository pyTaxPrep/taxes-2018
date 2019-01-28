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
Fills in a Schedule SE EZ form.

Relies on Schedule C, plus the 'name' and 'ssn' fields from data.json.

Fills in lines 2 - 6; does not support line 1a or 1b (net farm profit,
social security).
'''

from . import utils
from . import cez_1040

data = utils.parse_values()

###################################

def build_data():
    
    schedule_c = cez_1040.build_data()

    line_2 = utils.dollars_cents_to_float(schedule_c['net_profit_dollars'],
                                          schedule_c['net_profit_cents'])
    line_3 = line_2

    line_4 = line_3 * 0.9235
    
    line_5 = line_4 * 0.153

    line_6 = line_5 * 0.50

    data_dict = {
        'name'             : data['name'],
        'ssn'              : data['ssn']
        }

    utils.add_keyed_float(line_2, 'line_2', data_dict)
    utils.add_keyed_float(line_3, 'line_3', data_dict)
    utils.add_keyed_float(line_4, 'line_4', data_dict)
    utils.add_keyed_float(line_5, 'line_5', data_dict)
    utils.add_keyed_float(line_6, 'line_6', data_dict)

    return data_dict

def fill_in_form():
    data_dict = build_data()
    basename = 'f1040sse.pdf'
    utils.write_fillable_pdf(basename, data_dict, 'sse.keys')


if __name__ == '__main__':
    fill_in_form()




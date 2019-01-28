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
Fills out a Form 8606 when used for backdoor Roth IRA conversions.

You need a dictionary of type 'backdoor_conversion' in data.json's 1099_r entry.

{
 "type" : "backdoor_conversion",
 "contribution" : 5500.0,   <-- How much you put in your traditional IRA in 2018
                                (Line 1 and Line 4)
 "converted"    : 5550.0,   <-- How much was converted into the Roth IRA (Line 8)
 "total_basis"  : 100.0,    <-- Your total basis for 2018 (Line 2)
 "nonroth_eoy"  : 100.0,    <-- Value of non-roth IRAs at the end of 2018 (Line 6)
 "distributions" : 0.0      <-- Any distributions excluding rollovers, conversions,
                                etc. (Line 7)
}

You also need standard personal information fields (name, ssn, address).
'''

from . import utils

data = utils.parse_values()

###################################

def build_data():

    data_dict = {}

    if '1099_r' not in data:
        raise Exception("We need a 1099-R for this form!")

    conv = [ x for x in data['1099_r'] if x['type'] == 'backdoor_conversion' ]
    if len(conv) != 1:
        raise Exception("Need exactly one backdoor conversion type!")

    conv = conv[0]

    data_dict['name'] = data['name']
    data_dict['ssn'] = data['ssn']
    data_dict['home_address'] = data['address']
    data_dict['apt_no'] = data['address_apt']
    data_dict['city_state_zip'] = '%s, %s %s' % (data['address_city'],
                                                 data['address_state'],
                                                 data['address_zip'])

    traditional_contribution = conv['contribution']
    utils.add_keyed_float(traditional_contribution,
                          'trad_ira',
                          data_dict)

    total_basis = conv['total_basis']
    utils.add_keyed_float(total_basis,
                          'total_basis',
                          data_dict)

    line_3 = traditional_contribution + total_basis
    utils.add_keyed_float(line_3,
                          'line_3',
                          data_dict)

    this_year_contrib = 0
    utils.add_keyed_float(this_year_contrib,
                          '2019_contributions',
                          data_dict)

    line_5 = line_3 - this_year_contrib
    utils.add_keyed_float(line_5,
                          'line_5',
                          data_dict)
    
    
    line_6 = conv['nonroth_eoy']
    utils.add_keyed_float(line_6,
                          'year_end_trad_ira_value',
                          data_dict)

    line_7 = conv['distributions']
    utils.add_keyed_float(line_6,
                          'distributions',
                          data_dict)

    line_8 = conv['converted']
    utils.add_keyed_float(line_8,
                          'net_converted',
                          data_dict)

    line_9 = line_6 + line_7 + line_8
    utils.add_keyed_float(line_9,
                          'line_9',
                          data_dict)

    quotient = line_5 / line_9
    quotient_str = '%.6f' % (quotient)
    sp = quotient_str.split('.')
    data_dict['quotient_int'] = sp[0]
    data_dict['quotient_decimal'] = str(sp[1]) + ' '

    line_11 = line_8 * quotient
    utils.add_keyed_float(line_11,
                          'nontaxable_converted',
                          data_dict)

    line_12 = line_7 * quotient
    utils.add_keyed_float(line_12,
                          'nontaxable_nonconvert',
                          data_dict)

    line_13 = line_11 + line_12
    utils.add_keyed_float(line_13,
                          'nontaxable_dist',
                          data_dict)

    line_14 = line_3 - line_13
    utils.add_keyed_float(line_14,
                          'total_basis_now',
                          data_dict)

    line_15a = line_7 - line_12
    utils.add_keyed_float(line_15a,
                          'line_15a',
                          data_dict)


    line_15b = 0
    utils.add_keyed_float(line_15b,
                          'disaster',
                          data_dict)

    line_15c = line_15a - line_15b
    utils.add_keyed_float(line_15c,
                          'taxable_amt',
                          data_dict)

    line_16 = line_8
    utils.add_keyed_float(line_16,
                          'line_16',
                          data_dict)

    line_17 = line_11
    utils.add_keyed_float(line_17,
                          'line_17',
                          data_dict)

    line_18 = line_16 - line_17
    utils.add_keyed_float(line_18,
                          'line_18',
                          data_dict)

    data_dict['_taxable_amt'] = line_18

    # Is there a 10% penalty? No.
    # Instructions for Form 5329 say:
    #  > "The additional tax on early distributions doesn't apply
    #     to any of the following:
    #     ...
    #        - A distribution from a traditional or SIMPLE IRA that
    #          was converted to a Roth IRA.
    #     ...

    return data_dict

def fill_in_form():
    data_dict = build_data()
    basename = 'f8606.pdf'

    utils.write_fillable_pdf(basename, data_dict, 'f8606.keys')


if __name__ == '__main__':
    fill_in_form()




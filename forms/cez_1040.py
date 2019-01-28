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
Fills in a Schedule C-EZ form.

The following keys must be defined in data.json:
    => name
    => ssn

    => address
    => address_city
    => address_state
    => address_zip

    => profession (principal business or profession, including product or service)
    => profession_code (from Schedule C tables)

    => business_exp (list of dictionaries containing 'description' and 'amount' keys, can be empty)
    => 1099_misc (list of dictionaries containing an 'other_income' key)
    
Additionally, the following keys are optional but supported:
    => meals (amount of deductible meals)
    => vehicle (dictionary containing 'dates', 'mileage' and 'mileage_rate' keys).
       [Assumes the vehicle was available for personal use, all miles driven were
        for business (and not commuting or other), the vehicle is the only vehicle,
        and that you have evidence to support the deduction but its not written.]

It makes the following assumptions:
    => Your business doesn't have a separate name or address.
    => You didn't make any payments that would require you to file a 1099.
'''

from . import utils

data = utils.parse_values()

def calculate_expenses():

    d = {}

    if 'meals' in data:
        d['wk_meals_dollars'], d['wk_meals_cents'] = utils.float_to_dollars_cents( data['meals'] )
 
    
    prefixes = ['wk_b', 'wk_c', 'wk_d', 'wk_e', 'wk_f']

    expenses = data['business_exp'][:]

    if 'vehicle' in data:
        expenses.append(
            {'description' : 'Vehicle Mileage (%d miles @ $0.545 per mile)' % 
             (data['vehicle']['mileage']),
             'amount'      : data['vehicle']['mileage'] * data['vehicle']['mileage_rate']})

    for i, ex in enumerate(expenses):
        pfx = prefixes[i]
        dollars, cents = utils.float_to_dollars_cents(ex['amount'])
        d[pfx + '_desc'] = ex['description']
        d[pfx + '_dollars'] = dollars
        d[pfx + '_cents'] = cents
    
    total_cost = sum( [ x['amount'] for x in expenses ] )
    
    if 'meals' in data:
        total_cost +=  d['wk_meals_dollars'] + d['wk_meals_cents'] * 0.01
            
    d['wk_total_dollars'], d['wk_total_cents'] = utils.float_to_dollars_cents(total_cost)

    return d

def build_data():
    expenses = calculate_expenses()

    data_dict = {
        'name'             : data['name'],
        'ssn'              : data['ssn'],
        'profession'       : data['profession'],
        'code'             : data['profession_code'],
        'business_addr_1'  : data['address'],
        'business_addr_2'  : '%s, %s %s' % (data['address_city'],
                                            data['address_state'],
                                            data['address_zip']),
        'need_1099_n'      : True,
        'receipts_dollars' : int(sum( [ x['other_income'] for x in data['1099_misc'] ] ) ),
        'receipts_cents'   : 0,
        'expenses_dollars' : expenses['wk_total_dollars'],
        'expenses_cents'   : expenses['wk_total_cents'],
        }

    if 'vehicle' in data:
        data_dict['vehicle_date'] = data['vehicle']['dates']
        data_dict['vehicle_miles_bus'] = data['vehicle']['mileage']
        data_dict['vehicle_personal_y'] = True,
        data_dict['vehicle_another_n'] = True,
        data_dict['vehicle_evidence_y'] = True,
        data_dict['vehicle_written_n'] = True,
    
    data_dict['net_profit_dollars'], data_dict['net_profit_cents'] = utils.subtract_dc(data_dict['receipts_dollars'],
                                                                                       data_dict['receipts_cents'],
                                                                                       data_dict['expenses_dollars'],
                                                                                       data_dict['expenses_cents'])
    
    for k in expenses:
        data_dict[k] = expenses[k]

    return data_dict

def fill_in_form():
    data_dict = build_data()
    basename = 'f1040sce.pdf'
    utils.write_fillable_pdf(basename, data_dict, 'cez.keys')


if __name__ == '__main__':
    fill_in_form()




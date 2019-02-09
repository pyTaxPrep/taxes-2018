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
Some common utilities used to fill in the different forms.
'''

import io
import os
import sys
import json
import pdfrw
import reportlab.pdfgen.canvas

ROUND_TO_DOLLARS = True

# PDF Format Keys
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_FIELD_TYPE = '/FT'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
PARENT_KEY = '/Parent'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

'''
Somewhat hacky string manipulation functions
'''

def commaify(n):
    '''
    Add commas into a numerical string.
    
    "1234567" => "1,234,567"
    '''

    if n.isdigit():
        chars = list(n)
        for i in range( len(chars) - 3, 0, -3 ):
            chars[i] = ',' + chars[i]
        return ''.join(chars)
    return n

            
def get_pad(x1, x2):
    '''
    Pad where we place text within a field.
    '''
    return int( 0.04 * abs(x1 - x2) )


'''
Read in supporting files - data.json and keyfiles for forms.
'''
def parse_values():
    with open('data.json') as fd:
        return json.load(fd)

def parse_keyfile(kf):
    '''
    We want to map the readable field name to it's actual name in the
    PDF. Complicating matters, the actual name can contain pretty much
    anything, including spaces.

    Keyfiles store one field per line. The first token is the readable
    field name. All the following tokens except the last one make up the
    field name. The last token contains the field type (/Tx or /Btn).
    '''

    rv = {}

    with open(os.path.join('keyfiles', kf)) as fd:
        lines = fd.readlines()
        
        lines = [ x.strip() for x in lines ]
        parsed = []
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith('#'):
                continue
            if len(line.strip()) == 0:
                continue
            firstSpace = line.find(' ')
            lastSpace = line.rfind(' ')
            readable = line[:firstSpace].strip()
            value = line[firstSpace:lastSpace].strip()
            type = line[lastSpace:].strip()

            parsed.append((readable, value, type))

        for readable, value, type in parsed:
            rv[value] = readable

    return rv


'''
Functions for adding in a text overlay to a PDF document.

Largely based on 

https://medium.com/@zwinny/filling-pdf-forms-in-python-the-right-way-eb9592e03dba
'''

def get_overlay(basename, data_dict, keyfile):
    '''
    Create an overlay layer containing the text we want,
    where we want it.
    '''
    input_pdf_path = os.path.join('templates', basename)
    output_pdf_path = os.path.join('filled', basename)

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotations = template_pdf.pages[0][ANNOT_KEY]
    
    value_to_readable = parse_keyfile(keyfile)

    data = io.BytesIO()
    pdf = reportlab.pdfgen.canvas.Canvas(data)

    if '_width' not in data_dict:
        data_dict['_width'] = 8

    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        if annotations is None:
            continue
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    ftype = annotation[ANNOT_FIELD_TYPE]
                else:
                    key = annotation[PARENT_KEY][ANNOT_FIELD_KEY]
                    if key is None:
                        continue
                    key = key[1:-1]
                    ftype = '/Tx'

                if key in value_to_readable:
                    readable = value_to_readable[key]
                        
                    if readable in data_dict:
                        if ftype == '/Btn':
                            value = 'X'
                        else:
                            if ROUND_TO_DOLLARS:
                                if readable.endswith('_cents'):
                                    value = str(data_dict[readable]).zfill(2)
                                    value = ''
                                elif readable.endswith('_dollars'):
                                    cent_key = readable.replace('_dollars', '_cents')
                                    cents = 0
                                    if cent_key in data_dict:
                                        cents = data_dict[cent_key]
                                    if cents >= 50:
                                        data_dict[readable] += 1
                                    value = str(data_dict[readable])
                                    value = commaify(value)
                                    value = ' ' * (data_dict['_width'] - len(value)) + value
                                else:
                                    value = str(data_dict[readable])
                                    value = commaify(value)
                            else:
                                if readable.endswith('_cents'):
                                    value = str(data_dict[readable]).zfill(2)
                                elif readable.endswith('_dollars'):
                                    value = str(data_dict[readable])
                                    value = commaify(value)
                                    value = ' ' * (data_dict['_width'] - len(value)) + value
                                else:
                                    value = str(data_dict[readable])
                                    value = commaify(value)

                        # This is a hack. But so is telling people to put text in places
                        # where there aren't fillable fields.
                        #   > Also, enter "Rollover" next to line 4b.
                        if readable == 'ira_pension_annuity_dollars':
                            if '_rollover_flag' in data_dict:
                                left = 420
                                bottom = 712
                                pdf.setFont('Courier', 8)
                                pdf.drawString(x = left, y = bottom, text = 'Rollover')

                        # print readable, value, data_dict[readable]
                        rect = annotation[ANNOT_RECT_KEY]
                        rect = [ float(str(x)) for x in rect ]
                        left = float(str(min(rect[0], rect[2]))) + get_pad(rect[0], rect[2])
                        bottom = float(str(min(rect[1], rect[3]))) + get_pad(rect[1], rect[3]) + 2
                        #print readable, rect, left, bottom
                        
                        pdf.setFont('Courier', 12)

                        pdf.drawString(x = left, y = bottom, text = value)
        pdf.showPage()

    pdf.save()
    data.seek(0)
    return data


def do_buttons(basename, data_dict, keyfile):
    '''
    Some buttons are tricky because they're linked together
    by a single parent element that we need to update.
    
    Handle that case here.
    '''

    input_pdf_path = os.path.join('filled', basename)
    output_pdf_path = os.path.join('filled', basename)

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotations = template_pdf.pages[0][ANNOT_KEY]
    
    value_to_readable = parse_keyfile(keyfile)

    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        if annotations is None:
            continue
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if not annotation[ANNOT_FIELD_KEY]:
                    parent_key = annotation[PARENT_KEY][ANNOT_FIELD_KEY]
                    if parent_key is None:
                        continue                            
                    parent_key = parent_key[1:-1]
                    if parent_key not in value_to_readable:
                        continue

                    if annotation['/AS']:
                        if 'BUTTONS' in data_dict:
                            for k, v in data_dict['BUTTONS']:
                                if k == value_to_readable[parent_key] and '/' + v in annotation['/AP']['/D'].keys():
                                    annotation[PARENT_KEY].update(pdfrw.PdfDict(V=v))

    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

def merge(overlay, basename):
    '''
    Merge the overlay with the original form, and return the result.
    '''

    input_pdf_path = os.path.join('templates', basename)

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    overlay_pdf = pdfrw.PdfReader(overlay)
    for page, data in zip(template_pdf.pages, overlay_pdf.pages):
        overlay = pdfrw.PageMerge().add(data)[0]
        pdfrw.PageMerge(page).add(overlay).render()
    form = io.BytesIO()
    pdfrw.PdfWriter().write(form, template_pdf)
    form.seek(0)
    return form


def write_fillable_pdf(basename, data_dict, keyfile):
    print('[+] %s' % (basename))
    # Generate our layer of text
    canvas = get_overlay(basename, data_dict, keyfile)
    # Merge it with the original PDF
    form = merge(canvas, basename)
    # Write out the result
    output_pdf_path = os.path.join('filled', basename)
    with open(output_pdf_path, 'wb') as f:
        f.write(form.read())
    # Circle back and handle grouped buttons
    do_buttons(basename, data_dict, keyfile)


def dump_fields(fp):
    '''
    Helper function to print out different fields in a PDF.

    Useful for generating keyfiles, debugging, etc.
    '''

    template_pdf = pdfrw.PdfReader(fp)
    annotations = template_pdf.pages[0][ANNOT_KEY]
    
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        if annotations is None:
            continue
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    type = annotation[ANNOT_FIELD_TYPE]
                    print (key, type)
                else:
                    print ('NOT ANNOT FIELD KEY')
                    if annotation['/AS']:
                        print ('Button', annotation['/AP']['/D'].keys(), annotation[PARENT_KEY][ANNOT_FIELD_KEY])
                    else:
                        print ('Text: ', annotation[PARENT_KEY][ANNOT_FIELD_KEY])
                        print (annotation[PARENT_KEY][ANNOT_VAL_KEY])

def calculate_tax_due(taxable_income):

    tax_table = json.load(open('tables/federal_table.json'))

    for lo, hi, amt in tax_table:
        if taxable_income >= lo and taxable_income < hi:
            return amt

    if taxable_income >= 100000 and taxable_income < 157500:
        tax_due = taxable_income * 0.24 - 5710.50
    elif taxable_income >= 157500 and taxable_income < 200000:
        tax_due = taxable_income * 0.32 - 18310.50
    elif taxable_income >= 20000 and taxable_income < 200000:
        tax_due = taxable_income * 0.35 - 24310.50
    elif taxable_income >= 50000 and taxable_income < 200000:
        tax_due = taxable_income * 0.37 - 34310.50
    else:
        raise Exception("Error calculating federal tax due!")

    return tax_due


'''
Utility functions for manipulating money values and turning
them into dollar, cent string tuples.
'''
def dollars_cents_to_float(d, c):
    return float(d) + float(c) * .01

def float_to_dollars_cents(f):
    # Python 3 uses bankers rounding (to the nearest even),
    # but the IRS always rounds 50 cents upwards.
    
    f_str = '%.2f' % (round(f, 2))
    sp = f_str.split('.')
    d = int(sp[0])
    c = int(sp[1])
    
    # Round and discard cents
    if (c >= 50):
        d += 1
    c = 0

    #d = int(round(f, 0))
    #c = 0
    return d, c

    #return d, c

def subtract_dc(d1, c1, d2, c2):
    v1 = d1 + c1 * .01
    v2 = d2 + c2 * .01
    difference = v1 - v2
    return float_to_dollars_cents(difference)

'''
Helper functions for setting and getting values that are
broken into two fields (dollars and cents).
'''
def add_keyed_float(fv, key, d):
    dollar, cent = float_to_dollars_cents(fv)
    d[key + '_dollars'] = dollar
    d[key + '_cents'  ] = cent

def add_fields(d, fields):
    total = 0.0
    for f in fields:
        dk = f + '_dollars'
        ck = f + '_cents'
        if dk and ck in d:
            total += dollars_cents_to_float(d[dk], d[ck])
    return total



if __name__ == '__main__':
    dump_fields(sys.argv[1])

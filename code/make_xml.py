# Convert the ERAB main table (`main.csv`) from the database dump
# into XML files.

import argparse
import csv
import os.path
import re


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Replace fields in CSV with numeric keys.')
    parser.add_argument(
        'main_csv_file', help='ERAB\'s main table.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    xml, xml_koll = {}, {}
    with open(args.main_csv_file) as fp:
        reader = csv.DictReader(fp)
        for r in reader:
            prefix = re.sub('[0-9\s].*$', '', r['id']).lower()
            if prefix not in xml:
                xml[prefix] = ['<COLLECTION>']
                xml_koll[prefix] = ['<COLLECTION>']
            xml[prefix].append('<ITEM nro="{}" y="{}">'.format(r['id'], r['aasta']))
            xml[prefix].append(r['metaxml'].strip())
            xml[prefix].append(r['textxml'].strip())
            xml[prefix].append(r['refsxml'].strip())
            xml[prefix].append('</ITEM>')
            xml_koll[prefix].append('<ITEM nro="{}">'.format(r['id']))
            xml_koll[prefix].append(r['metaxml_koll'].strip())
            xml_koll[prefix].append(r['textxml_koll'].strip())
            xml_koll[prefix].append(r['refsxml_koll'].strip())
            xml_koll[prefix].append('</ITEM>')
    for key in xml:
        xml[key].append('</COLLECTION>')
        xml_koll[key].append('</COLLECTION>')
    
    for key in xml:
        with open(os.path.join('xml', key + '.xml'), 'w+') as fp:
            fp.write('\n'.join(s for s in xml[key] if s))
        with open(os.path.join('xml_koll', key + '.xml'), 'w+') as fp:
            fp.write('\n'.join(s for s in xml_koll[key] if s))


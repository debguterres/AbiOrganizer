#!/usr/bin/python3
import argparse
import os
import pandas as pd
import zipfile
from Bio import SeqIO


class AbiOrganizer:

    channels = ['DATA9', 'DATA10', 'DATA11', 'DATA12']
    extensions = ('.ab1', '.pdf', '.phd.1', '.txt')

    def organize_files(self, order_table, order_file):

        table = pd.read_excel(order_table)
        table['personInCharge'] = table['personInCharge'].fillna('other')

        with zipfile.ZipFile(order_file + '.zip', 'r') as f:

            for index, row in table.iterrows():

                dir_path = order_file + '/' + row['personInCharge'] + '/' + row['primerCombination']
                file = str(row['sampleName']) + '_' + str(row['primerName'])

                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                for record in f.infolist():
                    if record.filename.startswith(file):
                        f.extract(record, dir_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Organize AB1 files acoording to Macrogen auxiliary table.\n"
                    "Macrogen auxiliary table should include four olbligate fields:\n\n"
                    "\t- sampleName\n"
                    "\t- primerName\n"
                    "\t- personInCharge\n"
                    "\t- primerCombination\n\n"
                    "The two former are default fields from Macrogen auxiliary table.\n"
                    "The last two fields will be used to hierarchically organize folder.\n"
                    "'personInCharge' indlude the name of the person responsible for the\n"
                    "sequencing and 'primerCombination' include the primer pair used to\n"
                    "generate the sequence (ex. NS1_NS4). A good choice is to use a\n"
                    "semmicolon '_' so separate primer names."
    )

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '--file',
        help="Inform the name zipped order file. Do not include the ZIP file extension.\n"
            "Ex.: --file '190731FN-022'.",
        required=True
    )

    required.add_argument(
        '--table',
        help="Inform the name of order table. Please include the file extension.\n"
            "Ex.: --table 'order.xlsx'.",
        required=True
    )
    
    args = parser.parse_args()
    AO = AbiOrganizer()
    AO.organize_files(args.table, args.file)

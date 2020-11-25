#! ./bin/python3

import csv
import os
import sys
from csvToPDF import CSV_to_PDF_Generator

class Batch_CSV_TO_PDF_GENERATOR:
    def __init__(self, file_path, output_dir, nogroup=False):
        self.file_path = file_path 
        self.output_dir = output_dir
        self.nogroup = nogroup

    def process(self):
        with open(self.file_path, mode='r', encoding='utf-8-sig') as csv_file:
            csv_reader = list(csv.DictReader(csv_file))
            if self.nogroup:
                self.all_in_one_process(csv_reader)
            else:
                self.group_process(csv_reader)
            print("Complete")

    def all_in_one_process(self, csv_reader):
            print("Generating non grouped barcode sheet(s)")

            generator = CSV_to_PDF_Generator(self.file_path, self.output_dir+'/batch.pdf')
            generator.create()




    def group_process(self, csv_reader):
            print("Generating group barcode sheet(s)")

            skus = {}
    
            for row in csv_reader:
                if row['sku'] in skus:
                    skus[row['sku']].append(row)
                else:
                    skus[row['sku']] = []
                    skus[row['sku']].append(row)
    
            for sku, rows in skus.items():
                print("creating "+ sku  + " folder") 
                os.makedirs(self.output_dir+"/"+sku)
                with open(self.output_dir+"/"+sku+"/"+sku+".csv", mode='w') as small_csv_file:
                    fieldnames = ['sku', 'barcode', 'season', 'size', 'product', 'design']
                    writer = csv.DictWriter(small_csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in rows:
                        writer.writerow(row)
                generator = CSV_to_PDF_Generator(self.output_dir+'/'+sku+'/'+sku+'.csv', self.output_dir+'/'+sku+'/'+sku+'.pdf') 
                generator.create()

def main():
    csv_file = sys.argv[1]
    output_dir = sys.argv[2]
    batch_generator = Batch_CSV_TO_PDF_GENERATOR(csv_file, output_dir)
    batch_generator.process()

#main()

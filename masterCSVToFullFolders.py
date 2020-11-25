#! ./bin/python3

import csv
import os
import sys
from csvToPDF import CSV_to_PDF_Generator

class Batch_CSV_TO_PDF_GENERATOR:
    def __init__(self, file_path, output_dir):
        self.file_path = file_path 
        self.output_dir = output_dir

    def process(self):
        with open(self.file_path, mode='r', encoding='utf-8-sig') as csv_file:
            csv_reader = list(csv.DictReader(csv_file))

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
            print("Complete")

def main():
    csv_file = sys.argv[1]
    batch_generator = Batch_CSV_TO_PDF_Generator(csv_file)
    batch_generator.process()

#main()

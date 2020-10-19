#! ./bin/python3

import csv
import os
import sys
from csvToPDF import CSV_to_PDF_Generator


def main():
    for arg in sys.argv:
        if arg == "-h":
            print("Call with CSV file as the first argument");
            return

    csv_file = sys.argv[1]

    with open(csv_file, mode='r', encoding='utf-8-sig') as csv_file:
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
            os.makedirs("./output/"+sku)
            with open("./output/"+sku+"/"+sku+".csv", mode='w') as small_csv_file:
                fieldnames = ['sku', 'barcode', 'season', 'size', 'product', 'design']
                writer = csv.DictWriter(small_csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
            generator = CSV_to_PDF_Generator('./output/'+sku+'/'+sku+'.csv', './output/'+sku+'/'+sku+'.pdf') 
            generator.create()

main()

#! ./bin/python3

import csv
import os
import sys
from csvToPDF import CSV_to_PDF_Generator


def main():
    csv_file = sys.argv[1]

    with open(csv_file, mode='r') as csv_file:
        csv_reader = list(csv.DictReader(csv_file))
        
        skus = {}

        for row in csv_reader:
            if row['sku'] in skus:
                skus[row['sku']].append(row)
            else:
                skus[row['sku']] = []
                skus[row['sku']].append(row)

        for sku, rows in skus.items():
            print(sku, rows)
            print("creating "+ sku  + " folder") 
            os.makedirs("./output/"+sku)
            with open("./output/"+sku+"/"+sku+".csv", mode='w') as small_csv_file:
                fieldnames = ['sku', 'barcode', 'season', 'size', 'product', 'design']
                writer = csv.DictWriter(small_csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for row in rows:
                    print('writing row: ', row, type(row))
                    writer.writerow(row)
            generator = CSV_to_PDF_Generator('./output/'+sku+'/'+sku+'.csv', './output/'+sku+'/'+sku+'.pdf') 
            generator.create()

main()

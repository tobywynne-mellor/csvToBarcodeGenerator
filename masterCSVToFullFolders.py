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
            os.mkdir("./"+sku)
            with open("./"+sku+"/"+sku+".csv", mode='w') as small_csv_file:
                writer = csv.writer(small_csv_file, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
                for row in rows:
                    writer.writerow(list(row).split(','))
            CSV_to_PDF_Generator('./'+sku+'/'+sku+'.csv', './'+sku+'/'+sku+'.pdf') 

main()

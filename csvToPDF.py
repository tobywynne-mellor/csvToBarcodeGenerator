#! ./bin/python3

### Recieve ###
    # - csv input of parent SKU, barcode, season code, size, product type, design
    # - output dir (default to ./output) 

### VALIDATE output dir ###
    # must not already exist

### VALIDATE CSV ###
    # check if headers are valid -> correct names and number of columns
    # check if each value is valid
        # SKU -> correct length, not having numbers at end
        # barcode -> correct length
        # season code -> 2 digits
        # size -> correct length
        # product type -> correct length, alphanumeric
        # design -> correct length, no numbers

### group all parent skus into dictionaries ###

### GENERATE ALL BARCODE IMAGES USING SCOROPION ###
    # for each parent sku create dir
    # use os package to call scorpion on all barcodes numbers and put in dir

### CREATE PDF ###
    # https://realpython.com/creating-modifying-pdf/#creating-a-pdf-file-from-scratch
    # named after parent sku
    # create pdf class
        # with correct dimentions for each part of the label on the A4 sheet
        # methods - addLabel, savePDF
    # save to parent sku dir

import sys
from csvFileProcessor import CSVFileProcessor
from barcodeSheetGenerator import BarcodeSheetGenerator

class CSV_to_PDF_Generator:
    def __init__(self, csv_file_path, output_path):
        self.csv_file_path = csv_file_path
        self.output_path = output_path

    def create(self):
        csvProcessor = CSVFileProcessor(self.csv_file_path)

        if csvProcessor.isValid():
            data = csvProcessor.getData()
            bsg = BarcodeSheetGenerator(data)
            bsg.generate(self.output_path)

def main():
    csv_file_path = sys.argv[1]
    output_path = sys.argv[2]
    generator = CSV_to_PDF_Generator(csv_file_path, output_path)
    generator.create()

#main()

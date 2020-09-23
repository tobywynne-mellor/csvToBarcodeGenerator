# DO A POC
    # generate a barcode with scorpion through python
    # create a pdf with the correct measurements

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

#import subprocess

#result = subprocess.call("", shell=True)


from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

canvas = Canvas("hello.pdf", pagesize=A4)
canvas.drawString(72, 72, "Hello, World")

canvas.drawImage("testimg.png", 200,200, mask="auto")
canvas.showPage()
canvas.save()

import os
import math
from imageProcess import ImageProcessor
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

class BarcodeSheetGenerator:
    def __init__(self, csv_data):
        self.csv_data = csv_data

    def createBarcode(self, barcodeNumber):
        data = barcodeNumber
        cmd = './ScorpionBarCode -action "pdff" -type "EAN-13" -data "'+data+'" -output "./'+data+'.pdf" -antialiasoff 1'
        os.system(cmd)
        processor = ImageProcessor(width=1000)
        image = processor.process("./"+data+".pdf")
        os.remove(data+".pdf")
        return image

    def get_data_queue(self):
        pass

    def generate(self, output_path):
        if output_path == None:
            print("no output path specified")
            return

        canvas = Canvas(output_path, pagesize=A4)
        canvas.setFont("Helvetica", 7)

        page_width, page_height = A4

        top_margin = 1.3*cm
        side_margin = 0.4*cm
        label_width = 4.95*cm
        label_height = 3*cm
        vertical_pitch = 3*cm
        horizontal_pitch = 5.05*cm

        image_width = 0.7*label_width
        image_height = (2/3)*label_height

        across = 4
        down = 9

        label_x_start = side_margin
        label_y_start = page_height - top_margin - label_height
        
        image_x_start = label_x_start + (label_width - image_width)/2
        image_y_start = label_y_start + (label_height*0.25)

        sku_x_start = label_x_start + label_width*0.04
        sku_y_start = label_y_start + label_height*0.04 + label_height*0.12

        product_x_start = sku_x_start
        product_y_start = label_y_start + label_height*0.04

        size_x_start = horizontal_pitch
        size_y_start = sku_y_start
        
        design_x_start = size_x_start 
        design_y_start = product_y_start 

        season_x_start = label_width / 2 + side_margin 
        season_y_start = product_y_start

        sheets_needed = math.ceil(len(self.csv_data) / 36)

        while sheets_needed >= 1:
            canvas.setFont("Helvetica", 7)
            for i in range(down):
                for j in range(across):

                    if len(self.csv_data) < 1:
                        break

                    data = self.csv_data.pop(0)

                    adjust_x = j * horizontal_pitch
                    adjust_y = i * vertical_pitch

                    # border
                    #x = label_x_start + adjust_x
                    #y = label_y_start - adjust_y
                    #canvas.rect(x, y, label_width, label_height, stroke=1, fill=0)

                    image_x = image_x_start + adjust_x
                    image_y = image_y_start - adjust_y
                    canvas.drawImage(self.createBarcode(data['barcode']), image_x, image_y, width=image_width, height=image_height, mask='auto')

                    sku_x = sku_x_start + adjust_x
                    sku_y = sku_y_start - adjust_y
                    canvas.drawString(sku_x, sku_y, data['sku'])

                    product_x = product_x_start + adjust_x
                    product_y = product_y_start - adjust_y
                    canvas.drawString(product_x, product_y, data['product'])

                    size_x = size_x_start + adjust_x
                    size_y = size_y_start - adjust_y
                    canvas.drawRightString(size_x, size_y, data['size'])

                    design_x = design_x_start + adjust_x
                    design_y = design_y_start - adjust_y
                    canvas.drawRightString(design_x, design_y, data['design'])
                    
                    season_x = season_x_start + adjust_x
                    season_y = season_y_start - adjust_y
                    canvas.drawCentredString(season_x, season_y, data['season'])

            sheets_needed -= 1
            canvas.showPage()

        canvas.save()
        print(output_path + " saved")

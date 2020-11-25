import os
import math

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget
from reportlab.graphics import renderPDF
from reportlab.pdfgen.canvas import Canvas

class BarcodeSheetGeneratorV2:
    def __init__(self, csv_data):
        self.csv_data = csv_data

        self.top_margin = 1.3*cm
        self.side_margin = 0.4*cm
        self.label_width = 4.95*cm
        self.label_height = 2.9*cm
        self.vertical_pitch = 3*cm
        self.horizontal_pitch = 5.05*cm
        self.page_width, self.page_height = A4

        self.image_width = 0.9*self.label_width
        self.image_height = 0.6*self.label_height

        self.across = 4
        self.down = 9

        self.label_x_start = self.side_margin
        self.label_y_start = self.page_height - self.top_margin - self.label_height

        self.image_x_start = self.label_x_start + (self.label_width - self.image_width)/2
        self.image_y_start = self.label_y_start + (self.label_height*0.3)

        self.sku_x_start = self.label_x_start + self.label_width*0.04
        self.sku_y_start = self.label_y_start + self.label_height*0.04 + self.label_height*0.12

        self.product_x_start = self.sku_x_start
        self.product_y_start = self.label_y_start + self.label_height*0.04

        self.size_x_start = self.horizontal_pitch
        self.size_y_start = self.sku_y_start

        self.design_x_start = self.size_x_start 
        self.design_y_start = self.product_y_start 

        self.season_x_start = self.label_width / 2 + self.side_margin 
        self.season_y_start = self.product_y_start

        self.sheets_needed = math.ceil(len(self.csv_data) / 36)

        self.barcode_y = 10


    def createBarcode(self, data):
        print("Creating barcode {} {} {} {}".format(data['barcode'], data['sku'], data['design'], data['size']))
        barcode = Ean13BarcodeWidget(data['barcode'])
        barcode.barWidth = 1.2 
        barcode.barHeight = self.image_height 
        x0, y0, bw, bh = barcode.getBounds()
        barcode.x = self.label_x_start + (self.label_width - bw)/2
        barcode.y = self.image_y_start # self.label_height # self.label_y_start #self.barcode_y 

        label_drawing = Drawing(self.label_width, self.label_height)

        sku = String(self.sku_x_start, self.sku_y_start, data['sku'], fontName="Helvetica", fontSize=7, textAnchor="start")
        size = String(self.size_x_start, self.size_y_start, data['size'], fontName="Helvetica", fontSize=7, textAnchor="end")
        product = String(self.product_x_start, self.product_y_start, data['product'], fontName="Helvetica", fontSize=7, textAnchor="start")
        design = String(self.design_x_start, self.design_y_start, data['design'], fontName="Helvetica", fontSize=7, textAnchor="end")
        season = String(self.season_x_start, self.season_y_start, data['season'], fontName="Helvetica", fontSize=7, textAnchor="middle")

        label_drawing.add(barcode)
        label_drawing.add(sku)
        label_drawing.add(size)
        label_drawing.add(product)
        label_drawing.add(design)
        label_drawing.add(season)

        return label_drawing

    def get_data_queue(self):
        pass

    def generate(self, output_path):
        if output_path == None:
            print("no output path specified")
            return

        canvas = Canvas(output_path, pagesize=A4)

        while self.sheets_needed >= 1:
            canvas.setFont("Helvetica", 7)
            for i in range(self.down):
                for j in range(self.across):

                    if len(self.csv_data) < 1:
                        break

                    data = self.csv_data.pop(0)

                    adjust_x = j * self.horizontal_pitch
                    adjust_y = i * -self.vertical_pitch

                    # border
                    x = self.label_x_start + adjust_x
                    y = self.label_y_start + adjust_y
                    #canvas.rect(x, y, self.label_width, self.label_height, stroke=1, fill=0)

                    renderPDF.draw(self.createBarcode(data), canvas, adjust_x, adjust_y)

            self.sheets_needed -= 1
            canvas.showPage()

        canvas.save()
        print(output_path + " saved")

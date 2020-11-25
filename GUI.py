#!/usr/bin/env python

import PySimpleGUI as sg
from masterCSVToFullFolders import Batch_CSV_TO_PDF_GENERATOR 

# All the stuff inside your window.
layout = [
        [sg.Text("Spreadsheet File"), sg.Input(), sg.FileBrowse()],
        [sg.Text("Output Folder"), sg.Input(), sg.FolderBrowse()],
        [sg.Submit()],
        [sg.Output(size=(100,30), key='-OUTPUT-')]
    ]
# Create the Window
window = sg.Window('Toby Tiger Barcodes', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    csv = values[0]
    output_dir = values[1]
    print=sg.Print
    barcodeGenerator = Batch_CSV_TO_PDF_GENERATOR(csv, output_dir) 
    barcodeGenerator.process() 
window.close()

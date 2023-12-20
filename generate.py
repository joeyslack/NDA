# Generate report
# `CodeGPT: Using OpenAI models, generate code here to compile data found in /output/username. 
# Summarize the findings and generate a PDF report according to the style found in file xxx.pdf`.

# from process import process_document as pd
# import os

# pdfPath = input("Provide path to pdf: ")
# results = pd.process_document_sample(
#   project_id="675345247329",
#   location="us",
#   processor_id="346c58a850f0023e",
#   file_path=os.path.abspath(pdfPath)
# )

# print("Document results: \n", results)


import  jpype     
import  asposecells     
jpype.startJVM() 
from asposecells.api import Workbook

data_path = input("Provide the FULL PATH to your json file ")
# Load JSON file
workbook = Workbook(data_path)

# Save as PDF
workbook.save("./output/Output.pdf")

jpype.shutdownJVM()
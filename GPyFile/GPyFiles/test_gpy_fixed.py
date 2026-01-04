import os
import sys
import shutil
from docx import Document
from openpyxl import Workbook
from fpdf import FPDF
import json

# Add the script dir to path to import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from GPy import *

# Ensure directories exist
os.makedirs(ARCHIVOS_DIR, exist_ok=True)
os.makedirs(PAPELERA_DIR, exist_ok=True)

print("=== Test 1: List initial directory ===")
listar(ARCHIVOS_DIR)

print("=== Test 2: Create TXT file ===")
crear_archivo("test.txt")

print("=== Test 3: Put content to TXT ===")
put_contenido("test.txt", "Hello, world!")

print("=== Test 4: View TXT content ===")
view_contenido("test.txt")

print("=== Test 5: Create JSON file ===")
crear_archivo("test.json")

print("=== Test 6: Put content to JSON ===")
put_contenido("test.json", "test_value")

print("=== Test 7: View JSON content ===")
view_contenido("test.json")

print("=== Test 8: Create DOCX file ===")
crear_archivo("test.docx")

print("=== Test 9: Put content to DOCX ===")
put_contenido("test.docx", "Document content here.")

print("=== Test 10: View DOCX content ===")
view_contenido("test.docx")

print("=== Test 11: Create XLSX file ===")
crear_archivo("test.xlsx")

print("=== Test 12: Put content to XLSX ===")
put_contenido("test.xlsx", "Excel data row")

print("=== Test 13: View XLSX content ===")
view_contenido("test.xlsx")

print("=== Test 14: Create PDF file (view not supported) ===")
crear_archivo("test.pdf")
print("PDF created successfully.")

print("=== Test 15: Create CSV file ===")
crear_archivo("test.csv")

print("=== Test 16: Put content to CSV ===")
put_contenido("test.csv", "csv,data,row")

print("=== Test 17: View CSV content ===")
view_contenido("test.csv")

print("=== Test 18: Create directory ===")
crear_carpeta("testdir")

print("=== Test 19: List after mkdir ===")
listar(ARCHIVOS_DIR)

print("=== Test 20: Rename file ===")
renombrar("test.txt", "renamed.txt")

print("=== Test 21: List after rename ===")
listar(ARCHIVOS_DIR)

print("=== Test 22: Move file to directory ===")
mover("renamed.txt", "testdir/renamed.txt")

print("=== Test 23: List directory after move ===")
listar(os.path.join(ARCHIVOS_DIR, "testdir"))

print("=== Test 24: Remove file (move to trash) ===")
eliminar("testdir/renamed.txt")

print("=== Test 25: List trash ===")
listar(PAPELERA_DIR)

print("=== Test 26: Restore file ===")
restaurar_archivo("renamed.txt")

print("=== Test 27: List after restore ===")
listar(ARCHIVOS_DIR)

print("=== Test 28: Error handling - View non-existent file ===")
view_contenido("nonexistent.txt")

print("=== Test 29: Error handling - Remove non-existent ===")
eliminar("nonexistent.txt")

print("=== Test 30: Help command ===")
ayuda()

print("=== All tests completed. Cleaning up... ===")
# Cleanup
for file in ["test.txt", "test.json", "test.docx", "test.xlsx", "test.pdf", "test.csv", "renamed.txt"]:
    if os.path.exists(os.path.join(ARCHIVOS_DIR, file)):
        os.remove(os.path.join(ARCHIVOS_DIR, file))
if os.path.exists(os.path.join(ARCHIVOS_DIR, "testdir")):
    shutil.rmtree(os.path.join(ARCHIVOS_DIR, "testdir"))
if os.path.exists(os.path.join(PAPELERA_DIR, "renamed.txt")):
    os.remove(os.path.join(PAPELERA_DIR, "renamed.txt"))

print("Cleanup done.")

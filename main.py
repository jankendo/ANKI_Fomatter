import os
import tkinter as tk
import tkinter.filedialog as filedialog
import zipfile
import sqlite3
import shutil

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[('Anki Package Files', '*.apkg')])

if os.path.exists('output'):
    shutil.rmtree('output')

with zipfile.ZipFile(file_path, 'r') as zip_ref:
    zip_ref.extractall('output')

db_path = 'output/collection.anki2'

conn = sqlite3.connect(db_path)

cursor = conn.execute('SELECT flds FROM notes')

for row in cursor:
    data = row[0]
    if data:
        fields = data.split("\x1f")
        print(fields)

conn.close()

from pypdf import PdfReader
import process_rows
from os import listdir
from os.path import isfile, join

input_path = "input";
files = [f for f in listdir(input_path) if isfile(join(input_path, f))]

data = [];



def visitor_body(text, cm, tm, font_dict, font_size):
    parts.append(text)

# main
for file in files:
    print(file)
    if (file.find(".") == 0):
        continue
    reader = PdfReader(input_path + "/" + file)
    parts = []
    pages = reader.pages[1:]

    for page in pages:
        page.extract_text(visitor_text=visitor_body)
        page_string = "".join(parts)
        res = process_rows.process(page_string.split("\n"))

    data.extend(res)

header = "Date,Description,Amount"
filename = "output/" + "all" + ".csv"
# print(data[0])
with open(filename, 'w') as f:
    f.write(header + "\n")
    for row in data:
        f.write(row)
        f.write("\n")

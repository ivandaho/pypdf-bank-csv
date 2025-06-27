from pypdf import PdfReader
import gxs
from os import listdir
from os.path import isfile, join

input_path = "input";
files = [f for f in listdir(input_path) if isfile(join(input_path, f))]

data = [];

START_PAGES = { "trust": 1, "gxs": 0}
currentSource = "gxs"


def visitor_body(text, cm, tm, font_dict, font_size):
    parts.append(text)

# main
for file in files:
    print(file)
    if (file.find(".") == 0):
        continue
    reader = PdfReader(input_path + "/" + file)
    pages = reader.pages[START_PAGES.get(currentSource):]

    allPagesContent = [];
    for page in pages:
        parts = []
        page.extract_text(visitor_text=visitor_body)
        page_string = "".join(parts)
        pp = page_string.split("\n")
        allPagesContent.extend(pp)

        # data.extend(pp)
    print(f'the length: {len(allPagesContent)}')

    res = gxs.processStatement(allPagesContent)
    # data.extend(pp)
    data.extend(res)
    gxs.writeGXS(res);


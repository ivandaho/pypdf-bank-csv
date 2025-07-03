from pypdf import PdfReader
import gxs
from os import listdir
from os.path import isfile, join
import trust

input_path = "input"
files = [f for f in listdir(input_path) if isfile(join(input_path, f))]

data = []

START_PAGES = {"trust": 1, "gxs": 0}
currentSource = "gxs"


def visitor_body(text, cm, tm, font_dict, font_size):
    parts.append(text)

# main

acrossFilesContent = {}

for file in files:
    allPagesContent = []
    if file.find(".") == 0:
        print(f"ignoring dotfile: {file}")
        continue
    print(f"processing file: {file}")
    reader = PdfReader(input_path + "/" + file)
    pages = reader.pages[START_PAGES.get(currentSource) :]

    for page in pages:
        parts = []
        page.extract_text(visitor_text=visitor_body)
        page_string = "".join(parts)
        pp = page_string.split("\n")
        allPagesContent.extend(pp)

    if currentSource == "trust":
        res = trust.process(allPagesContent)
        d = {}
        d["trust"] = res
        # TODO cleanup trust file writing method
        gxs.writeGXS(d, "trust")
    elif currentSource == "gxs":
        res, fileName = gxs.processStatement(allPagesContent)
        gxs.writeGXS(res, fileName)
        for k in res.keys():
            if acrossFilesContent.get(k) == None:
                acrossFilesContent[k] = []
            rows = res.get(k)
            acrossFilesContent[k].extend(res.get(k))

# write full files based on pocket
# note this doesn't handle early pockets where the naming was just "Pocket" instead of "Savings Pocket" or "Boost Pocket"
gxs.writeGXS(acrossFilesContent, "full")

# Bank PDF statement to CSV extractor

Python tool utilising `pypdf` to extract text from bank's pdf export to a usable .csv format.

Currently only supports Trust Bank Singapore pdf exports

`/input` and `/output` directories are git ignored.

## Usage

Put downloaded pdf files into `/input` folder. Multiple files are supported. files starting with `.` are ignored.

run `python3 main.py`.

Output will be in `output/all.csv`

## Caveats, notes

- untested, provided as is. might have inaccuracies
- input and output folders might need to be created manually the first time

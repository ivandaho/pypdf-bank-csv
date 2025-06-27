import re
from string import Template
from datetime import datetime
from typing import Dict
from constants import GXS_STATEMENT_ACCOUNT_REGEXP, GXS_STATEMENT_AMOUNT_REGEXP, NEWFILE_MARKER
t = Template("$date,\"$desc\",$posi$amount")

gxsPageHeader = "Date Description Withdrawal (S$) Deposit (S$) Balance (S$)"

def processStatement(rows: list[str]):
    processed_rows = {};
    date_string = ""
    desc_string = ""
    posi_neg_sign_string = ""
    amount_string = ""

    state = -1
    temp = "";
    isOpeningBalance = True;
    accountName = "";
    count = 0;
    lastBalance = 0;

    for i, row in enumerate(rows):
        if (state == -1):
            # if count is -1, look for the header to start processing
            if (row == gxsPageHeader):
                state = 0
                tempAccName = rows[i - 1];
                m = re.search(GXS_STATEMENT_ACCOUNT_REGEXP, tempAccName)
                if (m != None):
                    # found a new account within the statement
                    accountName = tempAccName
                    processed_rows[accountName] = [];
        else:
            # add to temp
            if (state > 0):
                # only add comma after first line
                temp = temp + ","

            lastRowWithAmountMatch = re.search(GXS_STATEMENT_AMOUNT_REGEXP, row);
            if (lastRowWithAmountMatch != None):
                try:
                    amount = float((lastRowWithAmountMatch.group(1)).replace(",", ""))
                    balance = float((lastRowWithAmountMatch.group(2)).replace(",", ""))
                    checkBalance = lastBalance + amount
                    lastBalance = balance
                    isDeposit = checkBalance == balance
                    if (isDeposit):
                        temp = temp + f"{amount}"
                    else:
                        temp = temp + f"-{amount}"
                except:
                    print(f'except: {row}')
            else:
                temp = temp + row

            state = state + 1
            if (isOpeningBalance or state > 4):
                isOpeningBalance = False
                processed_rows[accountName].append(temp)
                # reset
                temp = "";
                state = 0
                continue
            if (row == " "):
                count = count + 1
                print(f"found page bottom. {count}");
                # page bottom reached. wait until next page header again
                temp = "";
                state = -1

    return processed_rows


year = "1999"; # just to make it obvious

def parse_date(date_string):
    d = datetime.strptime(date_string + " " + year, "%d %b %Y")
    if (d.month >= 9):
        d = d.replace(2024)
    else:
        d = d.replace(2025)

    return d.strftime("%Y-%m-%d");

def make_positive_negative(sign_string):
    return "-" if sign_string == "" else sign_string

# writes the file after processing a statement
def writeGXS(processedRows: Dict):
    header = ""
    accName = ""
    # header = "Date,Description,Amount"
    for p in processedRows.keys():
        filename = f"output/{p}.csv"
        # print(data[0])
        with open(filename, 'w') as f:
            f.write(header + "\n")
            for row in processedRows[p]:
                f.write(row)
                f.write("\n")

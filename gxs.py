import re
from string import Template
from datetime import datetime
from typing import Dict
from constants import (
    GXS_STATEMENT_ACCOUNT_REGEXP,
    GXS_STATEMENT_AMOUNT_REGEXP,
    GXS_STATEMENT_DATE_REGEXP,
    GXS_STATEMENT_OPENING_BALANCE_REGEXP,
    GXS_STATEMENT_TIME_REGEXP,
    OUTPUT_CSV_HEADER,
)

t = Template('$date,"$desc",$posi$amount')

gxsPageHeader = "Date Description Withdrawal (S$) Deposit (S$) Balance (S$)"


def processStatement(rows: list[str]):
    processed_rows = {}

    state = -1
    temp = ""
    lookForOpeningBalance = True
    accountName = ""
    statementYear = "1999"  # should be replaced when opening balance header found
    count = 0
    lastBalance = 0

    fileName = "not-found"
    for i, row in enumerate(rows):
        if state == -1:
            # if count is -1, look for the header to start processing
            if row == gxsPageHeader:
                state = 0
                tempAccName = rows[i - 1]
                m = re.search(GXS_STATEMENT_ACCOUNT_REGEXP, tempAccName)
                if m != None:
                    # found a new account within the statement
                    accountName = tempAccName
                    lookForOpeningBalance = True
                    processed_rows[accountName] = []
        else:

            isDateInformation = re.search(GXS_STATEMENT_DATE_REGEXP, row)
            isTimeInformation = re.search(GXS_STATEMENT_TIME_REGEXP, row)
            lastRowWithAmountMatch = re.search(GXS_STATEMENT_AMOUNT_REGEXP, row)
            if lookForOpeningBalance:
                openingBalanceResult = re.search(
                    GXS_STATEMENT_OPENING_BALANCE_REGEXP, row
                )
                try:
                    if openingBalanceResult != None:
                        statementYear, f = get_info_from_opening_balance(
                            openingBalanceResult.group(1)
                        )
                        fileName = f
                        lastBalance = float(
                            (openingBalanceResult.group(2)).replace(",", "")
                        )
                        print(
                            f"setting last balance for {f} {accountName}: {lastBalance}"
                        )
                except:
                    print(f"could not determine opening balance: {row}")
            elif isDateInformation:
                temp = parse_date(row, statementYear)
            elif isTimeInformation:
                temp = f"{temp} {row},"
            elif lastRowWithAmountMatch != None:
                try:
                    desc = ""
                    if lastRowWithAmountMatch.group(1) != None:
                        desc = lastRowWithAmountMatch.group(1)

                    amount = float((lastRowWithAmountMatch.group(2)).replace(",", ""))
                    balance = float((lastRowWithAmountMatch.group(3)).replace(",", ""))
                    checkBalance = f"{(lastBalance + amount):.2f}"
                    lastBalance = balance
                    isDeposit = checkBalance == f"{balance:.2f}"
                    if isDeposit:
                        temp = f"{temp}{desc},{amount}"
                    else:
                        temp = f"{temp}{desc},-{amount}"

                    processed_rows[accountName].append(temp.replace(", ", ","))
                except:
                    print(f"except: {row}")
            else:
                # append row as description with space in between
                temp = f"{temp} {row}"

            state = state + 1

            if lookForOpeningBalance or lastRowWithAmountMatch != None:
                lookForOpeningBalance = False
                # reset
                temp = ""
                state = 0
                continue
            if row == " ":
                count = count + 1
                # page bottom reached. wait until next page header again
                temp = ""
                state = -1

    return processed_rows, fileName


year = "1999"
# just to make it obvious if the year was not set at all


def get_info_from_opening_balance(date_string):
    d = datetime.strptime(f"0{date_string}", "%d %b %Y")
    fileName = d.strftime("%Y-%m-%d")
    return d.strftime("%Y"), fileName


def parse_date(date_string, year):
    if date_string.index(" ") == 2:
        d = datetime.strptime(f"{date_string} {year}", "%d %b %Y")
    else:
        d = datetime.strptime(f"0{date_string} {year}", "%d %b %Y")
    return d.strftime("%Y-%m-%d")


# writes the file after processing a statement
def writeGXS(processedRows: Dict, fileName: str):
    for p in processedRows.keys():
        filename = f"output/{fileName}-{p}.csv"
        print(f"writing: {filename}")
        with open(filename, "w") as f:
            f.write(OUTPUT_CSV_HEADER + "\n")
            for row in processedRows[p]:
                f.write(row)
                f.write("\n")

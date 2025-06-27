import re
from string import Template
from datetime import datetime
t = Template("$date,\"$desc\",$posi$amount")

def process(rows):
    processed_rows = [];
    date_string = ""
    desc_string = ""
    posi_neg_sign_string = ""
    amount_string = ""

    for row in rows:
        if (row.find("Total outstanding balance") > -1 or row.find("Previous balance") > -1):
            continue
            # regular string
        m = re.search(r"(^\d\d [A-Z][a-z][a-z])(?: )(.+)(?: )(\+?)((\d,?)+\.\d\d)($|(?:Trust Bank Singapore Limited$))", row)

        if (m != None):
            date_string = parse_date(m.group(1))
            desc_string = m.group(2).replace(",", "")
            posi_neg_sign_string = make_positive_negative(m.group(3))
            amount_string = m.group(4).replace(",", "")
            single_row = t.substitute(date=date_string, desc=desc_string,posi=posi_neg_sign_string, amount=amount_string)

            processed_rows.append(single_row)
        else:
            # currency conversion rate data
            fx = re.search(r"(.+)(?<!Total outstanding balance)(?<!Previous balance)(?: )(\+?)((,?\d{,3})*\.\d\d)($|(?:Trust Bank Singapore$)|(?:Trust Bank Singapore Limited$))", row)
            if (fx != None):
                desc_string = desc_string + "|" + fx.group(1).replace(",", "")
                posi_neg_sign_string = make_positive_negative(fx.group(2))
                amount_string = fx.group(3).replace(",", "")

                single_row = t.substitute(date=date_string, desc=desc_string,posi=posi_neg_sign_string, amount=amount_string)

                processed_rows.append(single_row)

            else:
                # transaction date, description
                dd = re.search(r"(^\d\d [A-Z][a-z][a-z])(?: )(.+)$", row)
                if (dd != None):
                    # set data but don't append to array
                    date_string = parse_date(dd.group(1))
                    desc_string = dd.group(2).replace(",", "").strip()
                    posi_neg_sign_string = "CLEAR---------" # if these show up, there's a problem
                    amount_string =  "CLEAR---------"
                else:
                    print("IGNORING: " + row)

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

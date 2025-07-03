NEWFILE_MARKER = "NEWFILE_MARKER"
GXS_STATEMENT_ACCOUNT_REGEXP = (
    r"^((.* (Boost Pocket))|(.* (Pocket))|(.* (Savings Pocket))|(Main Account))$"
)
GXS_STATEMENT_AMOUNT_REGEXP = r"^((?:Interest Earned)|(?:Interest Earned Reversal)|(?:Base Interest earned))?(?: )?(\d{1,3}(?:[,]\d{3})*(?:\.\d{2})) (\d{1,3}(?:[,]\d{3})*(?:\.\d{2}))$"
GXS_STATEMENT_TIME_REGEXP = r"\d{2}:[0-5]\d (P|A)M$"
GXS_STATEMENT_DATE_REGEXP = r"^\d{,2} \w\w\w$"
GXS_STATEMENT_OPENING_BALANCE_REGEXP = (
    r"(.*)(?: Opening balance )(\d{1,3}(?:[,]\d{3})*(?:\.\d{2}))$$"
)
OUTPUT_CSV_HEADER = "Date,Description,Amount"

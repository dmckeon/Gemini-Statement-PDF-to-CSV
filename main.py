import os.path
import re
import pdfplumber
import pandas as pd
from collections import namedtuple

pdf_file = 'statement_2022-05-25.pdf' # This is where you enter the name of the statement you want converted

Transactions = namedtuple('Transactions', 'trans_id trans_date post_date vendor amount')

pdf_file_name = pdf_file.split('_')[1]
pdf_file_name = pdf_file_name.split('.')[0]

with pdfplumber.open(pdf_file) as pdf:
    page = pdf.pages[2]
    text = page.extract_text()

new_transaction = re.compile(r'(\d{10}) (\d+/\d+/\d+) (\d+/\d+/\d+) ([^$]+) (.*)')

transactions_list = []

for line in text.split('\n'):
    line = new_transaction.search(line)
    if line:
        trans_id = line.group(1)
        trans_date = line.group(2)
        post_date = line.group(3)
        vendor = line.group(4)
        amount = line.group(5)
        transactions_list.append(Transactions(trans_id, trans_date, post_date, vendor, amount))

df = pd.DataFrame(transactions_list)

df.to_csv(f'transactions-{pdf_file_name}.csv')

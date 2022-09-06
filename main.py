import os.path
import re
import pdfplumber
import pandas as pd
from collections import namedtuple

Transactions = namedtuple('Transactions', 'transaction_id transaction_date post_date merchant amount')

pdf_file = 'statement_2022-05-25.pdf'
pdf_file_name = pdf_file.split('_')[1]
pdf_file_name = pdf_file_name.split('.')[0]

with pdfplumber.open(pdf_file) as pdf:
    page = pdf.pages
    for i, pg in enumerate(page):
        text = page[i].extract_text()

new_transaction = re.compile(r'(\d{10}) (\d+/\d+/\d+) (\d+/\d+/\d+) ([^$]+) (.*)')

transactions_list = []

for line in text.split('\n'):
    line = new_transaction.search(line)
    if line:
        transaction_id = line.group(1)
        transaction_date = line.group(2)
        post_date = line.group(3)
        merchant = line.group(4)
        amount = line.group(5)
        transactions_list.append(Transactions(transaction_id, transaction_date, post_date, merchant, amount))

df = pd.DataFrame(transactions_list)

df.to_csv(f'transactions-{pdf_file_name}.csv')

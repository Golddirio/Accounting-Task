#!/usr/bin/env python
# coding: utf-8

# In[15]:


pip install pandas openpyxl


# In[17]:


import pandas as pd
from datetime import datetime
import argparse
file_path = 'Prepayment assignment.xlsx'
df = pd.read_excel(file_path, sheet_name='Schedule', skiprows=2)

#rename the columns for easier access
df.columns = [
    'Items', 'Invoice number', 'Invoice amount', 
    'Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24', 
    'Jul-24', 'Aug-24', 'Sep-24', 'Oct-24', 'Nov-24', 'Dec-24', 'Balance'
]
def generate_entries(df, month, item_name):
    entries = []
    month_col = month.strftime('%b-%y')
    item_row = df[df['Items'] == item_name]
    if not item_row.empty:
        row = item_row.iloc[0]
        amount = row[month_col]

        if amount != 0:
            date = month.strftime('%d/%m/%Y')
            description = f"Prepayment amortisation for {item_name}"
            reference = row['Invoice number']
            expense_account = "EXP001"
            prepayment_account = "PRE001"

            # Expense entry
            entries.append({
                'Date': date,
                'Description': description,
                'Reference': reference,
                'Account': expense_account,
                'Amount': abs(amount)
            })

            # Prepayment entry
            entries.append({
                'Date': date,
                'Description': description,
                'Reference': reference,
                'Account': prepayment_account,
                'Amount': -abs(amount)
            })
    else:
        print(f"No data found for item: {item_name}")
    return entries
#This part is for command line users to input the items and the months they want to query. 
#Then to get items and months would be args.month and args.items. But the logic is the same. 
#parser = argparse.ArgumentParser(description="Generate accounting entries for specific prepaid items.")
#parser.add_argument('--items', type=str, nargs='+', required=True, help="Names of the items (e.g., Webhosting Insurance)")
#parser.add_argument('--month', type=str, required=True, help="Month in 'YYYY-MM-DD' format (e.g., 2024-05-31)")
#args = parser.parse_args()

items = ["Webhosting", "Insurance"]  
month = "2024-05-31"
# Parse the month argument into a datetime object
month = datetime.strptime(month, '%Y-%m-%d')
# Generate accounting entries for all specified items
all_entries = []
for item in items:
    entries = generate_entries(df, month, item)
    all_entries.extend(entries)

entries_df = pd.DataFrame(all_entries)
print(entries_df)


# In[1]:


get_ipython().system('jupyter nbconvert --to script assessment.ipynb')


# In[ ]:





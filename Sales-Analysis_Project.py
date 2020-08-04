import pandas as pd
import os
import matplotlib.pyplot as plt

pd.set_option('display.max_column', 20)
pd.set_option('display.width', 600)

# making a list of all file names
files = [file for file in os.listdir('./SalesAnalysis/Sales_Data/')]
# for file in os.listdir('./SalesAnalysis/Sales_Data/'):
#     files.append(file)

# creating a empty dataframe
all_months_data = pd.DataFrame()

# concatenating all datasets
for i in files:
    df = pd.read_csv('./SalesAnalysis/Sales_Data/' + i)
    all_months_data = pd.concat([df, all_months_data])

# Saving data to CSV
all_months_data.to_csv('all_months_data.csv', index=False)

data = pd.read_csv('all_months_data.csv')

# cleaning data
# dropping 'Or'
data = data[data['Order Date'].str[0:2] != 'Or']
# finding and dropping nan values
na_data = data[data.isna().any(axis=1)]
data = data.dropna(how='all')
# converting columns
# data['Quantity Ordered'] = data['Quantity Ordered'].astype(dtype='int32')
# data['Price Each'] = data['Price Each'].astype(dtype='Float32')
data['Quantity Ordered'] = pd.to_numeric(data['Quantity Ordered'])
data['Price Each'] = pd.to_numeric(data['Price Each'])

# adding a month column
data['Month'] = data['Order Date'].str[0:2]
data['Month'] = data['Month'].astype(dtype='int32')

# adding sales column
data['Sales'] = data['Quantity Ordered'] * data['Price Each']

# month of best sales
best_month = data.groupby('Month').sum()

# plotting bar graph of sales per month
months = range(1, 13)
plt.bar(months, best_month['Sales'])
plt.xticks(months)
plt.xlabel('Months')
plt.ylabel('Sales in USD($)')
plt.show()

# adding a city column
# creating a function to use in apply function
def get_city(address):
    return address.split(',')[1]


def get_state(address):
    return address.split(',')[2].split(' ')[1]


data['City'] = data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

# plotting graph of sales per city
cities = [city for city, df in data.groupby(['City'])]
plt.bar(cities,data.groupby(['City']).sum()['Sales'])
plt.ylabel('Sales in USD ($)')
plt.xlabel('city')
plt.xticks(cities, rotation='vertical', size=8)
plt.show()

# converting string to data and time format
data['Order Date'] = pd.to_datetime(data['Order Date'])
# creating a hour and minute column
data['Hour'] = data['Order Date'].dt.hour
data['Minute'] = data['Order Date'].dt.minute

# plotting graph of orders per hour
hours = [hour for hour, df in data.groupby(['Hour'])]
plt.plot(hours, data.groupby('Hour').count())
plt.ylabel('Orders')
plt.xlabel('Hours')
plt.xticks(hours)
plt.grid()
plt.show()

# finding the duplicate Order ID and grouping them by product
duplicate = data[data['Order ID'].duplicated(keep=False)]
duplicate['Grouped'] = duplicate.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
# removing duplicates
duplicate = duplicate[['Order ID','Grouped']].drop_duplicates()

# importing tools to iterate and count
from itertools import combinations
from collections import Counter

count = Counter()
for row in duplicate['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key, value in count.most_common(10):
    print(key,value)

# Grouping by the product
product_group = data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']
# plotting graph of sales per city
products = [product for product, df in product_group]
plt.bar(products,quantity_ordered)
plt.ylabel('Quantity Ordered')
plt.xlabel('Products')
plt.xticks(products, rotation='vertical', size=8)
plt.show()

# calculating the mean of product prices
prices = data.groupby('Product').mean()['Price Each']
# plotting subplot for product,quantity_ordered and prices
fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, color='b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)

plt.show()
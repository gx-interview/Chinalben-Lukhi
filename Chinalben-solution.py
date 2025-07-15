import pandas as pd

data = pd.read_csv('source.csv')
print(data)
print(data.dtypes)

# Converting datetime datatype from string to datetime format
data['Datetime'] = pd.to_datetime(data['Datetime'])
print(data.dtypes)

# Shifting time to UTC+6
data['Datetime'] = data['Datetime'].dt.tz_localize('UTC').dt.tz_convert('Asia/Almaty')
print(data.dtypes)

productA_prices = data[data['Name'] == 'ProductA'].set_index('Datetime')['Price']

def total(row):
    if row['Name'] == 'ProductA':
        if row['Purity'] == 'Impure': 
            price = row['Price'] * 0.75
        else:
            price = row['Price']
        total_value = row['Amount'] * price
        return total_value
    else:
        a_price = productA_prices[row['Datetime']]
        diff = row['Price'] - a_price
        if row['Purity'] == 'Impure':
            diff *= 0.75
        total_value = row['Amount'] * diff
        return total_value

data['total'] = data.apply(total, axis=1)
data['total'] = data['total'].round(2)
data.to_csv('result.csv', index=False)

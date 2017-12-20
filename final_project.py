import matplotlib.pyplot as plt
import time
import datetime
import seaborn as sns
import pandas as pd
import pandas_datareader.data as web

sns.set_context("poster")
sns.set_style("ticks")


TIME = time.strftime("%Y,%m,%d", time.localtime()).split(',')
start_date = datetime.datetime(int(TIME[0])-1, int(TIME[1]), int(TIME[2]))
end_date = datetime.datetime(int(TIME[0]), int(TIME[1]), int(TIME[2]))
print("Start date: {}\n End date: {}".format(start_date, end_date))


def datareader(i:str) -> web.DataReader:
    try:
        df = web.DataReader(i, 'yahoo', start_date, end_date)
    except:
        df = datareader(i)
    return df


stock_indexes = ['^IXIC', '^NYA', '^DJI', '^GSPC', '000001.SS', '^STOXX50E']

tickers_input = input('Please the names of stock tickers you want to search: ')
tickers = tickers_input.split(',')
for i in range(0, len(tickers)):
    tickers[i] = tickers[i].strip()
indexes_max = []
tickers_max = []

print('In Processing. Please be patient.')


all_name = stock_indexes + tickers
all_data = {ticker: datareader(ticker) for ticker in all_name}
price = pd.DataFrame({ticker: data['Adj Close'] for ticker, data in all_data.items()})
price_vary = price.pct_change()


corr = price_vary.corr()
print(corr)
print('\n')


n = 0
for i in stock_indexes:
    for j in tickers:
        if j == tickers[0]:
            indexes_max.append([j, price_vary[i].corr(price_vary[j])])
        elif price_vary[i].corr(price_vary[j]) > indexes_max[n][1]:
            indexes_max[n] = [j, price_vary[i].corr(price_vary[j])]
    print('The best correlation for {} is {}, the value is {}.'.format(i, indexes_max[n][0], indexes_max[n][1]))
    n += 1
    if i == stock_indexes[5]:
        n = 0
print('\n')



for i in tickers:
    for j in stock_indexes:
        if j == stock_indexes[0]:
            tickers_max.append([j, price_vary[i].corr(price_vary[j])])
        elif price_vary[i].corr(price_vary[j]) > tickers_max[ii][1]:
            tickers_max[ii] = [j, price_vary[i].corr(price_vary[j])]
    print('The best correlation for {} is {}, the value is {}.'.format(i, tickers_max[ii][0], tickers_max[ii][1]))
    ii += 1
    if i == tickers[len(tickers) - 1]:
        ii = 0
print('\n')




for i in tickers:
    for j in stock_indexes:
        for k in range(-5, 6):
            if k == 0:
                continue
            if price_vary[i].shift(k).corr(price_vary[j]) > price_vary[i].corr(price_vary[j]):
                print('For {}, it got a better correlation with {} when shifted {} days, the corresponding '
                      'correlation is {}.'.format(i, j, k, price_vary[i].shift(k).corr(price_vary[j])))



plt.figure()
for i in tickers:
    plt.plot(price[i], label = i)
plt.legend(loc='upper right')
plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Price Lines")
plt.show()

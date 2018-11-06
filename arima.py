import pandas as pd
import csv
import datetime
import matplotlib.pyplot as plt
f = open('week1.csv', 'r')
flag = -1
tms = []
data = []
reader = csv.reader(f, delimiter=',')
for row in reader:
	if flag == -1:
		flag = 0
		continue
	prot = row[2].replace(' ', '')
	if prot != 'TCP':
		continue 
	# print(row[2])
	try:
		data.append(int(row[8]))
		tms.append(datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'))
	except Exception as e:
		continue
	if len(tms) > 1000000:
		break
st = tms[0]
cnt = 0
sums = 0
points = []
x = []
y= []
#print(len(tms), len(data))
for i in range(len(data)):
	if tms[i] > st + datetime.timedelta(seconds = 60):
		st = st + datetime.timedelta(seconds = 60)
		points.append([cnt, sums])
		x.append(cnt)
		y.append(sums)
		# print([cnt, sums])
		cnt = 0
		sums = 0
	sums = sums + data[i]
	cnt = cnt+1
	if len(points) > 100000:
		break

import csv
from datetime import timedelta, date
start_date = date(2013, 1, 1)
d = start_date
delta = datetime.timedelta(days=1)
with open('flow_col.csv', mode='w') as f:
    w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(x)):
        w.writerow([d.strftime("%Y-%m-%d"), float(x[i])])
        d+=delta
data = pd.read_csv('flow_col.csv',index_col=0)
data.head()
data.index = pd.to_datetime(data.index)
import plotly
from plotly.plotly import plot_mpl
plotly.tools.set_credentials_file(username='Dipendrasingh', api_key='3QsW03xW7rQadLNm9AVj')
from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(data, model='multiplicative')
fig = result.plot()
plot_mpl(fig)
from pyramid.arima import auto_arima
stepwise_model = auto_arima(data, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
print(stepwise_model.aic())

train = data[0:len(data)*0.67]
test = data[len(data)*0.68:]
stepwise_model.fit(train)
future_forecast = stepwise_model.predict(n_periods=37)
future_forecast = pd.DataFrame(future_forecast,index = test.index,columns=['Prediction'])
pd.concat([test,future_forecast],axis=1).iplot()
pd.concat([data,future_forecast],axis=1).iplot()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Consulta (BD firefox na pasta ~/.mozilla/firefox/*.default/places.sqlite )
# SELECT datetime(visit_date/1000000,'unixepoch') AS Time,url FROM moz_historyvisits, moz_places WHERE moz_historyvisits.place_id=moz_places.id ORDER BY Time DESC

with open('hist.txt') as f:
    content = f.readlines()

# Limpeza dos dados da consulta
raw_data = [line.split('|', 1) for line in [x.strip() for x in content]]

# Colocanda as datas de acesso de cada pagina no formato DateTime
data = pd.DataFrame(raw_data, columns=['datetime', 'url'])
data.datetime = pd.to_datetime(data.datetime)

# Contando o numero de ocorrencias de cada site 
hour_freq = data.datetime.dt.hour.value_counts().to_frame()
hour_freq.reset_index(level=0, inplace=True)
hour_freq.columns = ['hour_of_day', 'count']
hour_freq.sort_values(by="hour_of_day", inplace=True)

# plot preparation
fig = plt.figure()
ax = fig.add_subplot(111)

x_labels = hour_freq['hour_of_day'].tolist()
y_values = hour_freq['count'].tolist()
plt.plot(x_labels, y_values, marker='o') # plot the graph

# Annotating the y_values on the data points
for xy in zip(x_labels,y_values):                                       
    ax.annotate('%s' % xy[1], xy=xy, textcoords='data')

# x labels tange and titles
plt.xticks(np.arange(min(x_labels), max(x_labels)+1, 2.0))
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Pages')
plt.title('Browser History Analysis')
plt.grid(True)

plt.savefig('plot_browser_hist_2017-2018(feb)1.png')
plt.show()

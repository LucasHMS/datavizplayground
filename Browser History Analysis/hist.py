import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlparse

# Consulta (BD firefox na pasta ~/.mozilla/firefox/*.default/places.sqlite )
# SELECT datetime(visit_date/1000000,'unixepoch') AS Time,url FROM moz_historyvisits, moz_places WHERE moz_historyvisits.place_id=moz_places.id ORDER BY Time DESC

with open('hist.txt') as f:
    content = f.readlines()

# Limpeza dos dados da consulta
raw_data = [line.split('|', 1) for line in [x.strip() for x in content]]

# Colocanda as datas de acesso de cada pagina no formato DateTime
data = pd.DataFrame(raw_data, columns=['datetime', 'url'])
data.datetime = pd.to_datetime(data.datetime)

# Limpando as URLs, deixando somente os dominios e subdominios
parser = lambda u: urlparse(u).netloc
data.url = data.url.apply(parser)

# Contando o numero de ocorrencias de cada site 
site_frequencies = data.url.value_counts().to_frame()
site_frequencies.reset_index(level=0, inplace=True)
site_frequencies.columns = ['domain', 'count']

# plot num grafico de pizza
topN = 20
print(site_frequencies.head(20))
plt.figure(1, figsize=(10,10))
plt.title('Top $n Sites Visited'.replace('$n', str(topN)))
pie_data = site_frequencies['count'].head(topN).tolist()
pie_labels = None
pie_labels = site_frequencies['domain'].head(topN).tolist()
plt.pie(pie_data, autopct='%1.1f%%', labels=pie_labels)
plt.savefig('plot_browser_hist_2017-2018(feb).png')
plt.show()
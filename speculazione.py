
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
prezzi = pd.read_csv('https://dgsaie.mise.gov.it/open_data_export.php?export-id=2&export-type=csv', sep=',', error_bad_lines=False, header=0)
prezzi
import yfinance as yf

# Ticker per il Brent
brent_ticker = yf.Ticker("BZ=F")

# Ticker per il WTI
wti_ticker = yf.Ticker("CL=F")

# Ottieni i dati storici per il Brent
brent_df = brent_ticker.history(period="max")

# Ottieni i dati storici per il WTI
wti_df = wti_ticker.history(period="max")

# Stampa i primi 5 record dei prezzi del Brent
print(brent_df["Close"].head())

# Stampa i primi 5 record dei prezzi del WTI
print(wti_df["Close"].head())
import yfinance as yf

# Ticker per il cambio EUR/USD
eurusd_ticker = yf.Ticker("EURUSD=X")

# Ottieni i dati storici per il cambio EUR/USD
eurusd_df = eurusd_ticker.history(period="max")

eurusd_df




eurusd_df.index = pd.to_datetime(eurusd_df.index).date
wti_df.index = pd.to_datetime(wti_df.index).date

prezzi["Date"] = pd.to_datetime(prezzi["DATA_RILEVAZIONE"])

prezzi.index = pd.to_datetime(prezzi.index).date

prezzi = prezzi.set_index('DATA_RILEVAZIONE')
wti_eur = pd.merge(eurusd_df, wti_df, left_index=True, right_index=True)
wti_eur.dropna()
wti_eur

wti_eur.index = pd.to_datetime(wti_eur.index)
wti_eur = wti_eur[wti_eur.index >= '2005-01-03']



prezzi.index = pd.to_datetime(prezzi.index)

wti_eur_ben = pd.merge(wti_eur, prezzi, left_index=True, right_index=True)

def_wti_eur = wti_eur_ben[['Close_x', 'Close_y', 'BENZINA']]
def_wti_eur = wti_eur_ben.loc[:, ['Close_x', 'Close_y', 'BENZINA']]

df=def_wti_eur.rename(columns={'Close_x':'EurDol','Close_y': 'WTI'})
df["wtieur"] = df["WTI"] / df["EurDol"]
df["ben100"] = df["BENZINA"] / 1000

df['ben7'] = df['ben100'].rolling(window=7).mean()
df['wtieur7'] = df['WTI'].rolling(window=7).mean()

df["rap_WTI_BEN"] = df["ben7"] / (df["wtieur7"] /158.98)

import matplotlib.pyplot as plt
import seaborn as sns

# Calcola la media mobile a 7 giorni
df['rap_WTI_BEN_mm'] = df['rap_WTI_BEN'].rolling(window=7).mean()

# Calcola la deviazione standard a 7 giorni
df['rap_WTI_BEN_std'] = df['rap_WTI_BEN'].rolling(window=7).std()

# Traccia la line plot dei dati
sns.lineplot(data=df, x='index', y='rap_WTI_BEN')

# Traccia le bande di sigma
plt.fill_between(df.index, df['rap_WTI_BEN_mm'] - df['rap_WTI_BEN_std'], df['rap_WTI_BEN_mm'] + df['rap_WTI_BEN_std'], color='gray', alpha=0.5)
plt.fill_between(df.index, df['rap_WTI_BEN_mm'] - 2*df['rap_WTI_BEN_std'], df['rap_WTI_BEN_mm'] + 2*df['rap_WTI_BEN_std'], color='gray', alpha=0.2)
plt.fill_between(df.index, df['rap_WTI_BEN_mm'] - 3*df['rap_WTI_BEN_std'], df['rap_WTI_BEN_mm'] + 3*df['rap_WTI_BEN_std'], color='gray', alpha=0.1)

# Mostra il grafico
plt.show()


import matplotlib.pyplot as plt
import numpy as np

# Calcola la media e la deviazione standard dei valori della colonna rap_WTI_BEN
mean = df['rap_WTI_BEN'].mean()
std = df['rap_WTI_BEN'].std()

# Calcola gli intervalli 1, 2 e 3 sigma
interval_1 = mean + std
interval_2 = mean + 2 * std
interval_3 = mean + 3 * std

# Crea il grafico
plt.plot(df.index, df['rap_WTI_BEN'])
plt.axhline(y=mean, color='r', linestyle='-')
plt.axhline(y=interval_1, color='g', linestyle='--')
plt.axhline(y=interval_2, color='y', linestyle='--')
plt.axhline(y=interval_3, color='b', linestyle='--')
plt.xlabel('Data')
plt.ylabel('Valore')
plt.title('Andamento storico rap_WTI_BEN')
sns.set_palette("pastel")

plt.show()


import matplotlib.pyplot as plt
import pandas as pd
plt.figure(figsize=(32, 18))
# Calcola la media mobile a 30 giorni e gli intervalli di sigma
df['rap_WTI_BEN_mean'] = df['rap_WTI_BEN'].rolling(window=30).mean()
df['rap_WTI_BEN_std'] = df['rap_WTI_BEN'].rolling(window=30).std()
df['rap_WTI_BEN_std_upper_1'] = df['rap_WTI_BEN_mean'] + df['rap_WTI_BEN_std']
df['rap_WTI_BEN_std_upper_2'] = df['rap_WTI_BEN_mean'] + 2 * df['rap_WTI_BEN_std']
df['rap_WTI_BEN_std_upper_3'] = df['rap_WTI_BEN_mean'] + 3 * df['rap_WTI_BEN_std']
df['rap_WTI_BEN_std_lower_1'] = df['rap_WTI_BEN_mean'] - df['rap_WTI_BEN_std']
df['rap_WTI_BEN_std_lower_2'] = df['rap_WTI_BEN_mean'] - 2 * df['rap_WTI_BEN_std']
df['rap_WTI_BEN_std_lower_3'] = df['rap_WTI_BEN_mean'] - 3 * df['rap_WTI_BEN_std']

# Disegna il grafico dell'andamento storico della colonna rap_WTI_BEN
plt.plot(df.index, df['rap_WTI_BEN'], label='rap_WTI_BEN')
plt.plot(df.index, df['rap_WTI_BEN_mean'], label='mean')
plt.fill_between(df.index, df['rap_WTI_BEN_std_upper_3'], df['rap_WTI_BEN_std_lower_3'], alpha=0.2, label='+3 Sigma')
plt.fill_between(df.index, df['rap_WTI_BEN_std_upper_2'], df['rap_WTI_BEN_std_lower_2'], alpha=0.2, label='+2 Sigma')
plt.fill_between(df.index, df['rap_WTI_BEN_std_upper_1'], df['rap_WTI_BEN_std_lower_1'], alpha=0.2, label='+1 Sigma')
plt.legend()
plt.show()


import matplotlib.pyplot as plt
import pandas as pd
plt.figure(figsize=(32, 18))
# Calcola la media mobile a 30 giorni e gli intervalli di sigma
df['rap_WTI_BEN_mean'] = df['rap_WTI_BEN'].rolling(window=30).mean()
df['rap_WTI_BEN_std'] = df['rap_WTI_BEN'].rolling(window=30).std()
df['rap_WTI_BEN_std_upper_1'] = df['rap_WTI_BEN_mean'] + df['rap_WTI_BEN_std']
df['rap_WTI_BEN_std_upper_2'] = df['rap_WTI_BEN_mean'] + 2 * df['rap_WTI_BEN_std']
df['rap_WTI_BEN_std_upper_3'] = df['rap_WTI_BEN_mean'] + 3 * df['rap_WTI_BEN_std']
df['rap_WTI_BEN_std_lower_1'] = df['rap_WTI_BEN_mean'] - df['rap_WTI_BEN_std']
df['rap_WTI_BEN_std_lower_2'] = df['rap_WTI_BEN_mean'] - 2 * df['rap_WTI_BEN_std']
df['rap_WTI_BEN_std_lower_3'] = df['rap_WTI_BEN_mean'] - 3 * df['rap_WTI_BEN_std']

# Disegna il grafico dell'andamento storico della colonna rap_WTI_BEN
plt.plot(df.index, df['rap_WTI_BEN'], label='Rapporto in € fra Benzina senza accise e WTI', linewidth=4, color='blue')
plt.plot(df.index, df['rap_WTI_BEN_mean'], label='Media mobile 30gg',  linewidth=4, color='red')
plt.fill_between(df.index, df['rap_WTI_BEN_std_upper_3'], df['rap_WTI_BEN_std_lower_3'], alpha=0.2, label='+3 Sigma')
plt.fill_between(df.index, df['rap_WTI_BEN_std_upper_2'], df['rap_WTI_BEN_std_lower_2'], alpha=0.2, label='+2 Sigma')
plt.fill_between(df.index, df['rap_WTI_BEN_std_upper_1'], df['rap_WTI_BEN_std_lower_1'], alpha=0.2, label='+1 Sigma')
plt.legend()
plt.rcParams.update({'font.size': 30})
plt.ylim(0,3)
plt.grid(visible=True, color='gray', linestyle='--', linewidth=0.5)
plt.show()

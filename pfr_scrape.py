from bs4 import BeautifulSoup
import requests
import pandas as pd

pfr = 'https://www.pro-football-reference.com'

latest_year = 2022
earliest_year = 1970

cols = ['uid','name','pos']
for year in range(latest_year, earliest_year - 1, -1):
    cols.append(str(year))

df = pd.DataFrame(columns=cols)

id_set = set()

for year in range(latest_year, earliest_year - 1, -1):
    r = requests.get(pfr + '/years/' + str(year) + '/fantasy.htm')
    soup = BeautifulSoup(r.content, 'html.parser')
    parsed_table = soup.find_all('table')[0]

    for i,row in enumerate(parsed_table.find_all('tr')[2:]):
        dat = row.find('td', attrs={'data-stat': 'player'})
        try:
            name = dat.a.get_text()
            id = dat.get('data-append-csv')
            pos = row.find('td', attrs={'data-stat': 'fantasy_pos'}).get_text()
            half_ppr = round(float(row.find('td', attrs={'data-stat': 'fantasy_points_ppr'}).get_text()) - (float(row.find('td', attrs={'data-stat': 'rec'}).get_text()) / 2), 1)

            if id not in id_set:
                df.loc[len(df), 'uid'] = id
                df.loc[len(df) - 1, 'name'] = name
                df.loc[len(df) - 1, 'pos'] = pos
                df.loc[len(df) - 1, str(year)] = half_ppr
            else:
                row = df[df['uid']==id].index
                df.loc[row, str(year)] = half_ppr
        except:
            pass
    id_set = set(df['uid'])



df
df.to_csv('output.csv', index=False)
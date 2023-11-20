import pandas as pd
import requests
import time
import tqdm

df = pd.read_csv("data.csv")
df.insert(3, 'img', None)

found = 0
not_found = 0

with tqdm.tqdm(total=df.shape[0]) as pbar:
	for index, data in df.iterrows():
		pbar.update(1)
		try:
			id = data['uid']
			letter = id[0]
			player_url = f"https://www.pro-football-reference.com/players/{letter}/{id}.htm"
			r = requests.get(player_url)
			if r.status_code == 429:
				print(f"Too many requests at index {index}.")
				break
			try:
				line = r.text.split('\n')[244]
				img_url = line.split('\"')[3]
				if img_url.endswith(".jpg"):
					df.loc[index, 'img'] = img_url
					found += 1
				else:
					not_found += 1
			except IndexError:
				not_found += 1
			time.sleep(3.1)
		except:
			print(f"{found} images found")
			print(f"{not_found} images not found")
			df.to_csv('output.csv', index=False)
			break

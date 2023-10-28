from nflplayers.models import NFLPlayer
import pandas as pd
from django.core.exceptions import ValidationError
import numpy as np
from math import isnan

def populate_db(csv_path):
    df = pd.read_csv(csv_path)
    #df = df.where(pd.notnull(df), None)
    NFLPlayer.objects.all().delete()
    for row, data in df.iterrows():
        player = NFLPlayer()
        player.pk = row + 1
        player.uid = data['uid']
        player.name = data['name']
        player.pos = data['pos']
        for year in range(1970, 2023):
            if not isnan(data[str(year)]):
                setattr(player, f"fp_{year}", float(data[str(year)]))
        player.save()

populate_db("data.csv")
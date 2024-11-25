import sqlite3
import pandas as pd
import numpy as np
from math import isnan

def populate_db(csv_path, db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Delete all existing records in the api_nflplayer table
    cursor.execute("DELETE FROM api_nflplayer")
    conn.commit()

    cursor.execute("ALTER TABLE api_nflplayer ADD COLUMN fp_2023 REAL")
    conn.commit()

    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Iterate over the rows in the dataframe and insert them into the database
    for row, data in df.iterrows():
        # Prepare the values for the new player
        uid = data['uid']
        name = data['name']
        pos = data['pos'] if isinstance(data['pos'], str) else "WR"  # For positionless players
        name_searchable = data['name'].replace("'", "").replace("-", " ").replace(".", "")

        # Prepare the columns for the query (years 1970 to 2022)
        player_data = {'uid': uid, 'name': name, 'pos': pos, 'name_searchable': name_searchable}
        for year in range(1970, 2024):
            if not isnan(data.get(str(year), float('nan'))):
                player_data[f"fp_{year}"] = float(data[str(year)])

        years_with_points = []
        for year in range(1970, 2024):  # Adjust according to data range
            if player_data.get(f"fp_{year}") is not None:
                years_with_points.append(year)
        if years_with_points:
            years_played = f"({min(years_with_points)}-{max(years_with_points)})"
            player_data['years_played'] = years_played
        
        # Create the placeholders for the insert statement
        columns = ', '.join(player_data.keys())
        placeholders = ', '.join('?' * len(player_data))
        
        # Create the SQL query
        query = f"INSERT INTO api_nflplayer ({columns}) VALUES ({placeholders})"
        
        # Execute the insert query with the player data
        cursor.execute(query, tuple(player_data.values()))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Run the function to populate the database
populate_db("data.csv", "db.sqlite3")

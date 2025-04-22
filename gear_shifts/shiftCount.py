import pandas as pd

data = pd.read_csv('fsae_michigan18_&_madformulateam_mft02_evo_&_Yak_5150_&_stint_3.csv')

lap_group = data.groupby('Lap')

shifts_per_lap = {}

for lap, lap_data in lap_group:

    gear_column = lap_data['Gear']

    shifts = 0
    for i in range(1, len(lap_data)):
        if gear_column.iloc[i] != 0 and gear_column.iloc[i] != gear_column.iloc[i-1]:
            shifts += 1

    shifts_per_lap[lap] = shifts

for lap, shifts in shifts_per_lap.items():
        print(f"Lap {lap}: {shifts} shifts")
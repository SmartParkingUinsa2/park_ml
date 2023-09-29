import pandas as pd

# to create dummy
from faker import Faker
import numpy as np
import random

# Create a Faker object
fake = Faker()

# Generate fake data for your dataset
days = []
areas = []
hours = []
counts = []
densities = []

# Define the list
list_days = ["senin", "selasa", "rabu", "kamis", "jumat"]
list_hours = ["07.00", "12.00", "16.00"]
list_areas = ["FST", "Danau", "Masjid", "FISIP", "FPK"]

# Define the number of rows for each day
rows_per_day = 15
rows_per_hour = 5
rows_per_area = 1

# Define the total number of days to repeat the pattern
total_days = 500
total_hours = 1500
total_areas = 7500

# Loop to add to list
for day_idx in range(total_days):
    day = list_days[day_idx % len(list_days)]
    for _ in range(rows_per_day):
        days.append(day)

for hour_idx in range(total_hours):
    hour = list_hours[hour_idx % len(list_hours)]
    for _ in range(rows_per_hour):
        hours.append(hour)

for area_idx in range(total_areas):
    area = list_areas[area_idx % len(list_areas)]
    for _ in range(rows_per_area):
        areas.append(area)

for count_idx in range(7500):
    d_day = list_days[count_idx % len(list_days)]
    d_hour = list_hours[count_idx % len(list_hours)]
    d_area = list_areas[count_idx % len(list_areas)]

    if d_day == "senin":
      count = random.randint(80, 100)
    elif d_day == "selasa":
      count = random.randint(90, 110)
    elif d_day == "rabu":
      count = random.randint(80, 100)
    elif d_day == "kamis":
      count = random.randint(70, 90)
    elif d_day == "jumat":
      count = random.randint(50, 70)

    if d_hour == "07.00":
      count = count + 30
    elif d_hour == "12.00":
      count = count + 50
    elif d_hour == "16.00":
      count = count + 0

    if d_area == "FST":
      count = count + 100
    elif d_area == "Danau":
      count = count + 100
    elif d_area == "Masjid":
      count = count + 50
    elif d_area == "FISIP":
      count = count + 150
    elif d_area == "FPK":
      count = count + 50

    counts.append(count)

for densities_idx in range(7500):
  d_area = list_areas[densities_idx % len(list_areas)]
  d_count = counts[densities_idx]
  # FST
  if d_area == "FST":
    if d_count < 200:
      density = "sepi"
    elif d_count < 230:
      density = "renggang"
    else:
      density = "penuh"
  # Danau
  if d_area == "Danau":
    if d_count < 200:
      density = "sepi"
    elif d_count < 230:
      density = "renggang"
    else:
      density = "penuh"
  # Masjid
  if d_area == "Masjid":
    if d_count < 150:
      density = "sepi"
    elif d_count < 180:
      density = "renggang"
    else:
      density = "penuh"
  # FISIP
  if d_area == "FISIP":
    if d_count < 250:
      density = "sepi"
    elif d_count < 280:
      density = "renggang"
    else:
      density = "penuh"
  # FPK
  if d_area == "FPK":
    if d_count < 150:
      density = "sepi"
    elif d_count < 200:
      density = "renggang"
    else:
      density = "penuh"
  densities.append(density)


pd.set_option('display.max_rows', 10)
# Create a Pandas DataFrame from the list of dictionaries
data = pd.DataFrame({"hari": days, "jam": hours, "area": areas, "jumlah": counts, "kepadatan": densities})

# Save the DataFrame to a CSV file
data.to_csv('dummy_parkir.csv', index=False)
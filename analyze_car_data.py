import pandas as pd
import numpy as np
from datetime import datetime

# Read the data
df = pd.read_excel('car.xlsx')

print("=== VIETNAMESE CAR MARKET DATA ANALYSIS ===")
print(f"Total records: {len(df):,}")
print(f"Date range: {df['list_time'].min()} to {df['list_time'].max()}")
print()

# Convert timestamp to datetime for better analysis
df['list_date'] = pd.to_datetime(df['list_time'], unit='ms')

print("=== TOP BRANDS BY LISTING COUNT ===")
brand_counts = df['brand'].value_counts().head(10)
for brand, count in brand_counts.items():
    print(f"{brand}: {count:,} listings")
print()

print("=== PRICE ANALYSIS ===")
print(f"Average price: {df['price'].mean():,.0f} VND")
print(f"Median price: {df['price'].median():,.0f} VND")
print(f"Price range: {df['price'].min():,.0f} - {df['price'].max():,.0f} VND")
print()

print("=== TOP BRANDS BY AVERAGE PRICE ===")
brand_avg_price = df.groupby('brand')['price'].agg(['mean', 'count']).sort_values('mean', ascending=False)
brand_avg_price = brand_avg_price[brand_avg_price['count'] >= 10]  # Filter brands with at least 10 listings
for brand in brand_avg_price.head(10).index:
    avg_price = brand_avg_price.loc[brand, 'mean']
    count = brand_avg_price.loc[brand, 'count']
    print(f"{brand}: {avg_price:,.0f} VND ({count} listings)")
print()

print("=== FUEL TYPE DISTRIBUTION ===")
fuel_counts = df['fuel'].value_counts()
for fuel, count in fuel_counts.items():
    percentage = (count / len(df)) * 100
    print(f"{fuel}: {count:,} ({percentage:.1f}%)")
print()

print("=== GEARBOX DISTRIBUTION ===")
gearbox_counts = df['gearbox'].value_counts()
for gearbox, count in gearbox_counts.items():
    percentage = (count / len(df)) * 100
    print(f"{gearbox}: {count:,} ({percentage:.1f}%)")
print()

print("=== CONDITION DISTRIBUTION ===")
condition_counts = df['condition'].value_counts()
for condition, count in condition_counts.items():
    percentage = (count / len(df)) * 100
    print(f"{condition}: {count:,} ({percentage:.1f}%)")
print()

print("=== MILEAGE ANALYSIS ===")
print(f"Average mileage: {df['mileage_v2'].mean():,.0f} km")
print(f"Median mileage: {df['mileage_v2'].median():,.0f} km")
print(f"Mileage range: {df['mileage_v2'].min():,.0f} - {df['mileage_v2'].max():,.0f} km")
print()

# Price per kilometer analysis
df['price_per_km'] = df['price'] / df['mileage_v2']
print("=== PRICE PER KILOMETER ANALYSIS ===")
print(f"Average price per km: {df['price_per_km'].mean():,.0f} VND/km")
print(f"Median price per km: {df['price_per_km'].median():,.0f} VND/km")
print()

print("=== TOP MODELS BY LISTING COUNT ===")
model_counts = df['model'].value_counts().head(10)
for model, count in model_counts.items():
    print(f"{model}: {count:,} listings")
print()

# Sample of recent listings
print("=== SAMPLE RECENT LISTINGS ===")
recent_listings = df.sort_values('list_time', ascending=False).head(5)
for _, row in recent_listings.iterrows():
    print(f"{row['brand']} {row['model']} - {row['price']:,.0f} VND - {row['mileage_v2']:,} km - {row['condition']}") 
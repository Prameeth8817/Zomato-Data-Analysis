# Importing the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("zomato.csv", encoding='latin-1')

# Display the first few rows of the dataset
print(df.head())

# Data Cleaning
# Remove duplicates
df.drop_duplicates(inplace=True)

# Remove unnecessary columns
df = df.drop(['address', 'phone'], axis=1)

# Cleaning the rate column (removing '/5' and converting to float)
df['rate'] = df['rate'].replace('NEW', np.NaN)
df['rate'] = df['rate'].replace('-', np.NaN)
df['rate'] = df['rate'].astype(str).apply(lambda x: x.split('/')[0].strip()).replace('', np.NaN)
df['rate'] = df['rate'].astype(float)

# Filling missing values in rate with the mean rate
df['rate'].fillna(df['rate'].mean(), inplace=True)

# Clean the 'cost' column by removing commas and converting to numeric
df['approx_cost(for two people)'] = df['approx_cost(for two people)'].apply(lambda x: str(x).replace(',', '') if ',' in str(x) else x)
df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'], errors='coerce')

# Drop rows with missing values in the 'approx_cost(for two people)' column
df.dropna(subset=['approx_cost(for two people)'], inplace=True)

# Filling NaN values in 'cuisines' with mode
df['cuisines'].fillna(df['cuisines'].mode()[0], inplace=True)

# Analyzing Restaurants by Location
location_counts = df['location'].value_counts()

# Plotting the number of restaurants in each location
plt.figure(figsize=(12, 8))
sns.barplot(y=location_counts.index[:10], x=location_counts.values[:10], palette='coolwarm')
plt.title('Top 10 Locations with Most Restaurants', fontsize=16)
plt.xlabel('Number of Restaurants')
plt.ylabel('Location')
plt.show()

# Analyzing Rating Distribution
plt.figure(figsize=(8,6))
sns.distplot(df['rate'], bins=20, color='purple')
plt.title('Distribution of Restaurant Ratings')
plt.xlabel('Ratings')
plt.ylabel('Frequency')
plt.show()

# Analyzing Cost vs Rating
plt.figure(figsize=(10,6))
sns.scatterplot(x='rate', y='approx_cost(for two people)', data=df, hue='online_order', palette='viridis')
plt.title('Cost for Two People vs Rating')
plt.xlabel('Rating')
plt.ylabel('Cost for Two People')
plt.show()

# Checking whether restaurants with online ordering have higher ratings
plt.figure(figsize=(6,6))
sns.boxplot(x='online_order', y='rate', data=df, palette='Set1')
plt.title('Online Ordering vs Ratings')
plt.show()

# Most popular cuisines
top_cuisines = df['cuisines'].value_counts().head(10)

# Plotting top cuisines
plt.figure(figsize=(12, 8))
sns.barplot(y=top_cuisines.index, x=top_cuisines.values, palette='magma')
plt.title('Top 10 Most Popular Cuisines', fontsize=16)
plt.xlabel('Number of Restaurants')
plt.ylabel('Cuisines')
plt.show()

# Top Restaurant Chains
top_restaurant_chains = df['name'].value_counts().head(10)

# Plotting top restaurant chains
plt.figure(figsize=(12, 8))
sns.barplot(y=top_restaurant_chains.index, x=top_restaurant_chains.values, palette='cubehelix')
plt.title('Top 10 Restaurant Chains in Zomato', fontsize=16)
plt.xlabel('Number of Restaurants')
plt.ylabel('Restaurant Chain')
plt.show()

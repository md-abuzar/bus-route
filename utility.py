import pandas as pd
import re

# Slugify function to convert text to SEO-friendly URL
def slugify(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s-]', '', text)  # Remove special characters (except hyphens and spaces)
    text = re.sub(r'[\s_-]+', '-', text)  # Replace spaces, underscores, or multiple hyphens with a single hyphen
    text = re.sub(r'^-+|-+$', '', text)  # Remove leading or trailing hyphens
    return text

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('pmpl/tripsnew.csv')  # Replace with the path to your CSV file

# Apply the slugify function to the 'bus_num' column and create a new 'slug' column
df['slug'] = df['route_short_name'].apply(slugify)

# Save the DataFrame with the new 'slug' column to a new CSV file
df.to_csv('new_pmpml_routes.csv', index=False)

print("CSV file has been processed and saved as 'output.csv'")

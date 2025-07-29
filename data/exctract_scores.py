import pandas as pd

BASE_DIR = "data/"

# Input and output file paths
input_file = BASE_DIR + "results.csv"   # Replace with your actual file name
output_file = BASE_DIR+ "scores.csv"

# Load the CSV
df = pd.read_csv(input_file, sep=';')

### FILTER ###
# Remove all rows where 'UniversityExperience' is 'No'
df = df[(df['UniversityExperience'] == 'No')]

# Remove all students before 2023
df = df.dropna(subset=['GraduateYear'])
df['GraduateYear'] = pd.to_numeric(df['GraduateYear'], errors='coerce')
specific_graduateyears = [2023, 2024] 
df = df[(~df['GraduateYear'].isin(specific_graduateyears))]

print(f"The dataset has {len(df['Total'])} student submissions.")

### PREP DF ###
# Select only columns that end with '_points'
points_columns = [col for col in df.columns if col.endswith('_points')]

# Extract only those columns
df_points = df[points_columns]

# Rename columns, remove _points suffix
df_points.columns = [col.replace('_points', '') for col in df_points.columns]

# Write to new CSV
df_points.to_csv(output_file, index=False)

print(f"Saved {len(points_columns)} columns to {output_file}")

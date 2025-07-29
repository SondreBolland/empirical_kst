import argparse
import pandas as pd
from learning_spaces.kst import iita
from learning_spaces.kst import hasse
from learning_spaces.pks import blim

# ----------------------
# Argument parser setup
# ----------------------
parser = argparse.ArgumentParser(description="Run IITA and BLIM on binary student task data.")
parser.add_argument("--rows", type=int, default=10, help="Number of rows to sample from the dataset")
args = parser.parse_args()

# ----------------------
# Load and prepare data
# ----------------------
input_file = "data/scores.csv"
df = pd.read_csv(input_file, sep=',')
tasks = list(df.columns)

print("Data loaded")

# Sample the requested number of rows
df = df.sample(n=args.rows, random_state=42)

# Convert to binary
df_numeric = df.apply(pd.to_numeric, errors='coerce')
df_binary = df_numeric.fillna(0).gt(0).astype(int)
df_binary = df_binary[df_binary.sum(axis=1) > 0]  # Drop all-zero rows
print("Dataframe ready for analysis")

# ----------------------
# Run analyses
# ----------------------
print("Running analysis...")
response = iita(df_binary, v=1)
#model = blim(df_binary, v=1)

# ----------------------
# Output results
# ----------------------
implications = response["implications"]
error_rate = response["error.rate"]
print("Implications:", implications)
print("Error rate:", error_rate)

with open("implications.txt", "w") as f:
    f.write(str(implications))

# ----------------------
# Hasse Diagram
# ----------------------
hasse(imp=implications, n_items=len(tasks), labels=tasks)
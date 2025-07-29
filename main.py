import pandas as pd
from IPython.display import display
from learning_spaces.kst import iita

# Load the CSV file
input_file = "data/scores.csv"  # Replace with actual file name
df = pd.read_csv(input_file, sep=',')

# Convert to binary (1 = any non-zero, 0 = zero or NaN)
# Coerce all values to numeric (non-numeric become NaN), then convert to binary
df_numeric = df.apply(pd.to_numeric, errors='coerce')
df_binary = df_numeric.fillna(0).gt(0).astype(int)

# Drop students who answered no tasks
df_binary = df_binary[df_binary.sum(axis=1) > 0]


display(df_binary)
# Run IITA
response = iita(df_binary, v=1)

# Print the result
print("Implications:", response["implications"])
print("Error rate:", response["error.rate"])

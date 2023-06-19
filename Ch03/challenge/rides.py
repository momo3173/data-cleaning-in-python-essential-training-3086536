# %%
import pandas as pd

df = pd.read_csv('rides.csv')
df
# %%
# - Missing values are not allowed
missing_values = df.isnull().any(axis=1)
df[missing_values]

#%%
# - A plate must be a combination of at least 3 upper case letters or digits
plate_combination = ~df["plate"].str.contains(r'[0-9]|[A-Z]{3,}', na=False)
df[plate_combination]

#%%
# - Distance much be bigger than 0
dist_b_zero = df["distance"] < 0
df[dist_b_zero]

#%%
# Find out all the rows that have bad values
all_bad = missing_values | plate_combination | dist_b_zero
df[all_bad]
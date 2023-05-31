import pandas as pd
from xlwings import view


# Read in file for Makeover Monday
df = pd.read_excel("C:/Users/billy/OneDrive/Desktop/Professional/Courses/Data Vis UC Davis/Railroad infrastructure quality.xlsx")

# Remove whitespace from column names
df.columns = [str.strip(x) for x in df.columns]

# Sort by year reported, keep country record by most recent year reported
df = df.sort_values(by='Year', axis=0, ascending=False)
df = df.drop_duplicates(subset=['Countries'])

# Create a new ranking by average score (1 = best)
df = df.sort_values(by='Railroad infrastructure quality', axis=0, ascending=False)
df['Rank'] = df['Railroad infrastructure quality'].rank(method="min", ascending=False).astype(int)

# Find rank outcomes that are ties - add a "T-" before each instance for the Tableau visuals
duped_values = df.Rank.value_counts()[df.Rank.value_counts() > 1].index


def label_maker(country_rank, country_name):
    """
    Takes an element from the Rank column, and returns either the original value 
    or the original value with a "T-" in front for ties, followed by the country name.
    """
    if country_rank in duped_values.to_list():
        return "T-" + str(country_rank) + ". " + country_name
    else:
        return str(country_rank) + ". " + country_name
    

# Create new string in format of [ranking]. [Country] for planned Tableau visuals
df['rank_country'] = df.apply(lambda row: label_maker(row.Rank, row.Countries), axis=1)

# Drop index and unneeded columns
df = df.reset_index(drop=True)
df = df.drop(['Global rank'], axis=1)

# Order by rank, then alphabetize - for arranging the Tableau visuals
df = df.sort_values(['Rank', 'Countries'], ascending=[True, True])
df['index'] = pd.Series(df.index + 1)

view(df) # Verify df was cleaned properly

# Write cleaned file to csv for Tableau to read
df.to_csv("C:/Users/billy/OneDrive/Desktop/Professional/Courses/Data Vis UC Davis/Railroad infrastructure quality cleaned.csv", index=False)

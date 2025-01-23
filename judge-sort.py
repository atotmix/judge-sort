import pandas as pd
from collections import defaultdict
import numpy as np
judges = pd.DataFrame

try:
    judges = pd.read_csv("data-in/judges.csv")
except:
    raise FileNotFoundError("Failed to read CSV file. Ensure the judges.csv file exists")

expected_headers = ['Email', 'CC email (assistant or other colleague)', 'Mobile phone (Used only for comms at an event. No marketing.)', 'First name', 
                    'Last name', 'Job title', 'Company name', 'City', 'Preferred Pronouns', 'Ethnic Group', 
                    'If you are neurodivergent, please check this box so that we can get in touch with you to discuss any specific requirements you may have to ensure your experience with us is as productive and enjoyable as possible', 
                    'Are you part of an Agency Holding Company?', "If you selected 'Other', which one?\xa0", 'Company type', 'If you selected "Other", which one?', 
                    'Job Role/Department', 'Seniority Level', 'Years of Experience', 'Brand # 1', 'Brand # 2', 'Brand # 3', 'First choice for judging', 'Second choice for judging', 
                    '<p>If judging in-person on 5th September, are you able to join us for the drinks reception afterwards?</p>\n<p>(6pm-8pm)</p>',
                    'Have you judged for the Effies in the past?', 'If you’re new to Effie judging or would like a refresher we’re holding two online training sessions.\xa0 Please choose the session you would like to join.', 
                    'Dietary Restrictions/Allergies (for in-person judging)', 'Are you interested in any of the following?', 
                    'Conversion Date', 'Conversion Page', 'Conversion Title', 'Contact first name', 'Contact last name', 'Contact email', 'Contact ID']

#Ensure that all headers are present - making sure that the correct file is being loaded
if judges.columns.to_list() != expected_headers:
    print("This dataset does not contain the required headers.\nPlease ensure that you have placed the correct file in data-in/judges.csv")  

    missing_headers = [header for header in expected_headers if header not in judges.columns.to_list()]
    extra_headers = [header for header in judges.columns.to_list() if header not in expected_headers]
    
    error_message = "Header validation failed:\n"
    if missing_headers:
        error_message += f"  - Missing headers: {missing_headers}\n"
    if extra_headers:
        error_message += f"  - Unexpected headers: {extra_headers}\n"
    raise ValueError(error_message)

#Drop any duplicates if present - likely not but just in case as this data is collected by hand
judges.drop_duplicates()

#Ensure every row has the data that we're going to be using. 
required_columns = ['Email', 'First name', 'Last name', 'Job title', 'Company name', 'Preferred Pronouns', 'Ethnic Group']

missing_data = judges[required_columns].isnull()
rows_with_missing_data = missing_data.any(axis=1)


if rows_with_missing_data.any():
    # Get rows with missing data and their indices
    problematic_rows = judges[rows_with_missing_data]
    raise ValueError(
        f"Validation failed! The following rows have missing data in required columns:\n"
        f"{problematic_rows}"
    )


def distribute_teams(df, group_cols, n_groups):
    """
    Distributes individuals in a DataFrame into groups by first evenly distributing underrepresented groups
    and then using a round-robin approach for larger groups.

    Args:
        df (pd.DataFrame): The DataFrame containing individuals with their attributes.
        group_cols (list): Columns that define groups.
        n_groups (int): The number of groups to distribute individuals into.

    Returns:
        list: A list of DataFrames, each representing a group.
    """
    # Identify groups
    df['group'] = df[group_cols].apply(lambda row: tuple(row), axis=1)
    
    # Identify underrepresented groups (only one individual in the group)
    group_counts = df['group'].value_counts()
    underrepresented_groups = group_counts[group_counts == 1].index
    
    #print(underrepresented_groups)
    # Initialize groups
    groups = [pd.DataFrame() for _ in range(n_groups)]
    
    # Distribute underrepresented groups first
    for idx, group in enumerate(underrepresented_groups):
        person = df[df['group'] == group]
        groups[idx % n_groups] = pd.concat([groups[idx % n_groups], person])
        df = df[df['group'] != group]  # Remove distributed individuals
    
    # Distribute the rest of the dataset
    group_counts = df['group'].value_counts()
    group_buckets = defaultdict(list)
    for group, count in group_counts.items():
        group_buckets[group] = list(df[df['group'] == group].index)
    
    # Shuffle indices for randomness
    all_indices = list(df.index)
    np.random.shuffle(all_indices)
    
    # Distribute remaining individuals
    for idx, person_idx in enumerate(all_indices):
        #Ensure that 
        groups[idx % n_groups] = pd.concat([groups[idx % n_groups], df.loc[[person_idx]]])
    
    # Drop the helper 'group' column before returning
    for i in range(n_groups):
        groups[i] = groups[i].drop(columns=['group'])

    return groups


diversity_columns = ['Preferred Pronouns', 'Ethnic Group', 'Years of Experience']

teams = distribute_teams(judges,diversity_columns, len(judges) // 11 + 1)

for i, team in enumerate(teams):
    team.to_csv(f'data-out/team_{i}.csv', index=False)
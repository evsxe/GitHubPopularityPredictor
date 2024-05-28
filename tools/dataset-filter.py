import pandas as pd
from collections import Counter

file_path = 'Updated_Most_starred_Github_Repositories_Limited.csv'
df = pd.read_csv(file_path)

all_users = df['star_users'].str.split('|').explode()
user_counts = Counter(all_users)

users_to_keep = {user for user, count in user_counts.items() if count >= 2}

def filter_and_append_users(star_users):
    users = str(star_users).split('|')
    filtered_users = [user for user in users if user in users_to_keep]

    if len(filtered_users) < 1000:
        remaining_users = [user for user in users if user not in filtered_users]
        filtered_users += remaining_users[:1000 - len(filtered_users)]

    return '|'.join(filtered_users)


df['star_users'] = df['star_users'].apply(filter_and_append_users)

output_file_path = 'Filtered_and_Completed_Most_starred_Github_Repositories.csv'
df.to_csv(output_file_path, index=False)

from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup

file_path = 'most_popular_repositories.csv'
data = pd.read_csv(file_path, skip_blank_lines=True)

def get_star_users(repo_url):
    star_users = []
    page = 60
    while True:
        try:
            response = requests.get(f'{repo_url}/stargazers?page={page}')
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                user_elements = soup.select('ol.d-block li div a.d-inline-block')
                if not user_elements:
                    break
                for user in user_elements:
                    user_profile = user['href']
                    if user_profile.startswith('/'):
                        username = user_profile.split('/')[-1]
                        if username and username not in star_users:
                            star_users.append(username)
                page += 1
                if page > 100:
                    break
                print(page)
            else:
                print(f"Ошибка при запросе к {repo_url}: {response.status_code}")
                break
        except Exception as e:
            print("Слишком много запросов на сервер. Программа остановлена на 10 секунд...")
            sleep(10)
            continue

    return star_users

updated_data = []

for index, row in data.iterrows():
    star_users = get_star_users(row['repo_url'])
    row['star_users'] = '|'.join(star_users)
    updated_data.append(row)
    print("OK")

updated_data_df = pd.DataFrame(updated_data)

output_path = 'Updated_Most_starred_Github_Repositories_Limited.csv'
updated_data_df.to_csv(output_path, index=False, lineterminator='\n')

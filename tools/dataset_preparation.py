import pandas as pd

# Загрузка датасета
file_path = 'Most starred Github Repositories.csv'
df = pd.read_csv(file_path)

sorted_data = df.drop_duplicates(subset='repo_url').sort_values(by='stars', ascending=False)

# Извлечение 250 самых популярных репозиториев
top_250_repos = sorted_data.head(250)

# Выводим результат
top_250_repos[['repo_name', 'stars', 'repo_url']]

# Сохранение результатов в новые CSV файлы
most_popular_path = 'most_popular_repositories.csv'

top_250_repos.to_csv(most_popular_path, index=False)

import csv
from collections import defaultdict
import graphviz


def read_csv(file_path):
    repo_users = defaultdict(set)

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            repo_name = row['repo_name']
            star_users = row['star_users'].strip().split('|')
            for user in star_users:
                repo_users[repo_name].add(user)

    return repo_users


def build_graph(repo_users):
    dot = graphviz.Graph('Repositories')

    # add vertex
    for repo in repo_users.keys():
        dot.node(repo)

    # add edge
    repos = list(repo_users.keys())
    for i in range(len(repos)):
        for j in range(i + 1, len(repos)):
            common_users = repo_users[repos[i]].intersection(repo_users[repos[j]])
            if common_users:
                label = f"{len(common_users)}"

                # ToDo: needed ?
                # Display user names that match
                # if len(common_users) == 1:
                #     label += f" ({list(common_users)[0]})"
                # else:
                #     label += f" ({', '.join(common_users)})"

                dot.edge(repos[i], repos[j], label=label)

    return dot

file_path = '../datasets/test-data-star-git-rep.csv'
repo_users = read_csv(file_path)
graph = build_graph(repo_users)
graph.render('repositories_graph', format='png')
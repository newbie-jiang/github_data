import requests
import json

USERS = ["newbie-jiang", "LibDriver"]  # 在这里加你想展示的用户名
OUTPUT_PATH = "repos_data.json"

def fetch_repos(username):
    per_page = 100
    page = 1
    all_repos = []
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"请求失败，用户:{username}，状态码: {response.status_code}")
            break
        repos = response.json()
        if not repos:
            break
        for repo in repos:
            all_repos.append({
                "name": repo["name"],
                "description": repo["description"] or "（无简介）",
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo["language"] or "未指定",
                "pushed_at": repo["pushed_at"],
                "created_at": repo["created_at"],
            })
        page += 1
    return all_repos

if __name__ == "__main__":
    all_data = []
    for username in USERS:
        repos = fetch_repos(username)
        all_data.append({"username": username, "repos": repos})
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print("✅ 多用户 JSON 数据生成完毕:", OUTPUT_PATH)

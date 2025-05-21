import requests
import json
from datetime import datetime, timedelta
from operator import itemgetter

OUTPUT_PATH = "output/index.html"
USERNAME = "newbie-jiang"

def fetch_repos(username):
    per_page = 100
    page = 1
    all_repos = []

    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
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
                "created_at": repo["created_at"]
            })

        page += 1

    return all_repos

def save_to_html(data, username):
    # 获取当前 UTC 时间并转换为北京时间
    now_utc = datetime.utcnow()
    now_beijing = now_utc + timedelta(hours=8)
    update_time_str = now_beijing.strftime("%Y-%m-%d %H:%M:%S")

    data.sort(key=itemgetter("pushed_at"), reverse=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(f"""<html>
<head>
    <meta charset="utf-8">
    <title>{username} 的 GitHub 仓库</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        a {{ color: #007bff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}

        /* 右上角更新时间样式 */
        .update-time {{
            position: fixed;
            top: 10px;
            right: 10px;
            font-size: 14px;
            color: #666;
            background: #f9f9f9;
            padding: 5px 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            z-index: 1000;
        }}
    </style>
</head>
<body>
    <div class="update-time">文档当前更新：{update_time_str}</div>
    <h2>GitHub 用户 <code>{username}</code> 的仓库（共 {len(data)} 个）</h2>
    <table>
        <tr>
            <th>名称</th><th>描述</th><th>语言</th><th>⭐</th><th>🍴</th><th>更新时间</th>
        </tr>
""")
        for repo in data:
            try:
                utc_time = datetime.strptime(repo["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
                beijing_time = utc_time + timedelta(hours=8)
                time_str = beijing_time.strftime("%Y-%m-%d %H:%M")
            except:
                time_str = "未知"

            f.write(f"""<tr>
<td><a href="{repo['url']}" target="_blank">{repo['name']}</a></td>
<td>{repo['description']}</td>
<td>{repo['language']}</td>
<td>{repo['stars']}</td>
<td>{repo['forks']}</td>
<td>{time_str}</td>
</tr>\n""")
        f.write("</table></body></html>")
    print(f"✅ HTML 文件已生成：{OUTPUT_PATH}")

if __name__ == "__main__":
    repos = fetch_repos(USERNAME)
    save_to_html(repos, USERNAME)

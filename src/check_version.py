# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME check_version
AUTHOR Pfolg
TIME 2025/7/18 14:12
"""
import requests


def get_latest_github_version(owner, repo):
    """从GitHub API获取最新Release版本号"""
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()["tag_name"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"GitHub API error: {str(e)}")


def check_version_match(local_ver):
    """主检查函数"""
    # 配置参数
    REPO_OWNER = "Pfolg"
    REPO_NAME = "QuickTray"

    try:
        remote_ver = get_latest_github_version(REPO_OWNER, REPO_NAME)
        if remote_ver == local_ver:
            print(f"✅ 版本一致 (本地: {local_ver}, GitHub: {remote_ver})")
            return True, f"当前版本 {remote_ver} 已是最新版！"
        else:
            print(f"❌ 版本不一致 (本地: {local_ver}, GitHub最新: {remote_ver})")
            return False, f"GitHub 最新发布 {remote_ver} \n当前 {local_ver}"

    except Exception as e:
        print(f"⚠️ 检查失败: {str(e)}")
        return False, str(e)


if __name__ == "__main__":
    check_version_match("ver1.11.2-25718")

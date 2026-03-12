import os
import subprocess
import datetime

def init_git_repo(repo_path: str, repo_url: str) -> bool:
    """
    初始化Git仓库
    :param repo_path: 本地仓库路径
    :param repo_url: GitHub仓库URL
    :return: 是否成功
    """
    try:
        # 确保目录存在
        os.makedirs(repo_path, exist_ok=True)
        
        # 切换到仓库目录
        original_cwd = os.getcwd()
        os.chdir(repo_path)
        
        # 初始化Git仓库
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True, capture_output=True)
        
        # 创建README.md
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write('# AI-IT-News-Archive\n\nA repository for storing daily IT and AI news summaries.\n')
        
        # 初始提交
        subprocess.run(['git', 'add', 'README.md'], check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'AI News Bot'], check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'ai-news-bot@example.com'], check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True, capture_output=True)
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True, capture_output=True)
        
        # 切换回原目录
        os.chdir(original_cwd)
        return True
    except Exception as e:
        print(f"初始化Git仓库时出错: {e}")
        return False

def push_to_github(local_file: str, repo_path: str, commit_message: str = None) -> bool:
    """
    将文件推送到GitHub
    :param local_file: 本地文件路径
    :param repo_path: 本地仓库路径
    :param commit_message: 提交消息
    :return: 是否成功
    """
    try:
        # 确保仓库目录存在
        os.makedirs(repo_path, exist_ok=True)
        
        # 计算目标文件路径
        file_name = os.path.basename(local_file)
        dest_dir = os.path.join(repo_path, 'news_archives')
        os.makedirs(dest_dir, exist_ok=True)
        dest_file = os.path.join(dest_dir, file_name)
        
        # 复制文件到仓库
        import shutil
        shutil.copy2(local_file, dest_file)
        
        # 切换到仓库目录
        original_cwd = os.getcwd()
        os.chdir(repo_path)
        
        # 检查是否需要初始化Git
        if not os.path.exists('.git'):
            print("Git仓库未初始化，正在初始化...")
            return False
        
        # 添加文件
        subprocess.run(['git', 'add', f'news_archives/{file_name}'], check=True, capture_output=True)
        
        # 提交
        if not commit_message:
            commit_message = f"Add news summary for {file_name.split('_')[0]}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True)
        
        # 推送
        subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)
        
        # 切换回原目录
        os.chdir(original_cwd)
        return True
    except Exception as e:
        print(f"推送文件到GitHub时出错: {e}")
        return False

def clone_github_repo(repo_url: str, local_path: str) -> bool:
    """
    克隆GitHub仓库
    :param repo_url: GitHub仓库URL
    :param local_path: 本地路径
    :return: 是否成功
    """
    try:
        # 确保目录不存在
        if os.path.exists(local_path):
            import shutil
            shutil.rmtree(local_path)
        
        # 克隆仓库
        subprocess.run(['git', 'clone', repo_url, local_path], check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"克隆GitHub仓库时出错: {e}")
        return False

if __name__ == "__main__":
    # 测试
    repo_url = "https://github.com/liandyao/AI-IT-News-Archive.git"
    local_repo = os.path.join(os.getcwd(), "github_repo")
    
    # 克隆仓库
    if clone_github_repo(repo_url, local_repo):
        print("仓库克隆成功")
    
    # 推送测试文件
    test_file = "test.md"
    with open(test_file, 'w') as f:
        f.write("# Test File\n")
    
    if push_to_github(test_file, local_repo):
        print("文件推送成功")
    
    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
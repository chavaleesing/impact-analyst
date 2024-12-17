import gitlab
import git
import os

# Set up your GitLab URL and token
GITLAB_URL = 'https://gitdev.devops.krungthai.com'
PRIVATE_TOKEN = 'glpat-v9XrKuPojWVTPyx6yiYJ'

local_mapping = {
    "/Users/a677034/arise/repo/bo": "newwelfare/web-portal/services",

}

# Local directory to store the cloned repositories
LOCAL_DIR = '/Users/a677034/arise/repo/processor'

# Initialize the GitLab connection
gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)

# Get the group (replace GROUP_ID with your group id or group name)
group = gl.groups.get('newwelfare/services')

# Fetch all projects within the group
projects = group.projects.list(all=True)

# Clone or pull the latest changes from each repository
for project in projects:
    try:
        repo_url = project.ssh_url_to_repo  # You can also use project.http_url_to_repo for HTTPS cloning
        repo_name = project.path
        repo_path = os.path.join(LOCAL_DIR, repo_name)

        if not os.path.exists(repo_path):
            print(f"Cloning {repo_name}...")
            # git.Repo.clone_from(repo_url, repo_path)
        else:
            print(f"{repo_name} already exists locally. Pulling the latest changes...")

            try:
                repo = git.Repo(repo_path)
                # Fetch the latest branches from the remote
                repo.remotes.origin.fetch()

                # Get all remote branches (without the 'origin/' prefix)
                remote_branches = [ref.name.replace('origin/', '') for ref in repo.remotes.origin.refs]

                # Find the most recent branch (based on commit time)
                latest_branch = None
                for branch in remote_branches:
                    # Check if the branch exists on remote
                    if branch in remote_branches:
                        # Get the latest branch (sorting based on commit date)
                        if latest_branch is None:
                            latest_branch = branch
                        else:
                            branch_commit_date = repo.commit(f'origin/{branch}').committed_datetime
                            latest_commit_date = repo.commit(f'origin/{latest_branch}').committed_datetime
                            if branch_commit_date > latest_commit_date:
                                latest_branch = branch

                if latest_branch:
                    print(f"Switching to the latest branch: {latest_branch}")
                    # Checkout the latest branch (without 'origin/' prefix)
                    repo.git.checkout(latest_branch)

                    # Pull the latest changes from the selected branch
                    repo.remotes.origin.pull(latest_branch)
                    print(f"Pulled latest changes from {latest_branch}")
                else:
                    print(f"No remote branches found for {repo_name}.")
            except Exception as e:
                print(f"Error pulling {repo_name}: {e}")
    except Exception as e:
        print(f"Error on {repo_name}: {e}")

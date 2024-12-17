import os
import git

# Path to the parent directory containing repositories
REPO_DIR = '/Users/a677034/arise/repo/bo'  # Replace with the path to your directory containing repositories

def pull_latest_branch(repo_dir):
    # Iterate over all items in the folder
    for root, dirs, files in os.walk(repo_dir):
        # Check if '.git' folder exists (indicating it's a git repository)
        if '.git' in dirs:
            try:
                # Initialize the repo object
                repo = git.Repo(root)
                print(f"Processing repository in {root}")
                
                # Fetch the latest changes from remote
                repo.remotes.origin.fetch()

                # Get all remote branches
                remote_branches = [ref.name.replace('origin/', '') for ref in repo.remotes.origin.refs]
                
                # If no branches are found, skip the repo
                if not remote_branches:
                    print(f"No branches found in {root}. Skipping...")
                    continue

                # Find the latest branch based on the commit date
                latest_branch = None
                latest_commit_date = None
                for branch in remote_branches:
                    try:
                        # Get the commit date of the branch
                        commit_date = repo.commit(f'origin/{branch}').committed_datetime
                        if latest_commit_date is None or commit_date > latest_commit_date:
                            latest_commit_date = commit_date
                            latest_branch = branch
                    except git.exc.GitCommandError:
                        print(f"Error accessing commit info for branch {branch} in {root}. Skipping...")

                if latest_branch:
                    print(f"Switching to the latest branch: {latest_branch}")
                    # Checkout to the latest branch
                    repo.git.checkout(latest_branch)

                    # Pull the latest changes from the selected branch
                    repo.remotes.origin.pull(latest_branch)
                    print(f"Successfully pulled latest changes from {latest_branch}")
                else:
                    print(f"No valid branch found for {root}. Skipping...")
            except Exception as e:
                print(f"Error pulling repo in {root}: {e}")
        # Stop descending into subdirectories once we reach repositories
        dirs[:] = []

# Call the function
pull_latest_branch(REPO_DIR)

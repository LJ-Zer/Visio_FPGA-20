import os
import subprocess
import sys
import time

# Path to the local repository directory
repository_path = "/home/ubuntu/Desktop/Visio_FPGA/Facial_Recog/Face-Detected"

# Configure Git with user name and email (optional, can be set globally)
subprocess.run(['git', 'config', '--global', 'user.email', '20-06391@g.batstate-u.edu.ph'])
subprocess.run(['git', 'config', '--global', 'user.name', 'Zer-000'])

try:
  # Ensure GIT_TOKEN environment variable is set (security best practice)
  git_token = os.environ.get('GIT_TOKEN')
  if not git_token:
    print("Error: GIT_TOKEN environment variable not set. Please set it with your PAT.")
    sys.exit(1)

  while True:
    # Change to the repository directory
    os.chdir(repository_path)

    # Pull the latest changes from the remote repository
    subprocess.run(['git', 'pull', 'origin', 'master'], env={'GIT_TOKEN': git_token})

    # Add all tracked files (including new images)
    subprocess.run(['git', 'add', '.'])

    # Commit changes with a descriptive message (consider adding timestamp)
    commit_message = f"Automatic Upload - {time.strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(['git', 'commit', '-m', commit_message])

    # # Option 1: Using environment variable (preferred)
    # subprocess.run(['git', 'push', 'origin', 'master'], env={'GIT_TOKEN': git_token})

    # # Option 2: Explicitly setting username with PAT (alternative)
    subprocess.run(['git', 'push', 'origin', 'master', '--token', git_token])

    # Add a delay of 5 seconds before the next iteration
    time.sleep(5)

except KeyboardInterrupt:
  sys.exit()

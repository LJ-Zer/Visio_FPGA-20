import os
import subprocess
import sys
import time

# Path to the local repository directory
repository_path = "/home/ubuntu/Desktop/Visio_FPGA/Facial_Recog/Face-Detected"

# Configure Git with user name and email
subprocess.run(['git', 'config', '--global', 'user.email', '20-06391@g.batstate-u.edu.ph'])
subprocess.run(['git', 'config', '--global', 'user.name', 'Zer-000'])

try:
  git_token = os.environ.get('GIT_TOKEN')
  if not git_token:
    print("Error: GIT_TOKEN environment variable not set. Please set it with your PAT.")
    sys.exit(1)

  while True:
    GIT_TOKEN = "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"
    # Change to the repository directory
    os.chdir(repository_path)

    # Pull the latest changes from the remote repository
    subprocess.run(['git', 'pull', 'origin', 'master'], env={'GIT_TOKEN': git_token})

    # Add all tracked files (including new images)
    subprocess.run(['git', 'add', '.'])

    # Commit changes with a descriptive message (consider adding timestamp)
    commit_message = f"Automatic Upload - {time.strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(['git', 'commit', '-m', commit_message])

    # Push changes to the remote repository
    subprocess.run(['git', 'push', 'origin', 'master'], env={'GIT_TOKEN': git_token})

    # Add a delay of 5 seconds before the next iteration
    time.sleep(5)

except KeyboardInterrupt:
  sys.exit()

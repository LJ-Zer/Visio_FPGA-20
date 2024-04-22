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
  git_token = os.environ.get('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')
  if not git_token:
    print("Error: GIT_TOKEN environment variable not set. Please set it with your PAT.")
    sys.exit(1)

  while True:
    # Change to the repository directory
    os.chdir(repository_path)

    # Pull the latest changes from the remote repository
    subprocess.run(['git', 'pull', 'origin', 'master'], env={'GIT_TOKEN': git_token})

    # ... (rest of your script)

except KeyboardInterrupt:
  sys.exit()

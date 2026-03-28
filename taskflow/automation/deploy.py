import subprocess
import sys

EC2_HOST = "52.73.114.168"
EC2_USER = "ec2-user"
KEY_PATH = "/workspaces/taskflow/taskflow-key.pem"
IMAGE = "vidya2407/taskflow:latest"

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def deploy():
    print("🚀 Starting deployment to AWS EC2...")
    print("-" * 50)

    ssh_base = f"ssh -i {KEY_PATH} -o StrictHostKeyChecking=no {EC2_USER}@{EC2_HOST}"

    print("📦 Pulling latest Docker image...")
    run_command(f'{ssh_base} "sudo docker pull {IMAGE}"')

    print("🛑 Stopping old container...")
    run_command(f'{ssh_base} "sudo docker stop taskflow || true"')
    run_command(f'{ssh_base} "sudo docker rm taskflow || true"')

    print("▶️ Starting new container...")
    code = run_command(f'{ssh_base} "sudo docker run -d --name taskflow -p 5000:5000 {IMAGE}"')

    if code == 0:
        print("-" * 50)
        print(f"✅ Deployment successful!")
        print(f"🌐 App running at: http://{EC2_HOST}:5000")
    else:
        print("❌ Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    deploy()
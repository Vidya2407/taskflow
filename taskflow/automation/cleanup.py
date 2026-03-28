import subprocess
import sys
import os

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def cleanup():
    print("🧹 TaskFlow AWS Cleanup")
    print("-" * 50)
    print("⚠️  This will DESTROY all AWS resources!")
    print("This includes: EC2, VPC, Security Groups, Subnets")
    print("-" * 50)

    confirm = input("Are you sure? Type 'yes' to confirm: ")
    if confirm.lower() != "yes":
        print("❌ Cleanup cancelled!")
        sys.exit(0)

    print("\n🗑️ Destroying AWS infrastructure with Terraform...")
    os.chdir("/workspaces/taskflow/taskflow/terraform")
    code = run_command("terraform destroy -auto-approve")

    if code == 0:
        print("-" * 50)
        print("✅ All AWS resources destroyed successfully!")
        print("💰 No more charges will be incurred!")
    else:
        print("❌ Cleanup failed — check errors above!")

if __name__ == "__main__":
    cleanup()
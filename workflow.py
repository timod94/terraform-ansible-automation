import subprocess
import json
import os

TERRAFORM_DIR = "../terraform"
ANSIBLE_INVENTORY = "./inventory.ini"
ANSIBLE_PLAYBOOK = "../ping-playbook.yml"

def run_terraform():
    try:
        subprocess.run([ "terraform", "init" ], cwd=TERRAFORM_DIR, check=True)

        subprocess.run(["terraform", "apply", "-auto-approve"], cwd=TERRAFORM_DIR, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Fehler bei Terraform: {e}")
        exit(1)

def get_terraform_output():
    try:
        result = subprocess.run(
            ["terraform", "output", "-json"], cwd=TERRAFORM_DIR, check=True, capture_output=True
        )
        output = json.loads(result.stdout)
        return output

    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Abrufen des Terraform Outputs: {e}")
        exit(1)

def create_ansible_inventory(terraform_output):
    with open(ANSIBLE_INVENTORY, "w") as f:
        f.write("[all]\n")
        for instance in terraform_output["instances"]["value"]:
            ip_address = instance["ip_address"]
            username = instance["username"]
            key_name = instance["key_name"]
            private_key_path = os.path.expanduser("~/.ssh/id_rsa")
            f.write(f"{ip_address} ansible_user={username} ansible_ssh_private_key_file={private_key_path}\n")

    print(f"Ansible Inventory wurde in {ANSIBLE_INVENTORY} erstellt")

def run_ansible_playbook():
    try:
        subprocess.run(
            ["ansible-playbook", "-i", ANSIBLE_INVENTORY, ANSIBLE_PLAYBOOK],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen des Ansible Playbooks: {e}")
        exit(1)

if __name__=="__main__":

    run_terraform()

    terraform_output = get_terraform_output()

    create_ansible_inventory(terraform_output)

    run_ansible_playbook()
import subprocess
import Utilities.Settings as Settings

# Now you can use the secrets dictionary to access your secrets
settings = Settings.get_settings('settings/secrets.json')

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error:
        print(f"Error: {error}")
    else:
        return output.decode()

# Check if Docker is installed
docker_version = run_command("docker -v")

if not docker_version:
    print("Docker is not installed. Installing Docker...")
    # Update package list and install prerequisites
    run_command("sudo apt update")
    run_command("sudo apt install apt-transport-https ca-certificates curl software-properties-common")
    # Add Docker's official GPG key
    run_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
    # Add Docker's stable repository
    run_command('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')
    # Update package list again
    run_command("sudo apt update")
    # Install Docker
    run_command("sudo apt install docker-ce")
    print("Docker installed successfully.")
else:
    print("Docker is already installed.")

# Pull the official MySQL image
print("Pulling MySQL Docker image...")
run_command("sudo docker pull mysql")

# Start a MySQL container
print("Starting MySQL container...")
run_command(f"sudo docker run --name mysql-container -e MYSQL_ROOT_PASSWORD={settings['database-root-password']} -d mysql")

print("MySQL container started successfully.")
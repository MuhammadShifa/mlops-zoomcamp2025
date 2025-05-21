# 🛠️ MLOps Zoomcamp - Environment Setup (1.2a)

This guide walks through configuring your MLOps Zoomcamp environment using **GitHub Codespaces**, **VS Code**, **Anaconda (Python 3.9)**, and **Docker** — all managed cleanly, especially for Ubuntu users.

---

## ✅ Step 1: Create and Open GitHub Codespaces

1. Create a new **public GitHub repository**, e.g.:

   ```
   mlops-zoomcamp2025
   ```

2. Go to your repository → click on the green **"Code"** button → select **"Codespaces"** tab → click **"Create codespace on main"**.

3. It will open a **VS Code environment in the browser** with Docker already installed.

4. Test Docker inside Codespaces:
   ```bash
   docker run hello-world
   ```

---

## 🚨 Optional: Install Docker (if missing inside Codespaces or locally on Ubuntu)

If Docker is not installed, follow these commands:

```bash
# Remove older versions (optional)
sudo apt remove docker docker-engine docker.io containerd runc

# Update packages
sudo apt update

# Install dependencies
sudo apt install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker’s official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add Docker repo
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update and install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# To run docker without sudo
sudo groupadd docker
sudo usermod -aG docker $USER


# Test Docker installation
sudo docker run hello-world
```
---

## ✅ Step 2: Use VS Code Locally for Better Experience

Browser-based Codespaces are not ideal for Jupyter and MLflow.

1. Install **VS Code** locally from:  
   👉 https://code.visualstudio.com/

2. In VS Code, install the extension:  
   ➕ `GitHub Codespaces`

3. From your GitHub repo, click **"Open with VS Code"** to connect your local VS Code with Codespaces.

---

## ✅ Step 3: Check Python Version

Open a terminal in your Codespaces (either browser or VS Code):

```bash
python -V
```

If Python version is **not 3.9**, proceed to install Anaconda manually.

---

## ✅ Step 4: Install Anaconda with Python 3.9

1. Download Anaconda (2022 version includes Python 3.9):

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh
```

Follow the prompts and confirm everything (use default settings).

---

## ✅ Step 5: Verify Anaconda and Python Version

After installation, either restart terminal or run:

```bash
source ~/.bashrc
```

Then verify Python path and version:

```bash
which python
python -V
```

You should now see Python 3.9 from Anaconda.

---

## ✅ Step 6: Create a seperate Folder for notebook  and Open Jupyter Notebook

1. Create the notebook folder:

```bash
mkdir notebook
cd notebook
```

2. Launch Jupyter Notebook from vs code terminal not browser

```bash
jupyter notebook
```

3. Ports will be **automatically forwarded** by VS Code — you can now open and use the notebook in your browser.

---

## ✅ Step 7: Install Required Python Packages

Inside the notebook or terminal:

```bash
# jupyter notebook
!pip install pyarrow
# terminal
pip install pyarrow

```

---

✅ **You're ready to go!** Your environment now supports Docker, Jupyter, Python 3.9, and package installation — fully compatible with the MLOps Zoomcamp workflow.

# ☁️ MLOps Zoomcamp - Environment Setup with AWS EC2 (1.2b)

This guide outlines how to set up your MLOps Zoomcamp development environment using **AWS EC2**, **SSH config**, **Anaconda**, **Docker**, and **VS Code** with remote access.

---

## ✅ Step 1: Launch EC2 Instance

1. Log in to your AWS Management Console.
2. Navigate to **EC2** → click **Launch Instance**.
3. Configure the instance:
   - **Name**: `mlops-zoomcamp`
   - **AMI (OS)**: Choose Ubuntu 20.04 (recommended)
   - **Instance type**: e.g., t2.medium (you can choose according to free tier or course need)
   - **Key pair**: Create a new `.pem` key or use an existing one (download it and save to `~/.ssh/`)
   - **Security Group**:
     - Allow **SSH (port 22)**
     - Add a custom rule for **Jupyter (port 8888)** → allow from your IP

---

## ✅ Step 2: Connect to EC2 via SSH

Use the following command format from your terminal:

```bash
ssh -i ~/.ssh/your-key.pem ubuntu@<public-ipv4>
```

To simplify access, edit your SSH config file:

```bash
nano ~/.ssh/config
```

Add this block:

```
Host mlops-zoomcamp
    HostName <your-ec2-public-ip>
    User ubuntu
    IdentityFile ~/.ssh/your-key.pem
```

Now you can connect easily:

```bash
ssh mlops-zoomcamp
```

---

## ✅ Step 3: Update the System & Install Basic Tools

Once connected:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git curl wget nano -y
```

---

## ✅ Step 4: Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add current user to docker group
sudo usermod -aG docker $USER

# Log out and log back in, or run:
newgrp docker

# Verify
docker run hello-world
```

Optional: Install Docker Compose Plugin

```bash
sudo apt install docker-compose-plugin
```

---

## ✅ Step 5: Install Anaconda (Python 3.9)

```bash
# Download Anaconda installer
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh

# Run the installer
bash Anaconda3-2022.05-Linux-x86_64.sh

# Activate changes
source ~/.bashrc

# Verify installation
which python
python -V
```

---

## ✅ Step 6: Clone the Course Repo

```bash
git clone https://github.com/<your-username>/mlops-zoomcamp2025.git
cd mlops-zoomcamp2025
```

---

## ✅ Step 7: Connect EC2 to VS Code (Remote Development)

1. Install **VS Code** from:  
   👉 https://code.visualstudio.com/

2. Install the VS Code extension:  
   🔌 `Remote - SSH`

3. Press `F1` → Select `Remote-SSH: Connect to Host...` → choose `mlops-zoomcamp`.

4. VS Code will open a remote window connected to your EC2.

5. Open the folder where your project is located (`mlops-zoomcamp2025`).

---

## ✅ Step 8: Setup and Use Jupyter Notebook

1. From the EC2 terminal (inside VS Code), install Jupyter:

```bash
conda install notebook -y
```

2. Create a folder for notebooks:

```bash
mkdir notebooks
cd notebooks
jupyter notebook --no-browser --port=8888
```

3. VS Code will auto-detect and prompt to **forward port 8888**.  
   If not, click on the "Ports" tab and manually forward **port 8888**.

4. Click the forwarded link shown in VS Code → it will open Jupyter in your browser securely.

---

✅ **Done!** You now have a production-like environment on AWS EC2, connected to VS Code, with Docker, Anaconda, and Jupyter — all ready for MLOps Zoomcamp.



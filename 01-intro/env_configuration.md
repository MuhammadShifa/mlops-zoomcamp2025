# 🛠️ MLOps Zoomcamp - Environment Setup (1.2)

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

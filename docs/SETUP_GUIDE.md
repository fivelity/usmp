# Ultimate Sensor Monitor - Setup Guide

This guide provides comprehensive instructions for setting up the Ultimate Sensor Monitor project (Version 2.0.0+) for local development and containerized environments.

## Table of Contents

1.  [Prerequisites (General)](#1-prerequisites-general)
2.  [Project Structure Overview](#2-project-structure-overview)
3.  [Manual Setup (Local Development)](#3-manual-setup-local-development)
  *   [3.1. General Notes for Manual Setup](#31-general-notes-for-manual-setup)
  *   [3.2. Windows (Non-WSL) Setup](#32-windows-non-wsl-setup)
      *   [3.2.1. Prerequisites for Windows](#321-prerequisites-for-windows)
      *   [3.2.2. Installing Node.js and pnpm on Windows](#322-installing-nodejs-and-pnpm-on-windows)
      *   [3.2.3. Installing Python and pip on Windows](#323-installing-python-and-pip-on-windows)
      *   [3.2.4. Installing Git on Windows](#324-installing-git-on-windows)
      *   [3.2.5. Special Considerations for Windows 11 24H2](#325-special-considerations-for-windows-11-24h2)
      *   [3.2.6. Frontend Setup on Windows](#326-frontend-setup-on-windows)
      *   [3.2.7. Backend Setup on Windows](#327-backend-setup-on-windows)
      *   [3.2.8. Running Manually on Windows](#328-running-manually-on-windows)
  *   [3.3. WSL2 (Windows Subsystem for Linux) Setup](#33-wsl2-windows-subsystem-for-linux-setup)
      *   [3.3.1. Prerequisites for WSL2](#331-prerequisites-for-wsl2)
      *   [3.3.2. Installing Node.js and pnpm on WSL2](#332-installing-nodejs-and-pnpm-on-wsl2)
      *   [3.3.3. Installing Python and pip on WSL2](#333-installing-python-and-pip-on-wsl2)
      *   [3.3.4. Installing Git on WSL2](#334-installing-git-on-wsl2)
      *   [3.3.5. Frontend Setup on WSL2](#335-frontend-setup-on-wsl2)
      *   [3.3.6. Backend Setup on WSL2](#336-backend-setup-on-wsl2)
      *   [3.3.7. Running Manually on WSL2](#337-running-manually-on-wsl2)
      *   [3.3.8. Accessing from Windows Host](#338-accessing-from-windows-host)
  *   [3.4. Linux Setup (e.g., Ubuntu, Fedora)](#34-linux-setup-eg-ubuntu-fedora)
      *   [3.4.1. Prerequisites for Linux](#341-prerequisites-for-linux)
      *   [3.4.2. Installing Node.js and pnpm on Linux](#342-installing-nodejs-and-pnpm-on-linux)
      *   [3.4.3. Installing Python and pip on Linux](#343-installing-python-and-pip-on-linux)
      *   [3.4.4. Installing Git on Linux](#344-installing-git-on-linux)
      *   [3.4.5. Frontend Setup on Linux](#345-frontend-setup-on-linux)
      *   [3.4.6. Backend Setup on Linux](#346-backend-setup-on-linux)
      *   [3.4.7. Running Manually on Linux](#347-running-manually-on-linux)
  *   [3.5. macOS Setup](#35-macos-setup)
      *   [3.5.1. Prerequisites for macOS](#351-prerequisites-for-macos)
      *   [3.5.2. Installing Node.js and pnpm on macOS](#352-installing-nodejs-and-pnpm-on-macos)
      *   [3.5.3. Installing Python and pip on macOS](#353-installing-python-and-pip-on-macos)
      *   [3.5.4. Installing Git on macOS](#354-installing-git-on-macos)
      *   [3.5.5. Frontend Setup on macOS](#355-frontend-setup-on-macos)
      *   [3.5.6. Backend Setup on macOS](#356-backend-setup-on-macos)
      *   [3.5.7. Running Manually on macOS](#357-running-manually-on-macos)
4.  [Docker Setup (Containerized Environment)](#4-docker-setup-containerized-environment)
  *   [4.1. Docker Prerequisites](#41-docker-prerequisites)
  *   [4.2. Using Docker Compose](#42-using-docker-compose)
  *   [4.3. Using the Makefile (Convenience)](#43-using-the-makefile-convenience)
5.  [Development Tools & Commands](#5-development-tools--commands)
  *   [5.1. Why pnpm?](#51-why-pnpm)
  *   [5.2. Common Frontend Commands (in `client/`)](#52-common-frontend-commands-in-client)
  *   [5.3. Common Backend Commands (in `server/`)](#53-common-backend-commands-in-server)
6.  [Troubleshooting](#6-troubleshooting)

---

## 1. Prerequisites (General)

Before you begin, ensure you have the following general software concepts understood and, where applicable, software installed. OS-specific installation details are covered in Section 3.

*   **Node.js**: Version 18.x or higher. This is a JavaScript runtime environment.
*   **pnpm**: Version 8.x or higher. This is the recommended package manager for the Svelte frontend, offering speed and efficiency.
*   **Python**: Version 3.9 or higher. This is the programming language for the backend.
*   **pip**: Python package installer (usually comes with Python). Used to install backend dependencies.
*   **Git**: For cloning the repository and version control.
*   **A Code Editor**: Such as VS Code, Sublime Text, or WebStorm, for editing project files.
*   **Terminal/Command Line Access**: Familiarity with using a terminal is essential.

---

## 2. Project Structure Overview

*   `client/`: Contains the Svelte 4 frontend application (SvelteKit).
  *   `package.json`: Defines frontend dependencies and scripts.
  *   `svelte.config.js`: SvelteKit configuration.
  *   `vite.config.ts`: Vite (build tool) configuration.
  *   `src/`: Frontend source code.
  *   `.env.example`: Template for environment variables.
*   `server/`: Contains the Python backend application (FastAPI).
  *   `requirements.txt`: Defines backend Python dependencies.
  *   `app/`: Backend source code.
  *   `start_backend.py`: Script to launch the backend server.
  *   `.env.example`: Template for environment variables.
*   `docs/`: Project documentation, including this guide.
*   `docker-compose.yml`: Defines services for containerized deployment/development.
*   `Dockerfile`: Root Dockerfile for building a combined image (primarily for production).
*   `Makefile`: Provides convenience commands for Docker and other tasks.
*   `pnpm-workspace.yaml`: Defines the pnpm workspace (if used at the root level).

---

## 3. Manual Setup (Local Development)

This section guides you through setting up the frontend and backend to run directly on your local machine without Docker, with specific instructions for various operating systems.

### 3.1. General Notes for Manual Setup

*   **Clone the Repository**: If you haven't already, clone the project repository to your local machine using Git:
  \`\`\`bash
  git clone <repository_url>
  cd <repository_directory>
  \`\`\`
*   **Environment Variables**: Both frontend and backend applications may use `.env` files for configuration. Always copy the `.env.example` to `.env` in both `client/` and `server/` directories and customize as needed.
  *   `client/.env`: Typically for `VITE_API_BASE_URL` or similar.
  *   `server/.env`: For database connections, API keys, etc.
*   **Virtual Environments for Python**: It is highly recommended to use virtual environments for Python projects to manage dependencies and avoid conflicts.

### 3.2. Windows (Non-WSL) Setup

This section focuses on setting up the project on Windows directly, without using WSL.

#### 3.2.1. Prerequisites for Windows

*   **Administrator Privileges**: May be required for some installations.
*   **Windows Terminal or PowerShell**: Recommended for a better command-line experience. Command Prompt (cmd.exe) also works.
*   **System Architecture**: Ensure you download 64-bit installers if you have a 64-bit OS.

#### 3.2.2. Installing Node.js and pnpm on Windows

1.  **Install Node.js:**
  *   Go to the official Node.js website: [nodejs.org](https://nodejs.org/).
  *   Download the LTS (Long Term Support) version installer for Windows (`.msi`).
  *   Run the installer and follow the prompts. Ensure "Add to PATH" is selected.
  *   Verify installation by opening a new terminal and typing:
      \`\`\`cmd
      node -v
      npm -v
      \`\`\`

2.  **Install pnpm:**
  *   Open a new terminal (PowerShell or Command Prompt as Administrator is recommended for global installs).
  *   Install pnpm globally using npm:
      \`\`\`cmd
      npm install -g pnpm
      \`\`\`
  *   Verify installation:
      \`\`\`cmd
      pnpm -v
      \`\`\`
  *   If `pnpm` command is not found, you might need to restart your terminal or your PC, or ensure the npm global path is in your system's PATH environment variable. (Typically `C:\Users\<YourUser>\AppData\Roaming\npm`)

#### 3.2.3. Installing Python and pip on Windows

1.  **Install Python:**
  *   Go to the official Python website: [python.org](https://www.python.org/downloads/windows/).
  *   Download the latest stable Python 3.9+ installer for Windows.
  *   Run the installer. **Crucially, check the box that says "Add Python X.Y to PATH"** at the beginning of the installation.
  *   Choose "Customize installation" if you want to change the install location, but default settings are usually fine.
  *   Verify installation by opening a new terminal:
      \`\`\`cmd
      python --version
      pip --version
      \`\`\`
      (Sometimes `py --version` is used if multiple Python versions are present).

#### 3.2.4. Installing Git on Windows

1.  **Install Git:**
  *   Go to the official Git website: [git-scm.com/download/win](https://git-scm.com/download/win).
  *   Download the Git for Windows installer.
  *   Run the installer. Default options are generally fine. Ensure "Git Bash Here", "Git GUI Here" are selected if you want those context menu options, and that Git can be used from the command prompt.
  *   Verify installation by opening a new terminal:
      \`\`\`cmd
      git --version
      \`\`\`

#### 3.2.5. Special Considerations for Windows 11 24H2

Windows 11 Version 24H2 introduces some built-in tools that might be familiar to Linux/macOS users:
*   **`sudo` command**: While available, it's generally not required for the typical development setup steps outlined here, as Node.js/Python installers handle permissions or prompt when needed. `npm install -g` might benefit from an admin terminal.
*   **`tar` and `curl`**: These are now built-in. While pnpm can be installed via `curl` on other OSes, the `npm install -g pnpm` method is standard and cross-platform for npm users. These tools might be useful for other development tasks.

The core setup process for Node.js, pnpm, Python, and Git remains the same as for other Windows versions.

#### 3.2.6. Frontend Setup on Windows

1.  **Navigate to the client directory:**
  Open your terminal (Windows Terminal, PowerShell, or cmd).
  \`\`\`cmd
  cd path\to\your\project\client
  \`\`\`

2.  **Install frontend dependencies using pnpm:**
  \`\`\`cmd
  pnpm install
  \`\`\`
  *If you previously used `npm` or `yarn` and have a `node_modules` folder or lock files from them, remove them first: `rd /s /q node_modules` and delete `package-lock.json` or `yarn.lock`.*

3.  **Configure Environment Variables:**
  *   Copy the example environment file:
      \`\`\`cmd
      copy .env.example .env
      \`\`\`
  *   Open `client\.env` in a text editor and modify variables like `VITE_API_BASE_URL` if the backend will run on a non-default URL/port. For local development, it's often `http://localhost:8000/api`.

#### 3.2.7. Backend Setup on Windows

1.  **Navigate to the server directory:**
  \`\`\`cmd
  cd path\to\your\project\server
  \`\`\`

2.  **Create and activate a Python virtual environment:**
  \`\`\`cmd
  python -m venv .venv
  .\.venv\Scripts\activate
  \`\`\`
  Your terminal prompt should now be prefixed with `(.venv)`.

3.  **Install backend dependencies:**
  \`\`\`cmd
  pip install -r requirements.txt
  \`\`\`

4.  **Configure Environment Variables:**
  *   Copy the example environment file:
      \`\`\`cmd
      copy .env.example .env
      \`\`\`
  *   Open `server\.env` in a text editor and modify as needed (e.g., database credentials, API keys).

#### 3.2.8. Running Manually on Windows

You'll typically need two separate terminal windows: one for the frontend and one for the backend.

*   **To run the frontend (SvelteKit dev server):**
  1.  Open a terminal.
  2.  Navigate to the client directory: `cd path\to\your\project\client`
  3.  Start the dev server:
      \`\`\`cmd
      pnpm dev
      \`\`\`
  4.  The application will usually be available at `http://localhost:5173` (or another port if 5173 is busy).

*   **To run the backend (FastAPI server):**
  1.  Open another terminal.
  2.  Navigate to the server directory: `cd path\to\your\project\server`
  3.  Activate the virtual environment:
      \`\`\`cmd
      .\.venv\Scripts\activate
      \`\`\`
  4.  Start the backend server (using the provided script or uvicorn directly):
      Using the project script:
      \`\`\`cmd
      python start_backend.py
      \`\`\`
      Or, if `start_backend.py` runs uvicorn, you might run uvicorn directly (check the script's content):
      \`\`\`cmd
      uvicorn app.main:app --reload --port 8000
      \`\`\`
  5.  The API will usually be available at `http://localhost:8000`.

### 3.3. WSL2 (Windows Subsystem for Linux) Setup

WSL2 allows you to run a Linux environment directly on Windows. Setup within WSL2 is similar to a native Linux setup.

#### 3.3.1. Prerequisites for WSL2

*   **WSL2 Enabled**: Ensure WSL2 is installed and enabled on your Windows machine. See [Microsoft's WSL Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install).
*   **Linux Distribution**: Install a Linux distribution (e.g., Ubuntu) from the Microsoft Store.
*   **Windows Terminal**: Recommended for easy access to your WSL2 distributions.

#### 3.3.2. Installing Node.js and pnpm on WSL2

Open your WSL2 terminal (e.g., Ubuntu).

1.  **Install Node.js (using nvm - Node Version Manager, recommended):**
  \`\`\`bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  # Add nvm to your shell's rc file (e.g., .bashrc, .zshrc)
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
  [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
  # Reload shell configuration
  source ~/.bashrc  # Or source ~/.zshrc, etc.
  nvm install --lts
  nvm use --lts
  node -v
  npm -v
  \`\`\`

2.  **Install pnpm:**
  \`\`\`bash
  npm install -g pnpm
  pnpm -v
  \`\`\`
  Alternatively, using standalone script:
  \`\`\`bash
  curl -fsSL https://get.pnpm.io/install.sh | sh
  # You might need to add pnpm to PATH, the script usually provides instructions.
  # e.g., export PNPM_HOME="/home/youruser/.local/share/pnpm"
  # export PATH="$PNPM_HOME:$PATH"
  # source ~/.bashrc
  \`\`\`

#### 3.3.3. Installing Python and pip on WSL2

1.  **Install Python:**
  Most Linux distributions come with Python 3. If not, or if you need a specific version:
  (Example for Ubuntu)
  \`\`\`bash
  sudo apt update
  sudo apt install python3 python3-pip python3-venv -y
  python3 --version
  pip3 --version
  \`\`\`

#### 3.3.4. Installing Git on WSL2

Git is usually pre-installed. If not:
(Example for Ubuntu)
\`\`\`bash
sudo apt update
sudo apt install git -y
git --version
\`\`\`

#### 3.3.5. Frontend Setup on WSL2

1.  **Navigate to the client directory (within WSL2 filesystem):**
  Your project files should ideally be within the WSL2 filesystem for better performance (e.g., `/home/youruser/projects/your_project/client`).
  \`\`\`bash
  cd /path/to/your/project/client
  \`\`\`

2.  **Install frontend dependencies:**
  \`\`\`bash
  pnpm install
  \`\`\`

3.  **Configure Environment Variables:**
  \`\`\`bash
  cp .env.example .env
  nano .env # Or use your preferred editor (e.g., code .env if VS Code remote WSL is set up)
  \`\`\`
  Update `VITE_API_BASE_URL` if needed. It will still be `http://localhost:8000/api` as WSL2 shares the network namespace.

#### 3.3.6. Backend Setup on WSL2

1.  **Navigate to the server directory:**
  \`\`\`bash
  cd /path/to/your/project/server
  \`\`\`

2.  **Create and activate Python virtual environment:**
  \`\`\`bash
  python3 -m venv .venv
  source .venv/bin/activate
  \`\`\`

3.  **Install backend dependencies:**
  \`\`\`bash
  pip install -r requirements.txt
  \`\`\`

4.  **Configure Environment Variables:**
  \`\`\`bash
  cp .env.example .env
  nano .env
  \`\`\`

#### 3.3.7. Running Manually on WSL2

*   **To run the frontend:**
  In a WSL2 terminal:
  \`\`\`bash
  cd /path/to/your/project/client
  pnpm dev
  \`\`\`

*   **To run the backend:**
  In another WSL2 terminal:
  \`\`\`bash
  cd /path/to/your/project/server
  source .venv/bin/activate
  python start_backend.py
  # Or: uvicorn app.main:app --reload --port 8000
  \`\`\`

#### 3.3.8. Accessing from Windows Host

Applications running inside WSL2 are accessible from your Windows host machine using `localhost`.
*   Frontend: `http://localhost:5173` (or the port shown by `pnpm dev`)
*   Backend API: `http://localhost:8000`

### 3.4. Linux Setup (e.g., Ubuntu, Fedora)

This section covers setup on a native Linux distribution.

#### 3.4.1. Prerequisites for Linux

*   **Terminal Access**: Standard.
*   **Package Manager**: `apt` (Debian/Ubuntu), `dnf` (Fedora), `pacman` (Arch), etc.
*   **Build Tools**: You might need `build-essential` (Debian/Ubuntu) or equivalent for compiling some npm packages.
  \`\`\`bash
  # For Debian/Ubuntu
  sudo apt install build-essential
  # For Fedora
  sudo dnf groupinstall "Development Tools"
  \`\`\`

#### 3.4.2. Installing Node.js and pnpm on Linux

Follow the same instructions as for WSL2 (Section 3.3.2), using `nvm` for Node.js installation is highly recommended.

1.  **Install Node.js (using nvm):**
  \`\`\`bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  # Add nvm to your shell's rc file (e.g., .bashrc, .zshrc)
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
  [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
  source ~/.bashrc # Or ~/.zshrc
  nvm install --lts
  nvm use --lts
  \`\`\`

2.  **Install pnpm:**
  \`\`\`bash
  npm install -g pnpm
  # Or: curl -fsSL https://get.pnpm.io/install.sh | sh
  \`\`\`

#### 3.4.3. Installing Python and pip on Linux

Follow the same instructions as for WSL2 (Section 3.3.3). Python 3, pip, and venv are typically installed via your distribution's package manager.

\`\`\`bash
# For Debian/Ubuntu
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
# For Fedora
sudo dnf install python3 python3-pip python3-virtualenv -y
\`\`\`

#### 3.4.4. Installing Git on Linux

Follow the same instructions as for WSL2 (Section 3.3.4). Git is typically installed via your distribution's package manager.

\`\`\`bash
# For Debian/Ubuntu
sudo apt install git -y
# For Fedora
sudo dnf install git -y
\`\`\`

#### 3.4.5. Frontend Setup on Linux

Identical to WSL2 Frontend Setup (Section 3.3.5).
1.  Navigate to `client/` directory.
2.  Run `pnpm install`.
3.  Copy and configure `client/.env`.

#### 3.4.6. Backend Setup on Linux

Identical to WSL2 Backend Setup (Section 3.3.6).
1.  Navigate to `server/` directory.
2.  Create and activate virtual environment (`python3 -m venv .venv`, `source .venv/bin/activate`).
3.  Run `pip install -r requirements.txt`.
4.  Copy and configure `server/.env`.

#### 3.4.7. Running Manually on Linux

Identical to WSL2 Running Manually (Section 3.3.7).
*   Frontend: `cd client && pnpm dev`
*   Backend: `cd server && source .venv/bin/activate && python start_backend.py` (or `uvicorn ...`)

### 3.5. macOS Setup

#### 3.5.1. Prerequisites for macOS

*   **Terminal Access**: (Terminal.app or iTerm2).
*   **Homebrew**: The missing package manager for macOS. Highly recommended.
  If not installed, run:
  \`\`\`bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  \`\`\`
  Ensure Homebrew is in your PATH. The installer usually provides instructions.
*   **Xcode Command Line Tools**: May be required for Git and other build tools.
  \`\`\`bash
  xcode-select --install
  \`\`\`

#### 3.5.2. Installing Node.js and pnpm on macOS

1.  **Install Node.js:**
  *   **Using Homebrew (recommended):**
      \`\`\`bash
      brew install node
      \`\`\`
  *   **Or using nvm (for version flexibility, also good):**
      Follow nvm installation steps from Linux/WSL2 section (3.3.2 or 3.4.2). Remember to add nvm to your shell config (`~/.zshrc` for modern macOS, or `~/.bash_profile`).
      \`\`\`bash
      curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
      # Add to shell config and source it
      nvm install --lts
      nvm use --lts
      \`\`\`
  Verify: `node -v`, `npm -v`.

2.  **Install pnpm:**
  *   **Using Homebrew:**
      \`\`\`bash
      brew install pnpm
      \`\`\`
  *   **Or using npm:**
      \`\`\`bash
      npm install -g pnpm
      \`\`\`
  *   **Or using standalone script:**
      \`\`\`bash
      curl -fsSL https://get.pnpm.io/install.sh | sh
      \`\`\`
  Verify: `pnpm -v`.

#### 3.5.3. Installing Python and pip on macOS

macOS comes with a system Python, but it's best to install your own version.

1.  **Install Python (using Homebrew):**
  \`\`\`bash
  brew install python3
  \`\`\`
  This will install the latest Python 3 and pip. `python3` and `pip3` commands will point to the Homebrew version.
  Verify: `python3 --version`, `pip3 --version`.

#### 3.5.4. Installing Git on macOS

Git comes with Xcode Command Line Tools. If you installed them, Git should be available.
Alternatively, install/update via Homebrew:
\`\`\`bash
brew install git
\`\`\`
Verify: `git --version`.

#### 3.5.5. Frontend Setup on macOS

Identical to Linux/WSL2 Frontend Setup (Section 3.3.5 or 3.4.5).
1.  Navigate to `client/` directory.
2.  Run `pnpm install`.
3.  Copy and configure `client/.env`.

#### 3.5.6. Backend Setup on macOS

Identical to Linux/WSL2 Backend Setup (Section 3.3.6 or 3.4.6).
1.  Navigate to `server/` directory.
2.  Create and activate virtual environment (`python3 -m venv .venv`, `source .venv/bin/activate`).
3.  Run `pip install -r requirements.txt` (use `pip3` if `pip` points to an older Python).
4.  Copy and configure `server/.env`.

#### 3.5.7. Running Manually on macOS

Identical to Linux/WSL2 Running Manually (Section 3.3.7 or 3.4.7).
*   Frontend: `cd client && pnpm dev`
*   Backend: `cd server && source .venv/bin/activate && python start_backend.py` (or `uvicorn ...`, using `python3` if needed)

---

## 4. Docker Setup (Containerized Environment)

This section describes how to use Docker and Docker Compose to run the application in containers. This is often preferred for consistency across environments and simplified deployment.

### 4.1. Docker Prerequisites

*   **Docker Desktop**: Install Docker Desktop for your OS (Windows, macOS, Linux).
  *   [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) (uses WSL2 backend by default on Windows 10/11 Home/Pro).
  *   [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/).
  *   [Docker Engine for Linux](https://docs.docker.com/engine/install/) (and Docker Compose plugin).
*   Ensure Docker daemon is running.

### 4.2. Using Docker Compose

The `docker-compose.yml` file at the root of the project defines the services (frontend, backend, potentially a database).

1.  **Navigate to the project root directory:**
  \`\`\`bash
  cd /path/to/your/project
  \`\`\`

2.  **Build and run the services:**
  \`\`\`bash
  docker-compose up --build
  \`\`\`
  *   `--build`: Forces Docker to rebuild images if Dockerfiles or their contexts have changed.
  *   `-d`: (Optional) To run in detached mode (in the background).
      \`\`\`bash
      docker-compose up --build -d
      \`\`\`

3.  **Accessing the application:**
  *   Frontend: Usually `http://localhost:5173` (or as configured in `docker-compose.yml`).
  *   Backend API: Usually `http://localhost:8000` (or as configured).

4.  **Stopping the services:**
  *   If running in the foreground, press `Ctrl+C`.
  *   If running in detached mode, or to stop and remove containers:
      \`\`\`bash
      docker-compose down
      \`\`\`

5.  **Environment Variables with Docker:**
  Docker Compose can use `.env` files at the project root or specified per service in `docker-compose.yml`. Check the `docker-compose.yml` for how environment variables are passed to containers (e.g., `env_file` directive or `environment` block). You might need to create `.env` files in `client/` and `server/` which are then copied into the Docker images during build, or mounted as volumes.

### 4.3. Using the Makefile (Convenience)

The `Makefile` provides shorthand commands for common Docker operations.

*   **Build and start services:**
  \`\`\`bash
  make up
  # or make build && make up
  \`\`\`
*   **Stop services:**
  \`\`\`bash
  make down
  \`\`\`
*   **View logs:**
  \`\`\`bash
  make logs
  # For specific service: make logs service=client
  \`\`\`
*   **Rebuild images:**
  \`\`\`bash
  make build
  \`\`\`
*   Explore other commands in the `Makefile`.

---

## 5. Development Tools & Commands

### 5.1. Why pnpm?

`pnpm` is used for the frontend for several reasons:
*   **Efficiency**: Creates a non-flat `node_modules` directory, which is more efficient and closer to Node.js's resolution algorithm.
*   **Disk Space**: Uses a content-addressable store to share packages across projects, saving disk space.
*   **Speed**: Often faster than npm and Yarn for installations.
*   **Strictness**: Helps avoid issues with phantom dependencies.

### 5.2. Common Frontend Commands (in `client/`)

(Run these from the `client/` directory)

*   `pnpm install`: Install dependencies.
*   `pnpm dev`: Start the development server with HMR (Hot Module Replacement).
*   `pnpm build`: Build the application for production.
*   `pnpm preview`: Preview the production build locally.
*   `pnpm check`: Run Svelte check (type checking).
*   `pnpm lint`: Run linters.
*   `pnpm format`: Format code.

### 5.3. Common Backend Commands (in `server/`)

(Run these from the `server/` directory, with virtual environment activated)

*   `pip install -r requirements.txt`: Install/update Python dependencies.
*   `pip freeze > requirements.txt`: Update `requirements.txt` after adding new packages.
*   `python start_backend.py`: Start the FastAPI development server (or the specific command used by this script).
*   `uvicorn app.main:app --reload --port 8000`: A common way to run FastAPI directly.
*   Linters/formatters (e.g., `flake8`, `black`, `isort`) if configured.

---

## 6. Troubleshooting

This section will be populated with common setup issues and their solutions.

*   **Command not found (node, npm, pnpm, python, pip, git):**
  *   **Solution**: Ensure the tool is installed correctly and its installation directory is added to your system's PATH environment variable. Restart your terminal or PC after installation or PATH modification. On Linux/macOS, ensure your shell configuration file (`.bashrc`, `.zshrc`, etc.) is sourced.

*   **Port already in use:**
  *   **Solution**: Another application is using the port (e.g., 5173 or 8000). Stop the other application or configure the project to use a different port (e.g., `pnpm dev --port <new_port>` for frontend, or change port in uvicorn command for backend).

*   **Permission denied (especially with global npm/pnpm installs or Docker on Linux):**
  *   **Solution**:
      *   For global npm/pnpm: Run the terminal as Administrator (Windows) or use `sudo` (Linux/macOS), though using `nvm` or configuring npm for local user installs is often a better long-term solution to avoid `sudo`.
      *   For Docker on Linux: Add your user to the `docker` group: `sudo usermod -aG docker $USER` and then log out/log in.

*   **WSL2 Network Issues:**
  *   **Solution**: Ensure your firewall isn't blocking WSL2. Sometimes, `wsl --shutdown` and restarting Docker Desktop (if it uses WSL2 backend) can resolve transient network issues.

*   **Frontend can't connect to backend (CORS errors, network errors):**
  *   **Solution**:
      *   Verify the backend is running and accessible directly (e.g., `curl http://localhost:8000/api/some_endpoint`).
      *   Check `VITE_API_BASE_URL` in `client/.env` is correct.
      *   Ensure the backend has CORS configured correctly to allow requests from the frontend's origin (e.g., `http://localhost:5173`).

*   **Python virtual environment issues:**
  *   **Solution**: Ensure the virtual environment is activated in your current terminal session. The prompt should usually indicate this (e.g., `(.venv)`). If dependencies are not found, try reactivating or reinstalling them within the active venv.

*   **Issues with `LibreHardwareMonitorLib.dll` or `HWiNFO` (if applicable to this project):**
  *   **Windows Specific**: These typically require running on Windows. The backend might have specific logic for these. Ensure any required DLLs are correctly placed or registered if needed. The backend might need to run with appropriate permissions to access hardware information.
  *   **Mock Data**: For development on non-Windows systems or if hardware monitoring is not the focus, the backend might have a mock sensor mode. Check `server/.env` or configuration options.

(More specific troubleshooting tips can be added as common issues are identified for this project.)

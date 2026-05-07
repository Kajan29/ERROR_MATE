# ErrorMate

ErrorMate is a global Python CLI tool that runs developer commands, detects terminal errors, and explains them in plain English using free AI.

No API key needed. Works with any project.

## Why ErrorMate

- Install once, use in any project.
- Works with PowerShell and Bash.
- Captures stdout and stderr in real time.
- Detects compile and runtime errors.
- Auto-detects project framework.
- Shows a focused explanation in a separate terminal window.
- **Free AI-powered explanations** - no API key required.
- Tells you exactly what went wrong and what to do.

## Supported Frameworks

- Node.js
- React
- Express.js
- Next.js
- NestJS
- Django
- FastAPI
- .NET
- Java Spring Boot
- PHP Laravel

## Step 1: Check if Python is Installed

First, check if Python is already on your machine.

**Windows (PowerShell / CMD):**

```powershell
python --version
```

**Linux/macOS:**

```bash
python3 --version
```

If you see something like `Python 3.8.x` or higher, skip to **Step 2**.

If you get an error like `command not found` or `not recognized`, install Python first:

---

### Install Python (if not installed)

**Windows:**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python installer
3. Run the installer
4. **Important: Check the box "Add Python to PATH"** before clicking Install
5. Close and reopen your terminal
6. Verify:

```powershell
python --version
pip --version
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install python3 python3-pip -y
python3 --version
```

**Linux (Fedora/CentOS):**

```bash
sudo dnf upgrade --refresh -y
sudo dnf install python3 python3-pip -y
python3 --version
```

**Linux (Arch Linux):**

```bash
sudo pacman -Syu
sudo pacman -S python python-pip
python3 --version
```

**Linux (openSUSE):**

```bash
sudo zypper refresh
sudo zypper install python3 python3-pip
python3 --version
```

**macOS:**

```bash
brew update
brew install python
python3 --version
```

If you don't have Homebrew, install it first:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

## Step 2: Install ErrorMate

Once Python is ready, install ErrorMate with one command:

**Windows (PowerShell / CMD):**

```powershell
pip install git+https://github.com/Kajan29/ERROR_MATE.git
```

**Linux/macOS:**

```bash
pip3 install git+https://github.com/Kajan29/ERROR_MATE.git
```

That's it! Verify it works:

```bash
errormate --help
```

### Upgrade to Latest Version

**Windows:**

```powershell
pip install --upgrade git+https://github.com/Kajan29/ERROR_MATE.git
```

**Linux/macOS:**

```bash
pip3 install --upgrade git+https://github.com/Kajan29/ERROR_MATE.git
```

### Uninstall

```bash
pip uninstall errormate
```

## Quick Start

Run your normal dev command through ErrorMate:

```bash
errormate run "npm run dev"
errormate run "python manage.py runserver"
errormate run "dotnet run"
errormate run "php artisan serve"
errormate run "mvn spring-boot:run"
```

Detect framework only:

```bash
errormate detect
```

## Common Options

```bash
errormate run "npm run dev" --shell bash
errormate run "dotnet run" --shell powershell
errormate run "npm run dev" --project-path .
errormate run "npm run dev" --no-popup
errormate run "npm run dev" --no-ai
errormate --version
```

- **--no-ai** - Skip AI explanation, use rule-based only
- **--no-popup** - Show errors in same terminal instead of a new window
- **--shell** - Force a specific shell (powershell or bash)
- **--project-path** - Set the project directory
- **--version** - Show version

## Example Output

```text
ERROR DETECTED
--------------------------------------------------

  Error:     Module not found: Can't resolve './components/Header'
  Framework: React
  Type:      Compile Error

--------------------------------------------------
  AI EXPLANATION
--------------------------------------------------

  What went wrong:
  Your code is trying to import a file called "Header" from the
  components folder, but that file does not exist or the path is wrong.

  How to fix it:
  1. Check if the file exists: src/components/Header.js
  2. Make sure the file name matches exactly (case-sensitive)
  3. Run: npm start

--------------------------------------------------
  WHAT THIS MEANS
--------------------------------------------------

  A required module or file could not be found during compilation.

--------------------------------------------------
  HOW TO FIX
--------------------------------------------------

  1. Check the import path for typos.
  2. Run: npm install
  3. Restart the development server.
```

## How It Works

1. ErrorMate runs your command in the selected shell.
2. It streams and captures stdout and stderr in real time.
3. It detects the framework from project files.
4. It applies framework-specific and common regex rules.
5. It asks free AI to explain the error in plain English.
6. It opens a separate terminal window with the full explanation.

## Framework Detection Rules

- package.json -> Node.js
- package.json with react dependency -> React
- package.json with express dependency -> Express.js
- package.json with next dependency -> Next.js
- package.json with @nestjs/core dependency -> NestJS
- manage.py -> Django
- .csproj or .sln -> .NET
- pom.xml or build.gradle -> Java Spring Boot
- artisan and composer.json -> Laravel

## Local Development

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Bash:

```bash
source .venv/bin/activate
```

Install dependencies and run tests:

```bash
pip install -r requirements.txt
pytest
```

## Roadmap

- Add support for more frameworks.
- Improve AI explanation quality with better prompts.
- Add error history tracking.

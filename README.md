# ErrorMate

ErrorMate is a global Python CLI tool that runs developer commands and detects terminal errors using rule-based regex matching.

Version 1 is fully non-AI.

## Why ErrorMate

- Install once, use in any project.
- Works with PowerShell and Bash.
- Captures stdout and stderr in real time.
- Detects compile and runtime errors.
- Auto-detects project framework.
- Shows a focused explanation in a separate terminal window.

## Supported Frameworks

- Node.js
- React
- Express.js
- Next.js
- NestJS
- Django
- .NET
- Java Spring Boot
- PHP Laravel

## Prerequisites

- Python 3.9+
- pip
- Recommended: pipx for clean global CLI installs

## Installation

### Option 1: Install globally from local source (recommended during development)

```bash
pipx install .
```

### Option 2: Install globally from GitHub

Replace USERNAME with your GitHub username after publishing.

```bash
pipx install git+https://github.com/USERNAME/errormate.git
```

### Option 3: Install with pip

```bash
pip install .
```

## Verify Installation

```bash
errormate --help
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
```

## Example Output

```text
Error Detected

Framework: React
Error Type: Compile Error
Main Error: Module not found

Meaning:
A required package or file cannot be found.

Possible Fix:
1. Check the import path.
2. Install the missing package.
3. Restart the development server.
```

## How It Works

1. ErrorMate runs the command in the selected shell.
2. It streams and captures stdout and stderr.
3. It detects the framework from project files.
4. It applies framework-specific and common regex rules.
5. It classifies the error and prints clear next steps.

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

## Publish Notes

If you are publishing to GitHub, keep package metadata updated in pyproject.toml:

- project name
- version
- description
- authors

## Roadmap

- Add optional AI-powered explanations as an opt-in feature in a future version.

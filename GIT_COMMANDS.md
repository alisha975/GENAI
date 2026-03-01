# Git Commands to Push Code to GitHub GENAI Repository

## Step 1: Initialize Git and Add Remote (if not already done)
cd "C:\Users\2211541\OneDrive - Cognizant\Desktop\Fullstack_project"

# Initialize git repository (if not already initialized)
git init

# Add your GitHub repository as remote
git remote add origin https://github.com/alisha975/GENAI.git

# Verify remote is added
git remote -v

---

## Step 2: Create and Switch to New Branch
# Create a new branch with a descriptive name (replace 'feature-langgraph-azure' with your branch name)
git checkout -b feature-langgraph-azure

# Or use the newer syntax:
git switch -c feature-langgraph-azure

---

## Step 3: Add All Files to Staging
git add .

# Verify files are staged
git status

---

## Step 4: Commit Your Changes
git commit -m "Add fullstack LangGraph project with Azure OpenAI integration, Jenkinsfile, and unit tests

- Migrated from Google Gemini to Azure OpenAI
- Added comprehensive Jenkinsfile for CI/CD pipeline
- Added Docker and docker-compose configuration
- Frontend React/Vite with TypeScript
- Backend Python with LangGraph agent
- Added unit tests for Jenkinsfile
- Added environment configuration management"

---

## Step 5: Push to GitHub
# Push your new branch to GitHub
git push -u origin feature-langgraph-azure

# Or if you want to push to main branch:
git push -u origin main

---

## Additional Useful Commands

# Check current branch
git branch

# See commit history
git log --oneline

# Check what will be pushed
git diff origin/main

# Pull latest changes from remote
git pull origin main

# Create a Pull Request (PR) on GitHub after pushing
# Go to: https://github.com/alisha975/GENAI
# Click "New Pull Request" and compare your branch with main

---

## Complete Workflow (All at once)

cd "C:\Users\2211541\OneDrive - Cognizant\Desktop\Fullstack_project"
git init
git remote add origin https://github.com/alisha975/GENAI.git
git checkout -b feature-langgraph-azure
git add .
git commit -m "Add fullstack LangGraph project with Azure OpenAI integration"
git push -u origin feature-langgraph-azure

---

## If Repository Already Has Content

# Clone the existing repository first
git clone https://github.com/alisha975/GENAI.git
cd GENAI

# Create new branch
git checkout -b feature-langgraph-azure

# Copy your files into this directory
# Then add, commit, and push

git add .
git commit -m "Add fullstack LangGraph project with Azure OpenAI integration"
git push -u origin feature-langgraph-azure

---

## To Make a Pull Request (on GitHub.com)

1. Go to: https://github.com/alisha975/GENAI
2. Click "Pull requests" tab
3. Click "New pull request"
4. Base: main, Compare: feature-langgraph-azure
5. Add title and description
6. Click "Create pull request"

---

## Notes:

- Replace "feature-langgraph-azure" with your preferred branch name
- You may be prompted for authentication when pushing (use Personal Access Token or SSH key)
- Make sure you have write access to the repository
- If the repository doesn't exist yet, create it on GitHub first


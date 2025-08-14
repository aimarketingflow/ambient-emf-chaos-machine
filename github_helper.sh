#!/bin/bash

# EMF Chaos Engine - GitHub Helper Script
# 6-Option Management Tool for Repository Operations
# AIMF LLC - August 2025

echo "🔥⚡ EMF CHAOS ENGINE - GITHUB HELPER ⚡🔥"
echo "================================================"
echo ""
echo "Choose an option:"
echo ""
echo "1. 📤 PUSH TO GITHUB (Add, Commit, Push)"
echo "2. 📥 PULL FROM GITHUB (Fetch latest changes)"
echo "3. 📊 STATUS CHECK (Git status + branch info)"
echo "4. 🌿 BRANCH MANAGEMENT (Create/switch branches)"
echo "5. 📋 COMMIT HISTORY (View recent commits)"
echo "6. 🔧 REPOSITORY SETUP (Initialize/configure repo)"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "🚀 PUSHING TO GITHUB..."
        echo "======================="
        
        # Check if we're in a git repository
        if [ ! -d ".git" ]; then
            echo "❌ Not a git repository. Run option 6 first to set up."
            exit 1
        fi
        
        # Show current status
        echo "📊 Current status:"
        git status --short
        echo ""
        
        # Add all changes
        echo "📤 Adding all changes..."
        git add .
        
        # Get commit message
        echo ""
        read -p "💬 Enter commit message (or press Enter for auto-message): " commit_msg
        
        if [ -z "$commit_msg" ]; then
            # Auto-generate commit message with timestamp
            commit_msg="EMF Chaos Engine update - $(date '+%Y-%m-%d %H:%M:%S')"
        fi
        
        # Commit changes
        echo "💾 Committing changes..."
        git commit -m "$commit_msg"
        
        # Push to remote
        echo "🚀 Pushing to GitHub..."
        git push origin main
        
        echo ""
        echo "✅ Successfully pushed to GitHub!"
        echo "🔗 Repository: https://github.com/your-username/emf-chaos-engine"
        ;;
        
    2)
        echo ""
        echo "📥 PULLING FROM GITHUB..."
        echo "========================"
        
        if [ ! -d ".git" ]; then
            echo "❌ Not a git repository. Run option 6 first to set up."
            exit 1
        fi
        
        echo "🔄 Fetching latest changes..."
        git fetch origin
        
        echo "📥 Pulling changes..."
        git pull origin main
        
        echo "✅ Repository updated!"
        ;;
        
    3)
        echo ""
        echo "📊 REPOSITORY STATUS..."
        echo "======================"
        
        if [ ! -d ".git" ]; then
            echo "❌ Not a git repository. Run option 6 first to set up."
            exit 1
        fi
        
        echo "🌿 Current branch:"
        git branch --show-current
        echo ""
        
        echo "📊 Repository status:"
        git status
        echo ""
        
        echo "🔗 Remote repositories:"
        git remote -v
        echo ""
        
        echo "📈 Recent activity:"
        git log --oneline -5
        ;;
        
    4)
        echo ""
        echo "🌿 BRANCH MANAGEMENT..."
        echo "======================"
        
        if [ ! -d ".git" ]; then
            echo "❌ Not a git repository. Run option 6 first to set up."
            exit 1
        fi
        
        echo "Current branches:"
        git branch -a
        echo ""
        
        echo "Choose branch action:"
        echo "1. Create new branch"
        echo "2. Switch to existing branch"
        echo "3. Delete branch"
        echo ""
        read -p "Enter choice (1-3): " branch_choice
        
        case $branch_choice in
            1)
                read -p "🌿 Enter new branch name: " branch_name
                git checkout -b "$branch_name"
                echo "✅ Created and switched to branch: $branch_name"
                ;;
            2)
                read -p "🔄 Enter branch name to switch to: " branch_name
                git checkout "$branch_name"
                echo "✅ Switched to branch: $branch_name"
                ;;
            3)
                read -p "🗑️ Enter branch name to delete: " branch_name
                git branch -d "$branch_name"
                echo "✅ Deleted branch: $branch_name"
                ;;
        esac
        ;;
        
    5)
        echo ""
        echo "📋 COMMIT HISTORY..."
        echo "==================="
        
        if [ ! -d ".git" ]; then
            echo "❌ Not a git repository. Run option 6 first to set up."
            exit 1
        fi
        
        echo "📈 Recent commits (last 10):"
        git log --oneline --graph --decorate -10
        echo ""
        
        echo "📊 Commit statistics:"
        echo "Total commits: $(git rev-list --count HEAD)"
        echo "Contributors: $(git shortlog -sn | wc -l)"
        echo ""
        
        echo "🔥 Latest commit details:"
        git show --stat HEAD
        ;;
        
    6)
        echo ""
        echo "🔧 REPOSITORY SETUP..."
        echo "====================="
        
        if [ -d ".git" ]; then
            echo "✅ Git repository already exists!"
            echo ""
            echo "Current configuration:"
            git config --list | grep -E "(user\.|remote\.)"
            echo ""
            read -p "🔄 Reconfigure repository? (y/n): " reconfig
            if [ "$reconfig" != "y" ]; then
                exit 0
            fi
        fi
        
        # Initialize git if not already done
        if [ ! -d ".git" ]; then
            echo "🎯 Initializing git repository..."
            git init
        fi
        
        # Set up user configuration
        echo ""
        echo "👤 Git User Configuration:"
        read -p "Enter your name: " git_name
        read -p "Enter your email: " git_email
        
        git config user.name "$git_name"
        git config user.email "$git_email"
        
        # Set up remote repository
        echo ""
        echo "🔗 Remote Repository Setup:"
        read -p "Enter GitHub repository URL (https://github.com/username/repo.git): " repo_url
        
        if [ ! -z "$repo_url" ]; then
            # Remove existing remote if it exists
            git remote remove origin 2>/dev/null || true
            
            # Add new remote
            git remote add origin "$repo_url"
            echo "✅ Remote repository configured!"
        fi
        
        # Create initial commit if needed
        if [ -z "$(git log --oneline 2>/dev/null)" ]; then
            echo ""
            echo "📝 Creating initial commit..."
            
            # Create .gitignore if it doesn't exist
            if [ ! -f ".gitignore" ]; then
                cat > .gitignore << EOF
# EMF Chaos Engine - Git Ignore File

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
emf_chaos_venv/
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp

# RF Data (keep private)
rf_data/
captures/
*.pcap

# Configuration (keep private)
config/local_*
*.key
*.pem
EOF
                echo "📋 Created .gitignore file"
            fi
            
            # Add all files and create initial commit
            git add .
            git commit -m "🔥 Initial commit - EMF Chaos Engine setup"
            
            # Push to remote if configured
            if [ ! -z "$repo_url" ]; then
                echo "🚀 Pushing initial commit to GitHub..."
                git branch -M main
                git push -u origin main
            fi
        fi
        
        echo ""
        echo "✅ Repository setup complete!"
        echo "🔗 Remote: $(git remote get-url origin 2>/dev/null || echo 'Not configured')"
        echo "🌿 Branch: $(git branch --show-current)"
        ;;
        
    *)
        echo ""
        echo "❌ Invalid option. Please choose 1-6."
        exit 1
        ;;
esac

echo ""
echo "🔥⚡ EMF Chaos Engine GitHub Helper Complete! ⚡🔥"
echo "================================================"

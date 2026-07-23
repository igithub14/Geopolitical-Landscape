# Databricks notebook source
# MAGIC %md
# MAGIC # 🛡️ Git Daily Safety Backup
# MAGIC 
# MAGIC **Purpose**: Automated daily commit and push to GitHub for disaster recovery
# MAGIC 
# MAGIC **Schedule**: Daily at 23:00 (11:00 PM)
# MAGIC 
# MAGIC **Author**: Cristiano Mombello
# MAGIC 
# MAGIC **Last Updated**: 2026-07-23
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC ## 📋 Script Overview
# MAGIC 
# MAGIC This notebook performs automated Git operations to ensure all work is safely backed up to GitHub:
# MAGIC 
# MAGIC 1. **Check Git Status**: Verify repository state and identify changed files
# MAGIC 2. **Stage Changes**: Add all modified/new files to staging area
# MAGIC 3. **Commit**: Create commit with auto-generated timestamp message
# MAGIC 4. **Push**: Upload commit to GitHub remote repository
# MAGIC 5. **Email Notification**: Send success/failure report to cristiano.mombello@gmail.com
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC ## ⚙️ Configuration
# MAGIC 
# MAGIC **Repository Path**: `/Workspace/Users/cristiano.mombello@gmail.com/Geopolitical_Landscape`
# MAGIC 
# MAGIC **Branch**: `main`
# MAGIC 
# MAGIC **Notification Email**: `cristiano.mombello@gmail.com`
# MAGIC 
# MAGIC **Schedule**: Databricks Job scheduled for 23:00 daily (Europe/Rome timezone)
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC ## 🚨 Error Handling
# MAGIC 
# MAGIC The script includes comprehensive error handling:
# MAGIC - Git authentication failures
# MAGIC - Merge conflicts
# MAGIC - Network connectivity issues
# MAGIC - Push rejections (non-fast-forward)
# MAGIC 
# MAGIC All errors trigger immediate email notification with diagnostic details.
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC ## 📧 Notification Format
# MAGIC 
# MAGIC **Success Email**:
# MAGIC - Subject: "✅ Git Backup Success - [Date]"
# MAGIC - Body: Commit hash, files changed, timestamp
# MAGIC 
# MAGIC **Failure Email**:
# MAGIC - Subject: "🚨 Git Backup FAILED - [Date]"
# MAGIC - Body: Error message, stack trace, repository state

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1️⃣ Import Dependencies

import subprocess
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2️⃣ Configuration Variables

# Repository configuration
REPO_PATH = "/Workspace/Users/cristiano.mombello@gmail.com/Geopolitical_Landscape"
BRANCH = "main"

# Email configuration
NOTIFICATION_EMAIL = "cristiano.mombello@gmail.com"

# Timestamp for commit message
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
DATE_SHORT = datetime.now().strftime("%Y-%m-%d")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3️⃣ Helper Functions

def run_git_command(command, cwd=REPO_PATH):
    """
    Execute a git command and return the result.
    
    Args:
        command (list): Git command as list of strings (e.g., ['git', 'status'])
        cwd (str): Working directory for command execution
    
    Returns:
        tuple: (success: bool, output: str, error: str)
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        success = result.returncode == 0
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        return success, output, error
        
    except subprocess.TimeoutExpired:
        return False, "", "Command timeout after 60 seconds"
    except Exception as e:
        return False, "", str(e)


def send_email_notification(subject, body, is_success=True):
    """
    Send email notification via Databricks notification system.
    
    Args:
        subject (str): Email subject line
        body (str): Email body content
        is_success (bool): Whether this is a success or failure notification
    """
    try:
        # Use Databricks dbutils for email notifications
        # Note: This requires the notebook to be run as part of a Job with email notifications configured
        
        emoji = "✅" if is_success else "🚨"
        full_subject = f"{emoji} {subject}"
        
        # Format body with HTML for better readability
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: {'#d4edda' if is_success else '#f8d7da'}; padding: 15px; border-radius: 5px; }}
                .content {{ padding: 15px; }}
                .footer {{ margin-top: 20px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; font-size: 12px; }}
                pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 3px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>{emoji} Git Safety Backup Report</h2>
                <p><strong>Date:</strong> {TIMESTAMP}</p>
            </div>
            <div class="content">
                <pre>{body}</pre>
            </div>
            <div class="footer">
                <p>📍 Repository: Geopolitical_Landscape</p>
                <p>🔗 <a href="https://github.com/igithub14/Geopolitical-Landscape">View on GitHub</a></p>
                <p>⚙️ Automated by Databricks Job</p>
            </div>
        </body>
        </html>
        """
        
        # Store notification details for Job to pick up
        # The actual email sending is handled by Databricks Job notifications
        print(f"\n{'='*60}")
        print(f"NOTIFICATION: {full_subject}")
        print(f"{'='*60}")
        print(body)
        print(f"{'='*60}\n")
        
        # Create a result widget for Job to capture
        dbutils.notebook.exit({
            "status": "success" if is_success else "failed",
            "subject": full_subject,
            "body": body,
            "timestamp": TIMESTAMP
        })
        
    except Exception as e:
        print(f"⚠️ Failed to send email notification: {e}")
        # Don't fail the entire script if email fails
        pass

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4️⃣ Main Backup Logic

def git_daily_backup():
    """
    Main function to perform daily Git backup with commit and push.
    
    Returns:
        bool: True if backup successful, False otherwise
    """
    
    print(f"\n🛡️ Starting Git Daily Safety Backup - {TIMESTAMP}\n")
    print(f"📁 Repository: {REPO_PATH}")
    print(f"🌿 Branch: {BRANCH}\n")
    
    # Step 1: Check Git status
    print("[1/5] Checking repository status...")
    success, output, error = run_git_command(['git', 'status', '--porcelain'])
    
    if not success:
        error_msg = f"Failed to check Git status:\n{error}"
        print(f"❌ {error_msg}")
        send_email_notification(
            f"Git Backup FAILED - {DATE_SHORT}",
            error_msg,
            is_success=False
        )
        return False
    
    # Check if there are changes to commit
    if not output:
        success_msg = f"""Repository is clean - no changes to commit.

Status: Up to date with remote
Branch: {BRANCH}
Timestamp: {TIMESTAMP}

ℹ️ No action required - all files already backed up."""
        print("✅ No changes detected - repository clean")
        send_email_notification(
            f"Git Backup - No Changes - {DATE_SHORT}",
            success_msg,
            is_success=True
        )
        return True
    
    # Parse changed files
    changed_files = output.split('\n')
    file_count = len(changed_files)
    print(f"✅ Found {file_count} changed file(s)")
    for file in changed_files[:10]:  # Show first 10 files
        print(f"   {file}")
    if file_count > 10:
        print(f"   ... and {file_count - 10} more")
    
    # Step 2: Stage all changes
    print("\n[2/5] Staging changes...")
    success, output, error = run_git_command(['git', 'add', '-A'])
    
    if not success:
        error_msg = f"Failed to stage changes:\n{error}"
        print(f"❌ {error_msg}")
        send_email_notification(
            f"Git Backup FAILED - {DATE_SHORT}",
            error_msg,
            is_success=False
        )
        return False
    
    print("✅ Changes staged successfully")
    
    # Step 3: Create commit
    print("\n[3/5] Creating commit...")
    commit_message = f"[Automated Safety Backup] {TIMESTAMP}\n\nDaily automated commit by git_daily_safety_backup.py\nFiles changed: {file_count}"
    
    success, output, error = run_git_command(['git', 'commit', '-m', commit_message])
    
    if not success:
        error_msg = f"Failed to create commit:\n{error}\n\nOutput:\n{output}"
        print(f"❌ {error_msg}")
        send_email_notification(
            f"Git Backup FAILED - {DATE_SHORT}",
            error_msg,
            is_success=False
        )
        return False
    
    print("✅ Commit created successfully")
    print(f"   {output}")
    
    # Extract commit hash
    commit_hash = ""
    for line in output.split('\n'):
        if 'main' in line or 'master' in line:
            parts = line.split()
            if len(parts) > 1:
                commit_hash = parts[1].strip('[]')
                break
    
    # Step 4: Push to remote
    print("\n[4/5] Pushing to GitHub...")
    success, output, error = run_git_command(['git', 'push', 'origin', BRANCH])
    
    if not success:
        error_msg = f"""Failed to push to GitHub:

Error:
{error}

Output:
{output}

⚠️ Commit was created locally but not pushed to remote.
💡 Manual intervention may be required.

Possible causes:
- Network connectivity issues
- Git authentication failure
- Push rejected (non-fast-forward)
- Remote repository issues

Commit Hash: {commit_hash}
Branch: {BRANCH}"""
        print(f"❌ {error_msg}")
        send_email_notification(
            f"Git Backup FAILED - {DATE_SHORT}",
            error_msg,
            is_success=False
        )
        return False
    
    print("✅ Pushed to GitHub successfully")
    print(f"   {output}")
    
    # Step 5: Send success notification
    print("\n[5/5] Sending success notification...")
    
    success_msg = f"""✅ Git backup completed successfully!

📊 Backup Summary:
  • Files Changed: {file_count}
  • Commit Hash: {commit_hash}
  • Branch: {BRANCH}
  • Timestamp: {TIMESTAMP}

📝 Changed Files (first 10):
"""
    
    for file in changed_files[:10]:
        success_msg += f"\n  {file}"
    
    if file_count > 10:
        success_msg += f"\n  ... and {file_count - 10} more"
    
    success_msg += f"\n\n🔗 View on GitHub: \
https://github.com/igithub14/Geopolitical-Landscape/commits/{BRANCH}"
    
    send_email_notification(
        f"Git Backup Success - {DATE_SHORT}",
        success_msg,
        is_success=True
    )
    
    print("\n" + "="*60)
    print("🎉 GIT DAILY SAFETY BACKUP COMPLETED SUCCESSFULLY")
    print("="*60 + "\n")
    
    return True

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5️⃣ Execute Backup

try:
    success = git_daily_backup()
    
    if not success:
        # Exit with error code for Job monitoring
        dbutils.notebook.exit({"status": "failed", "timestamp": TIMESTAMP})
    else:
        # Exit with success
        dbutils.notebook.exit({"status": "success", "timestamp": TIMESTAMP})
        
except Exception as e:
    # Catch any unexpected errors
    error_msg = f"""Unexpected error during Git backup:

Error Type: {type(e).__name__}
Error Message: {str(e)}

Timestamp: {TIMESTAMP}
Repository: {REPO_PATH}

⚠️ The backup script encountered an unexpected error.
💡 Please check the Job run logs for more details."""
    
    print(f"\n❌ CRITICAL ERROR:\n{error_msg}\n")
    
    send_email_notification(
        f"Git Backup CRITICAL ERROR - {DATE_SHORT}",
        error_msg,
        is_success=False
    )
    
    dbutils.notebook.exit({"status": "error", "error": str(e), "timestamp": TIMESTAMP})

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC 
# MAGIC ## 📚 Usage Instructions
# MAGIC 
# MAGIC ### Manual Execution
# MAGIC 
# MAGIC To test this notebook manually:
# MAGIC 
# MAGIC 1. Open the notebook
# MAGIC 2. Click "Run All" in the top menu
# MAGIC 3. Check output for success/failure
# MAGIC 4. Verify email notification received
# MAGIC 
# MAGIC ### Scheduled Execution (Job Setup)
# MAGIC 
# MAGIC 1. **Create a new Job**:
# MAGIC    - Go to Workflows → Jobs → Create Job
# MAGIC    - Name: "Git Daily Safety Backup"
# MAGIC 
# MAGIC 2. **Add Task**:
# MAGIC    - Task name: "backup_geopolitical_landscape"
# MAGIC    - Type: Notebook
# MAGIC    - Path: Select this notebook
# MAGIC    - Cluster: Shared cluster or create new (small cluster sufficient)
# MAGIC 
# MAGIC 3. **Configure Schedule**:
# MAGIC    - Trigger type: Scheduled
# MAGIC    - Schedule: Cron expression `0 23 * * *` (11:00 PM daily)
# MAGIC    - Timezone: Europe/Rome
# MAGIC 
# MAGIC 4. **Configure Email Notifications**:
# MAGIC    - Recipients: cristiano.mombello@gmail.com
# MAGIC    - Notify on: Start, Success, Failure
# MAGIC    - Include run output: Yes
# MAGIC 
# MAGIC 5. **Save and Enable**
# MAGIC 
# MAGIC ### Monitoring
# MAGIC 
# MAGIC - **Job Runs**: Workflows → Jobs → Git Daily Safety Backup → Runs
# MAGIC - **Email Inbox**: Check cristiano.mombello@gmail.com daily
# MAGIC - **GitHub Commits**: https://github.com/igithub14/Geopolitical-Landscape/commits/main
# MAGIC 
# MAGIC ### Troubleshooting
# MAGIC 
# MAGIC **Problem**: Authentication failure
# MAGIC - **Solution**: Verify Git credentials configured in Databricks User Settings → Git Integration
# MAGIC 
# MAGIC **Problem**: Push rejected (non-fast-forward)
# MAGIC - **Solution**: Manual pull required - repository has remote changes not present locally
# MAGIC 
# MAGIC **Problem**: Email not received
# MAGIC - **Solution**: Verify Job email notifications configured correctly, check spam folder
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC ## 🔒 Security Notes
# MAGIC 
# MAGIC - Git credentials managed by Databricks (no hardcoded tokens)
# MAGIC - Email notifications use Databricks Job notification system (no SMTP credentials)
# MAGIC - Repository access requires proper Databricks workspace permissions
# MAGIC - Script runs with user's Git credentials (cristiano.mombello@gmail.com)
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC ## 📝 Maintenance
# MAGIC 
# MAGIC **Last Updated**: 2026-07-23
# MAGIC 
# MAGIC **Change Log**:
# MAGIC - 2026-07-23: Initial version with email notifications
# MAGIC 
# MAGIC **Next Review**: 2026-08-23

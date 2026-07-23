#  Git Daily Safety Backup - Setup Instructions

**Script**: `git_daily_safety_backup.py`

**Purpose**: Automated daily commit and push to GitHub with email notifications

**Notification Email**: cristiano.mombello@gmail.com

---

##  Quick Setup Checklist

- [ ] Create Databricks Job
- [ ] Configure notebook task
- [ ] Set schedule (23:00 daily)
- [ ] Configure email notifications
- [ ] Test run manually
- [ ] Enable job

---

##  Detailed Setup Steps

### Step 1: Navigate to Workflows

1. Open Databricks workspace
2. Click **"Workflows"** in left sidebar
3. Click **"Jobs"** tab
4. Click **"Create Job"** button (top right)

---

### Step 2: Configure Job Settings

**Job Name**: `Git Daily Safety Backup - Geopolitical Landscape`

**Description**: 
```
Automated daily Git commit and push for disaster recovery.
Commits all changes at 23:00 and sends email notification.
```

---

### Step 3: Add Notebook Task

1. Click **"+ Add task"**

2. **Task Configuration**:
   * **Task name**: `backup_geopolitical_landscape`
   * **Type**: Notebook
   * **Source**: Workspace
   * **Path**: Browse and select:
     ```
     /Users/cristiano.mombello@gmail.com/Geopolitical_Landscape/git_daily_safety_backup.py
     ```

3. **Compute**:
   * **Cluster**: Select existing shared cluster OR
   * **New Job Cluster**:
     - Cluster name: `backup-cluster`
     - Cluster mode: Single node
     - Databricks runtime: Latest LTS version
     - Node type: Smallest available (script is lightweight)
     - Auto termination: 10 minutes

4. Click **"Create"**

---

### Step 4: Configure Schedule

1. In the Job details page, find **"Trigger"** section

2. Click **"Add trigger"**

3. **Schedule Settings**:
   * **Trigger type**: Scheduled
   * **Schedule type**: Cron
   * **Cron expression**: `0 23 * * *`
     - Translation: "At 23:00 (11:00 PM) every day"
   * **Timezone**: `Europe/Rome`
   * **Pause status**: UNPAUSED (active)

4. Click **"Save"**

---

### Step 5: Configure Email Notifications

1. In Job details page, scroll to **"Notifications"** section

2. Click **"Edit"**

3. **Email Recipients**:
   * Add: `cristiano.mombello@gmail.com`

4. **Notification Triggers** (select ALL):
   * ✅ On Start
   * ✅ On Success
   * ✅ On Failure
   * ✅ No Retries (skip retries for backup script)

5. **Additional Settings**:
   * ✅ Include run output in notification
   * ✅ Send empty success notifications

6. Click **"Save"**

---

### Step 6: Configure Git Credentials (if not already done)

1. Click your profile icon (top right)

2. Select **"User Settings"**

3. Navigate to **"Git Integration"** tab

4. Add GitHub credentials:
   * **Git provider**: GitHub
   * **Username**: `igithub14`
   * **Token**: Generate a Personal Access Token from GitHub:
     - Go to GitHub → Settings → Developer Settings → Personal Access Tokens
     - Generate new token (classic)
     - Scopes: `repo` (full control of private repositories)
     - Copy token and paste in Databricks

5. Click **"Save"**

---

### Step 7: Test Run (Manual)

1. In Job details page, click **"Run now"** button (top right)

2. Monitor the run:
   * Click on the run in "Job runs" section
   * Watch notebook execution in real-time
   * Check for success/failure

3. **Verify Success**:
   * ✅ Run status shows "Succeeded"
   * ✅ Check email inbox for notification
   * ✅ Verify new commit on GitHub:
     - https://github.com/igithub14/Geopolitical-Landscape/commits/main
   * ✅ Commit message contains "[Automated Safety Backup]"

4. **If Failure**:
   * Check run logs for error details
   * Common issues:
     - Git credentials not configured
     - Network connectivity
     - Repository permissions
   * Email notification will contain error details

---

### Step 8: Enable Scheduled Job

1. Verify test run succeeded

2. In Job details page, find **"Trigger"** section

3. Ensure toggle is **ON** (blue)
   * If OFF (gray), click toggle to enable

4. Verify next run time is displayed:
   * "Next run: Today at 23:00" (or tomorrow if after 23:00)

---

## ✅ Verification Checklist

After setup, verify the following:

- [ ] Job appears in Workflows → Jobs list
- [ ] Job status is "Active" (not paused)
- [ ] Schedule shows "Next run: [timestamp]"
- [ ] Email notifications configured for all triggers
- [ ] Test run completed successfully
- [ ] Email notification received from test run
- [ ] New commit visible on GitHub
- [ ] Commit message contains "[Automated Safety Backup]"

---

## 📧 Expected Email Notifications

### Success Email (Daily at ~23:01)

**Subject**: ✅ Git Backup Success - [Date]

**Body**:
```
✅ Git backup completed successfully!

Backup Summary:
  • Files Changed: [count]
  • Commit Hash: [hash]
  • Branch: main
  • Timestamp: [timestamp]

Changed Files (first 10):
  [list of files]

View on GitHub:
  https://github.com/igithub14/Geopolitical-Landscape/commits/main
```

### Failure Email (If Error Occurs)

**Subject**: 🚨 Git Backup FAILED - [Date]

**Body**:
```
Failed to [operation]:

Error:
[error details]

⚠️ Manual intervention may be required.
💡 [troubleshooting suggestions]
```

### No Changes Email (If Repository Clean)

**Subject**: ✅ Git Backup - No Changes - [Date]

**Body**:
```
Repository is clean - no changes to commit.

Status: Up to date with remote
Branch: main

ℹ️ No action required - all files already backed up.
```

---

## Monitoring & Maintenance

### Daily Monitoring

1. **Check Email** (every morning):
   * Verify backup email received
   * Read any failure notifications
   * Take action if errors reported

2. **GitHub Verification** (weekly):
   * Visit: https://github.com/igithub14/Geopolitical-Landscape/commits/main
   * Verify daily commits present
   * Check commit messages for consistency

3. **Job Run History** (weekly):
   * Workflows → Jobs → Git Daily Safety Backup
   * Click "Runs" tab
   * Review recent run history
   * Check for any failures

### Monthly Maintenance

* Review job logs for any warnings
* Verify email notifications still working
* Check Git credentials not expired
* Update script if needed (version in README)

---

## 🚨 Troubleshooting Guide

### Problem: No Email Received

**Solutions**:
1. Check spam/junk folder
2. Verify email address in Job notifications settings
3. Check Job run completed (Workflows → Jobs → Runs)
4. Verify notification settings include "On Success"

### Problem: Job Failed - Authentication Error

**Solutions**:
1. User Settings → Git Integration
2. Verify GitHub token still valid
3. Generate new token if expired
4. Update Databricks Git credentials
5. Re-run job manually to test

### Problem: Push Rejected (Non-Fast-Forward)

**Cause**: Remote repository has commits not present locally

**Solutions**:
1. Open repository in Databricks
2. Manually pull latest changes: `git pull origin main`
3. Resolve any merge conflicts
4. Next scheduled run will succeed

### Problem: Commit Created But Push Failed

**Cause**: Network issue or GitHub service disruption

**Solutions**:
1. Verify network connectivity
2. Check GitHub status: https://www.githubstatus.com
3. Next run will push accumulated commits
4. Manual push if urgent: `git push origin main`

### Problem: Job Not Running on Schedule

**Solutions**:
1. Check Job trigger is UNPAUSED
2. Verify cron expression correct: `0 23 * * *`
3. Check timezone: Europe/Rome
4. Review Job run history for any errors
5. Manually trigger to test

---

## 📞 Support

**Script Location**: `/Users/cristiano.mombello@gmail.com/Geopolitical_Landscape/git_daily_safety_backup.py`

**Repository**: https://github.com/igithub14/Geopolitical-Landscape

**Author**: Cristiano Mombello (cristiano.mombello@gmail.com)

**Last Updated**: 2026-07-23

---

## 🎯 Success Criteria

The backup system is working correctly when:

✅ Email received daily at ~23:01 (success or no-changes)

✅ GitHub shows daily commits with "[Automated Safety Backup]" message

✅ No failure emails received

✅ Job runs visible in Databricks Workflows (success status)

✅ All project work backed up within 24 hours

---

**Setup Complete! 🎉**

Your daily Git safety backup is now configured and will run automatically every day at 23:00.

You'll receive email notifications for every run, ensuring peace of mind that all work is safely backed up to GitHub.

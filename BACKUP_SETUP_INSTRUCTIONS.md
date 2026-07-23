#  Git Daily Safety Backup - Setup Instructions

**Script**: `git_daily_safety_backup.py`

**Purpose**: Automated daily commit and push to GitHub with email notifications

**Notification Email**: cristiano.mombello@gmail.com

---

## Expected Email Notifications

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

**Subject**: Git Backup FAILED - [Date]

**Body**:
```
Failed to [operation]:

Error:
[error details]

Manual intervention may be required.
[troubleshooting suggestions]
```

### No Changes Email (If Repository Clean)

**Subject**: ✅ Git Backup - No Changes - [Date]

**Body**:
```
Repository is clean - no changes to commit.

Status: Up to date with remote
Branch: main

No action required - all files already backed up.
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

## Troubleshooting Guide

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

## Support

**Script Location**: `/Users/cristiano.mombello@gmail.com/Geopolitical_Landscape/git_daily_safety_backup.py`

**Repository**: https://github.com/igithub14/Geopolitical-Landscape

**Author**: Cristiano Mombello (cristiano.mombello@gmail.com)

**Last Updated**: 2026-07-23

---

## Success Criteria

The backup system is working correctly when:

✅ Email received daily at ~23:01 (success or no-changes)

✅ GitHub shows daily commits with "[Automated Safety Backup]" message

✅ No failure emails received

✅ Job runs visible in Databricks Workflows (success status)

✅ All project work backed up within 24 hours
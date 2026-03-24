#!/usr/bin/env bash
# ============================================================
# 05_cron_check.sh — WP-Cron & Server Cron Audit
# Requires: SSH_HOST, SSH_USER, SSH_PORT, SSH_KEY_PATH, WP_PATH
# ============================================================

SSH_CMD="ssh -o StrictHostKeyChecking=no -p ${SSH_PORT:-22} ${SSH_KEY_PATH:+-i $SSH_KEY_PATH} $SSH_USER@$SSH_HOST"

echo "========================================"
echo "  AUDIT MODULE 5: Cron Jobs"
echo "========================================"

echo ""
echo "--- DISABLE_WP_CRON Setting ---"
$SSH_CMD "wp --path=$WP_PATH config get DISABLE_WP_CRON --skip-plugins --skip-themes 2>&1 || echo 'Not set (wp-cron is ENABLED via HTTP)'"

echo ""
echo "--- All Scheduled WP-Cron Events ---"
$SSH_CMD "wp --path=$WP_PATH cron event list --fields=hook,next_run_relative,recurrence,args 2>&1"

echo ""
echo "--- Total Cron Event Count ---"
$SSH_CMD "wp --path=$WP_PATH cron event list --format=count 2>&1"

echo ""
echo "--- Overdue Cron Events (past their scheduled run time) ---"
$SSH_CMD "wp --path=$WP_PATH cron event list --fields=hook,next_run_relative 2>&1 | grep -E '\-[0-9]+ (second|minute|hour|day)' || echo 'No overdue events detected'"

echo ""
echo "--- Cron Schedules Registered ---"
$SSH_CMD "wp --path=$WP_PATH cron schedule list 2>&1"

echo ""
echo "--- Manually Trigger wp-cron (test run) ---"
$SSH_CMD "wp --path=$WP_PATH cron event run --due-now 2>&1"

echo ""
echo "--- Server-Level Crontab (current user) ---"
$SSH_CMD "crontab -l 2>&1 || echo 'No crontab for current user'"

echo ""
echo "--- System-Wide Cron Jobs (if accessible) ---"
$SSH_CMD "ls /etc/cron.d/ 2>&1 && cat /etc/cron.d/* 2>&1 | grep -i 'wp\|wordpress\|php' || echo 'No WordPress-related system cron jobs found'"

echo ""
echo "[MODULE 5 COMPLETE]"

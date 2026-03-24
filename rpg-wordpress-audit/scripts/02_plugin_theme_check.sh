#!/usr/bin/env bash
# ============================================================
# 02_plugin_theme_check.sh — Plugin & Theme Audit
# Requires: SSH_HOST, SSH_USER, SSH_PORT, SSH_KEY_PATH, WP_PATH
# ============================================================

SSH_CMD="ssh -o StrictHostKeyChecking=no -p ${SSH_PORT:-22} ${SSH_KEY_PATH:+-i $SSH_KEY_PATH} $SSH_USER@$SSH_HOST"

echo "========================================"
echo "  AUDIT MODULE 2: Plugins & Themes"
echo "========================================"

echo ""
echo "--- Active Plugins (with versions) ---"
$SSH_CMD "wp --path=$WP_PATH plugin list --status=active --fields=name,version,update,update_version 2>&1"

echo ""
echo "--- Inactive Plugins ---"
$SSH_CMD "wp --path=$WP_PATH plugin list --status=inactive --fields=name,version 2>&1"

echo ""
echo "--- Must-Use Plugins ---"
$SSH_CMD "wp --path=$WP_PATH plugin list --status=must-use --fields=name,version 2>&1"

echo ""
echo "--- Plugins with Available Updates ---"
$SSH_CMD "wp --path=$WP_PATH plugin list --update=available --fields=name,version,update_version 2>&1"

echo ""
echo "--- Installed Themes ---"
$SSH_CMD "wp --path=$WP_PATH theme list --fields=name,status,version,update 2>&1"

echo ""
echo "--- Active Theme Details ---"
$SSH_CMD "wp --path=$WP_PATH theme get \$(wp --path=$WP_PATH theme list --status=active --field=name 2>&1) --fields=name,version,template,author 2>&1"

echo ""
echo "--- Themes with Available Updates ---"
$SSH_CMD "wp --path=$WP_PATH theme list --update=available --fields=name,version,update_version 2>&1"

echo ""
echo "[MODULE 2 COMPLETE]"

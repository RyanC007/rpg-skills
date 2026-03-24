#!/usr/bin/env bash
# ============================================================
# 01_core_check.sh — WordPress Core File & Version Audit
# Requires: SSH_HOST, SSH_USER, SSH_PORT, SSH_KEY_PATH, WP_PATH
# ============================================================

SSH_CMD="ssh -o StrictHostKeyChecking=no -p ${SSH_PORT:-22} ${SSH_KEY_PATH:+-i $SSH_KEY_PATH} $SSH_USER@$SSH_HOST"

echo "========================================"
echo "  AUDIT MODULE 1: WordPress Core"
echo "========================================"

echo ""
echo "--- WordPress Version ---"
$SSH_CMD "wp --path=$WP_PATH core version 2>&1"

echo ""
echo "--- Core Update Status ---"
$SSH_CMD "wp --path=$WP_PATH core check-update 2>&1"

echo ""
echo "--- Core File Integrity (Checksum Verification) ---"
$SSH_CMD "wp --path=$WP_PATH core verify-checksums 2>&1"

echo ""
echo "--- WordPress Configuration (wp-config.php) ---"
$SSH_CMD "wp --path=$WP_PATH config list --fields=name,value --skip-plugins --skip-themes 2>&1 | grep -v 'DB_PASSWORD\|AUTH_KEY\|SECURE_AUTH_KEY\|LOGGED_IN_KEY\|NONCE_KEY\|AUTH_SALT\|SECURE_AUTH_SALT\|LOGGED_IN_SALT\|NONCE_SALT'"

echo ""
echo "--- PHP Version ---"
$SSH_CMD "php -v 2>&1 | head -1"

echo ""
echo "--- wp-config.php File Permissions ---"
$SSH_CMD "stat -c '%a %n' $WP_PATH/wp-config.php 2>&1"

echo ""
echo "--- WordPress Memory Limit ---"
$SSH_CMD "wp --path=$WP_PATH eval 'echo WP_MEMORY_LIMIT;' 2>&1"

echo ""
echo "--- Active WordPress Locale ---"
$SSH_CMD "wp --path=$WP_PATH option get WPLANG 2>&1"

echo ""
echo "[MODULE 1 COMPLETE]"

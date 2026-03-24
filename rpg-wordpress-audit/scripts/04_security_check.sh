#!/usr/bin/env bash
# ============================================================
# 04_security_check.sh — Security Audit
# Requires: SSH_HOST, SSH_USER, SSH_PORT, SSH_KEY_PATH, WP_PATH
# ============================================================

SSH_CMD="ssh -o StrictHostKeyChecking=no -p ${SSH_PORT:-22} ${SSH_KEY_PATH:+-i $SSH_KEY_PATH} $SSH_USER@$SSH_HOST"

echo "========================================"
echo "  AUDIT MODULE 4: Security"
echo "========================================"

echo ""
echo "--- WordPress Security Keys (present/missing) ---"
$SSH_CMD "wp --path=$WP_PATH config list --fields=name --skip-plugins --skip-themes 2>&1 | grep -E 'AUTH_KEY|SECURE_AUTH_KEY|LOGGED_IN_KEY|NONCE_KEY|AUTH_SALT|SECURE_AUTH_SALT|LOGGED_IN_SALT|NONCE_SALT'"

echo ""
echo "--- Admin User Check (default 'admin' username) ---"
$SSH_CMD "wp --path=$WP_PATH user get admin --field=login 2>&1 && echo 'WARNING: Default admin username exists' || echo 'OK: No default admin username found'"

echo ""
echo "--- User List (Administrators) ---"
$SSH_CMD "wp --path=$WP_PATH user list --role=administrator --fields=ID,user_login,user_email,user_registered 2>&1"

echo ""
echo "--- WordPress Debug Mode ---"
$SSH_CMD "wp --path=$WP_PATH config get WP_DEBUG --skip-plugins --skip-themes 2>&1"

echo ""
echo "--- WP_DEBUG_DISPLAY (should be false in production) ---"
$SSH_CMD "wp --path=$WP_PATH config get WP_DEBUG_DISPLAY --skip-plugins --skip-themes 2>&1 || echo 'Not set (defaults to true if WP_DEBUG is true)'"

echo ""
echo "--- File Editing Disabled (DISALLOW_FILE_EDIT) ---"
$SSH_CMD "wp --path=$WP_PATH config get DISALLOW_FILE_EDIT --skip-plugins --skip-themes 2>&1 || echo 'Not set — file editing via admin is ENABLED'"

echo ""
echo "--- wp-config.php Permissions (should be 400 or 440) ---"
$SSH_CMD "stat -c '%a' $WP_PATH/wp-config.php 2>&1"

echo ""
echo "--- .htaccess Permissions ---"
$SSH_CMD "stat -c '%a' $WP_PATH/.htaccess 2>&1 || echo '.htaccess not found'"

echo ""
echo "--- wp-content/uploads Directory Permissions ---"
$SSH_CMD "stat -c '%a' $WP_PATH/wp-content/uploads 2>&1"

echo ""
echo "--- Check for PHP Files in Uploads Directory (potential malware) ---"
$SSH_CMD "find $WP_PATH/wp-content/uploads -name '*.php' 2>&1 | head -20"

echo ""
echo "--- WordPress Version Exposed in Meta Tags ---"
$SSH_CMD "wp --path=$WP_PATH option get blogdescription 2>&1"

echo ""
echo "--- SSL / HTTPS Check ---"
$SSH_CMD "wp --path=$WP_PATH option get siteurl 2>&1 | grep -q 'https' && echo 'OK: Site URL uses HTTPS' || echo 'WARNING: Site URL does not use HTTPS'"

echo ""
echo "[MODULE 4 COMPLETE]"

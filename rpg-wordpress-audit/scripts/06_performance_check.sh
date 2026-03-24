#!/usr/bin/env bash
# ============================================================
# 06_performance_check.sh — Performance & Caching Audit
# Requires: SSH_HOST, SSH_USER, SSH_PORT, SSH_KEY_PATH, WP_PATH
# ============================================================

SSH_CMD="ssh -o StrictHostKeyChecking=no -p ${SSH_PORT:-22} ${SSH_KEY_PATH:+-i $SSH_KEY_PATH} $SSH_USER@$SSH_HOST"

echo "========================================"
echo "  AUDIT MODULE 6: Performance & Caching"
echo "========================================"

echo ""
echo "--- Object Cache Type ---"
$SSH_CMD "wp --path=$WP_PATH cache type 2>&1"

echo ""
echo "--- Object Cache Drop-in Present ---"
$SSH_CMD "ls $WP_PATH/wp-content/object-cache.php 2>&1 && echo 'Object cache drop-in found' || echo 'No object cache drop-in'"

echo ""
echo "--- Advanced Cache Drop-in Present ---"
$SSH_CMD "ls $WP_PATH/wp-content/advanced-cache.php 2>&1 && echo 'Advanced cache drop-in found (page caching active)' || echo 'No advanced cache drop-in (no page caching)'"

echo ""
echo "--- Active Caching Plugins ---"
$SSH_CMD "wp --path=$WP_PATH plugin list --status=active --fields=name 2>&1 | grep -iE 'cache|rocket|litespeed|w3|swift|comet|breeze|sg-cachepress' || echo 'No common caching plugin detected'"

echo ""
echo "--- Active Image Optimisation Plugins ---"
$SSH_CMD "wp --path=$WP_PATH plugin list --status=active --fields=name 2>&1 | grep -iE 'smush|imagify|shortpixel|ewww|tinypng|optimole|kraken' || echo 'No common image optimisation plugin detected'"

echo ""
echo "--- PHP OPcache Status ---"
$SSH_CMD "php -r 'echo opcache_get_status() ? \"OPcache: ENABLED\" : \"OPcache: DISABLED\";' 2>&1 || echo 'Could not determine OPcache status'"

echo ""
echo "--- WordPress Site URL & Home URL ---"
$SSH_CMD "wp --path=$WP_PATH option get siteurl 2>&1"
$SSH_CMD "wp --path=$WP_PATH option get home 2>&1"

echo ""
echo "--- Post Count by Type ---"
$SSH_CMD "wp --path=$WP_PATH post list --post_status=publish --format=count 2>&1 | xargs -I{} echo 'Published posts: {}'"
$SSH_CMD "wp --path=$WP_PATH post list --post_type=page --post_status=publish --format=count 2>&1 | xargs -I{} echo 'Published pages: {}'"

echo ""
echo "--- Disk Usage of wp-content ---"
$SSH_CMD "du -sh $WP_PATH/wp-content/ 2>&1"
$SSH_CMD "du -sh $WP_PATH/wp-content/uploads/ 2>&1"
$SSH_CMD "du -sh $WP_PATH/wp-content/plugins/ 2>&1"
$SSH_CMD "du -sh $WP_PATH/wp-content/themes/ 2>&1"

echo ""
echo "--- PHP Error Log (last 50 lines) ---"
$SSH_CMD "find /var/log /tmp $WP_PATH -name 'error_log' -o -name 'php_error.log' -o -name 'debug.log' 2>/dev/null | head -3 | xargs -I{} sh -c 'echo \"=== {} ===\"; tail -50 {}' 2>&1 || echo 'Could not locate PHP error log'"

echo ""
echo "[MODULE 6 COMPLETE]"

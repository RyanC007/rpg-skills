#!/usr/bin/env bash
# ============================================================
# 03_database_check.sh — Database Health Audit
# Requires: SSH_HOST, SSH_USER, SSH_PORT, SSH_KEY_PATH, WP_PATH
#           DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
# ============================================================

SSH_CMD="ssh -o StrictHostKeyChecking=no -p ${SSH_PORT:-22} ${SSH_KEY_PATH:+-i $SSH_KEY_PATH} $SSH_USER@$SSH_HOST"
MYSQL_CMD="mysql -h$DB_HOST -u$DB_USER -p$DB_PASSWORD $DB_NAME"

echo "========================================"
echo "  AUDIT MODULE 3: Database Health"
echo "========================================"

echo ""
echo "--- WP-CLI Database Check (Table Integrity) ---"
$SSH_CMD "wp --path=$WP_PATH db check 2>&1"

echo ""
echo "--- Database Size ---"
$SSH_CMD "wp --path=$WP_PATH db size --tables 2>&1"

echo ""
echo "--- MySQL / MariaDB Version ---"
$SSH_CMD "$MYSQL_CMD -e 'SELECT VERSION();' 2>&1"

echo ""
echo "--- Top 10 Largest Tables ---"
$SSH_CMD "$MYSQL_CMD -e \"
  SELECT table_name AS 'Table',
         ROUND((data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
  FROM information_schema.tables
  WHERE table_schema = '$DB_NAME'
  ORDER BY (data_length + index_length) DESC
  LIMIT 10;
\" 2>&1"

echo ""
echo "--- Transient Count (can bloat wp_options) ---"
$SSH_CMD "wp --path=$WP_PATH eval 'global \$wpdb; echo \$wpdb->get_var(\"SELECT COUNT(*) FROM \$wpdb->options WHERE option_name LIKE \\\"_transient_%\\\"\");' 2>&1"

echo ""
echo "--- Autoloaded Options Size ---"
$SSH_CMD "wp --path=$WP_PATH eval 'global \$wpdb; \$result = \$wpdb->get_var(\"SELECT SUM(LENGTH(option_value)) FROM \$wpdb->options WHERE autoload = \\\"yes\\\"\"); echo round(\$result / 1024, 2) . \" KB\";' 2>&1"

echo ""
echo "--- Post Revisions Count ---"
$SSH_CMD "wp --path=$WP_PATH eval 'global \$wpdb; echo \$wpdb->get_var(\"SELECT COUNT(*) FROM \$wpdb->posts WHERE post_type = \\\"revision\\\"\");' 2>&1"

echo ""
echo "--- Spam Comments Count ---"
$SSH_CMD "wp --path=$WP_PATH eval 'global \$wpdb; echo \$wpdb->get_var(\"SELECT COUNT(*) FROM \$wpdb->comments WHERE comment_approved = \\\"spam\\\"\");' 2>&1"

echo ""
echo "[MODULE 3 COMPLETE]"

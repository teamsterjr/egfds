import os
MYSQL_USER = os.environ.get('RDS_USERNAME', 'root')
MYSQL_PASSWORD = os.environ.get('RDS_PASSWORD')
MYSQL_HOST = os.environ.get('RDS_HOSTNAME', '127.0.0.1')
MYSQL_PORT = os.environ.get('RDS_PORT', 3306)
MYSQL_DB = os.environ.get('RDS_DB', 'EGFDS')
SITE_NAME = 'EGFDS!'
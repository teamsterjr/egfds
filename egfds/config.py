import os
DB_USER = os.environ.get('RDS_USERNAME', 'root')
DB_PASSWORD = os.environ.get('RDS_PASSWORD')
DB_HOST = os.environ.get('RDS_HOSTNAME', '127.0.0.1')
DB_PORT = os.environ.get('RDS_PORT', 5432)
DB_DB = os.environ.get('RDS_DB', 'egfds')
SITE_NAME = 'EGDS!'

import pymssql
import os

INHEALTH_DB_USER = os.environ.get('INHEALTH_DB_USER')
INHEALTH_DB_PASSWORD = os.environ.get('INHEALTH_DB_PASSWORD')

def get_db():
	conn = pymssql.connect(server= 'inhealth.wse.jhu.edu', user=INHEALTH_DB_USER, password=INHEALTH_DB_PASSWORD, database='master')
	cursor = conn.cursor()
	return cursor
import sqlite3
from os.path import dirname, abspath



#-------------------------------------------
def get_db_file_loc():
	parent_dir = dirname(abspath(__file__))
	sqlite_file = parent_dir + "/"+ 'smrt_db.sqlite'    # name of the sqlite database file

	return sqlite_file
#============================================
def create_db():
	sqlite_file = get_db_file_loc()
	table_name = 'results'  # name of the table to be created
	field_1_name = 'tree_id' # name of the column
	field_1_type = 'TEXT'  # column data type

	field_2_name = 'job_id' # name of the column
	field_2_type = 'TEXT'  # column data type

	field_3_name = 'job_status' # name of the column
	field_3_type = 'TEXT'  # column data type

	field_4_name = 'execution_time' # name of the column
	field_4_type = 'REAL'  # column data type

	field_5_name = 'current_job_step' # name of the column
	field_5_type = 'INTEGER'  # column data type	
		
	try:
		# Connecting to the database file
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()

		# Creating a table
		# note that PRIMARY KEY column must consist of unique values!
		c.execute('CREATE TABLE {tn} ({nf1} {ft1} PRIMARY KEY, {nf2} {ft2}, {nf3} {ft3}, {nf4} {ft4}, {nf5} {ft5})'\
        .format(tn=table_name, nf1=field_1_name, ft1=field_1_type, nf2=field_2_name, ft2=field_2_type, nf3=field_3_name, ft3=field_3_type, nf4=field_4_name, ft4=field_4_type, nf5=field_5_name, ft5=field_5_type))

		# Committing changes and closing the connection to the database file
		conn.commit()
		print "smrt database created"
	except sqlite3.Error as e:
		print "An error occurred:", e.args[0]
	conn.close()
	
#------------------------------------------------
def insert_db(tid, jid, jst, et, cjstp):
	sqlite_file = get_db_file_loc()
	try:
		# Connecting to the database file
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()

		# Inserts record into the database
		sql_stmt = "INSERT INTO results VALUES ('"+tid+"','"+jid+"','"+jst+"',"+str(et)+","+str(cjstp)+")" 
		c.execute(sql_stmt)

		conn.commit()
		print "record inserted into database"

	except sqlite3.IntegrityError:
		print('ERROR: ID already exists in PRIMARY KEY column {}'.format(field_1_name))
	except sqlite3.Error as e:
		print "An error occurred:", e
	
	conn.close()

#------------------------------------------------
def query_jid_db(jid):
	tree_id, job_status, ex_time, cur_step = None, None, None, None
	sqlite_file = get_db_file_loc() 
	try:
		# Connecting to the database file
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()

		# Query record from the database
		c.execute("SELECT * FROM results WHERE job_id='{j_id}'".format(j_id=jid))
		id_exists = c.fetchone()
		if id_exists:
			tree_id = id_exists[0]
			job_status = id_exists[2]
			ex_time = id_exists[3]
			cur_step = id_exists[4]
		else:
			print(':( {} does not exist'.format(jid))

	except sqlite3.Error as e:
		print "An error occurred:", e
	
	conn.close()

	return tree_id, job_status, cur_step, ex_time

#--------------------------------------------
def query_tid_db(tid):
	tree_id, job_id, job_status, ex_time, cur_step = None, None, None, None, None
	sqlite_file = get_db_file_loc() 
	try:
		# Connecting to the database file
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()

		# Query record from the database
		c.execute("SELECT * FROM results WHERE tree_id='{t_id}'".format(t_id=tid))
		id_exists = c.fetchone()
		if id_exists:
			tree_id = id_exists[0]
			job_id = id_exists[1]
			job_status = id_exists[2]
			ex_time = id_exists[3]
			cur_step = id_exists[4]
		else:
			print(':( {} does not exist'.format(tid))

	except sqlite3.Error as e:
		print "An error occurred:", e
	
	conn.close()

	return tree_id, job_id, job_status, cur_step, ex_time

#--------------------------------------------
def query2_db():
	tree_id, job_state, ex_time = None, None, None
	sqlite_file = get_db_file_loc() 
  
	try:
		# Connecting to the database file
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()

		c.execute("SELECT * FROM results")
		all_rows = c.fetchall()
		print('All rows: ', all_rows)

	except sqlite3.Error as e:
		print "An error occurred:", e
	
	conn.close()

#--------------------------------------------
#if __name__ == "__main__":
	#create_db()
	#print get_db_file_loc()
	#insert_db("c4fb4-112233434", "c4fb47f4-8f13-4272-aa00-7134d24a2744", "SUCCESS", 300.56, 11)
	#print query_db("c4fb47f4-8f13-4272-aa00-7134d24a2744")
	#print query_tid_db("c4fb4-112233434")	
	#query2_db()

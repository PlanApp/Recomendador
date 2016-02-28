import psycopg2


#try:
#    conn = psycopg2.connect("dbname='freetalk' user='@' host='@' password='@)
#except:
#    print "I am unable to connect to the database"

class DataBase:
        def __init__(self):
		try:
	                DBNAME="@"
	                USER="@"
	                HOST="@"
	                PASSWD="@"

			self.conn = psycopg2.connect("dbname='%s' user='%s'  host='%s' password='%s'" %(DBNAME, USER, HOST,PASSWD))
	                self.cur = self.conn.cursor()
                        print "--------------------"
                        print "[[  conect BDD :)  ]]"
                        print "--------------------"
		except:
			print ""
			print "--------------------"
			print "[[Error conect BDD]]"
			print "--------------------"
			print ""



	def select_multi(self,sql):
		self.cur.execute('%s' %(sql))
		query = self.cur.fetchall() #multiples filas
		return query

	def select(self,sql):
		self.cur.execute('%s' %(sql))
		query = self.cur.fetchone() #una sola fila 
		return query

	def update(self,sql):
		self.cur.execute('%s' %(sql))
		self.conn.commit()

	def insert(self,sql):
		self.cur.execute('%s' %(sql))
		self.conn.commit()
        def close(self):
                conn.close()



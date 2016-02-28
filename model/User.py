#
#
# Tabla users
# Funciones para consultar a la base de datos
# PostgresSQL
#

#import conexion
#cur=conexion.pgsql();
import sys
sys.path.append('../config/')
import Config

cur=Config.DataBase();

class User:
	def __init__(self):
		self.id=0
		self.name=""
		self.lastname=""
		self.email=""
		self.birthday=""
		self.sex=""
		self.url_photo=""
		self.passwd=""
		self.nick=""

	def getAllUser(self):
		rows = cur.select_multi("SELECT id, name, nick, passwd  FROM users;")
		return rows #Arreglo de usuarios

	def getUserById(self, idx):
		try:
			query = cur.select("SELECT id, name, nick, passwd  FROM users where id='%s';" %( idx ))
			return query
		except:
			return (-1)

	def getUserByName(self, namex):
		try:
			query = cur.select("SELECT id, name, nick, passwd  FROM users where name='%s';" %( namex ))
			return query
		except:
			return (-1)

	def getIDUserByNick(self, nickx):
                try:
                        query = cur.select("SELECT id FROM users where nick='%s';" %( nickx ))
                        return query[0]
                except:
                        return "null"


	def registro(self, namex, lastnamex, emailx, birthdayx, sexx, url_photox, passwdx, nickx):
		try:
			if (str(self.getIDUserByNick(nickx)) == "null" ):
				query= cur.insert("INSERT INTO users (name, lastname, email, birthday, sex, url_photo, passwd, nick) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(namex, lastnamex, emailx, birthdayx, sexx, url_photox, passwdx, nickx))
				return "Ok"
			return "null"
		except:
			return (-1)

#import User
import sys
sys.path.append('../model/')
import User


#LLAMADA A EL MODELO DEL USUARIO
userx = User.User()

#CONSULTAR POR TODOS LOS USUARIOS
rows = userx.getAllUser()
for row in rows:
	print row[0], row[1], row[2], row[3]

#CONSULTAR POR UN USUARIO POR LLAVE PRIMARIA (ID)
var = userx.getUserById(1)
print var


#CONSULTA POR UN USUARIO POR NOMBRE
var = userx.getUserByName('Leonardo')
print var


#CONSULTA EL ID DE UN NICK
try:
	var = userx.getIDUserByNick('l30bravo')
	print var
except:
	print "Error getUserByNick"


#INSERTAR USUARIO
try:
	var = userx.registro('Test', 'test', 'test@mail.cl', '12/12/1900', 'M', 'none', '124', 'Prueba2')
	print var
except:
	print "Error a ingresar usuario"

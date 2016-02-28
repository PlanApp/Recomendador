#WEBSERVICE PLANAPP V2.0

#!flask/bin/python
##import bdd
##import os
##import recomendador
from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from flask import Response

#DECORADOR HTML LIBRERIA
# permite dejar en formato http las respuestas del webservice.
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

#DECORADOR HTML
# funcion para realizar crossdoamin y responder el json en formato http
def crossdomain(origin=None, methods=None, headers=None,max_age=21600, attach_to_all=True,automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

#### WEBSERVICE PAGINAS ####

app = Flask(__name__)

#INDEX
@app.route('/')
@app.route('/index')
def index():
	return "PanApp Webservice : Hello, World!"


#CANCIONES PARA USUARIOS NO REGISTRADOS (RANDOM)
@app.route('/songs',  methods=['GET'])
@crossdomain(origin='*')
def get_any():
        mood = []
        mood.append(float(float(request.args['mood_1'])/100))
        mood.append(float(float(request.args['mood_2'])/100))
        mood.append(float(float(request.args['mood_3'])/100))
        mood.append(float(float(request.args['mood_4'])/100))
        mood.append(float(float(request.args['mood_5'])/100))
	print "pensativo_enloquecido :"+str(mood[0])+" triste_feliz : "+str(mood[1])+" paz_furioso :"+str(mood[2])+" frio_caliente :"+str(mood[3])
	
	item = bdd.Item()
	song = item.getAnySong(mood)
	id_song = song.getId()
	cancion = song.getCancion()
	banda = song.getBanda()
	frase = song.getFrase()
	print cancion
	data = {'id':str(id_song), 'nombre': str(cancion),'frase': str(frase), 'banda':str(banda)} 
	respuesta =  json.dumps(data)
	print respuesta
        return Response(respuesta, content_type='application/json')


#CANCIONES PARA USUARIOS  REGISTRADOS (RECOMENDADOR)
@app.route('/usongs',  methods=['GET'])
@crossdomain(origin='*')
def get_usersong():
        mood = []
        mood.append(float(float(request.args['mood_1'])/100))
        mood.append(float(float(request.args['mood_2'])/100))
        mood.append(float(float(request.args['mood_3'])/100))
        mood.append(float(float(request.args['mood_4'])/100))
        mood.append(float(float(request.args['mood_5'])/100))
	id_user = request.args['id']
	cont = request.args['cont']
	cont_dos=0
	cancion=""
        #print "pensativo_enloquecido :"+str(mood[0])+" triste_feliz : "+str(mood[1])+" paz_furioso :"+str(mood[2])+" frio_caliente :"+str(mood[3])
	item = bdd.Item()
	item_virtual = item.itemVirtual(id_user)
	cont_likes = item.verLikes(id_user)


	if (cont_likes != 0):
		cluster = item.getCluster(id_user)
		#CUANDO EL CLUESTER ES NULL QUE RECOMIENDE CUALQUIERA
		#capturar una cancion
		recomender = recomendador.Recomendador(mood,item_virtual)
		rank=recomender.rankear(cluster)
		#data="["
		for item in rank:
		        #print respuestas.getBanda()
		        #print respuestas.getID(), respuestas.getDistancia(), respuestas.getFrase(), respuestas.getCancion(), respuestas.getAutor()
			if (int (cont) == cont_dos):
				#cancion = "{'id':'%s', 'nombre':'%s', frase:'%s'm 'banda':'%s'}" %(item.getID(), item.getCancion(), item.getFrase(), item.getAutor());
				cancion = {'id':str(item.getID()), 'nombre':str(item.getCancion()), 'frase':str(item.getFrase()), 'banda':str(item.getAutor())} 
			#data = data + " " + cancion + ","
			cont_dos=cont_dos+1
		#data= data + "]"
	if (cont_likes ==0):
		song = item.getAnySong(mood)
        	id_song = song.getId()
	        cancion = song.getCancion()
	        banda = song.getBanda()
	        frase = song.getFrase()
	        print cancion
	        cancion = {'id':str(id_song), 'nombre': str(cancion),'frase': str(frase), 'banda':str(banda)}

        respuesta =  json.dumps(cancion)
        print respuesta
        return Response(respuesta, content_type='application/json')


@app.route('/like', methods=['POST'])
@crossdomain(origin='*')
def get_like():
        id_item = request.form['id_item']
        id_user = request.form['id_user']
	l = bdd.Like()
	l.doneLike(id_user, id_item, 1) #Registra el like en la BDD
	print id_item, id_user
	data = {'edo':'ok'}
        respuesta = json.dumps(data)
        print respuesta
        return Response(respuesta, content_type='application/json')

#LOGIN
@app.route('/login', methods=['POST'])
@crossdomain(origin='*')
def signup():
	user = "";
	passwd="";
        user = request.form['user']
        passwd = request.form['passwd']
        Userx = bdd.User()
        Id = Userx.login(user,passwd)
        print "login:"+user+" - "+passwd
        if (Id !=0):
                data = {'id': str(Id),'user': str(user), 'edo':'ok'} #USUARIO VALIDO
        else:
        	data = {"id":"0", "user": str(user), "edo":"no"} #USUARIO INVALIDO
        respuesta = json.dumps(data)
	print respuesta
        return Response(respuesta, content_type='application/json')


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
        app.debug = True
    	app.run(host='0.0.0.0', port=port)



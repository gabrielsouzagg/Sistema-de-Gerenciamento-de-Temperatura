
from flask import Flask,request, jsonify
from config import app_config, app_active
from flask_restful import Resource, Api
from sqlalchemy import create_engine, text
from json import dumps
from flask_cors import CORS,cross_origin
from datetime import datetime

config = app_config[app_active]

db_connect = create_engine('mysql+mysqlconnector://root@localhost/fatec')

def create_app(config_name):

    app = Flask(__name__, template_folder='templates')

    cors = CORS(app, resources={r'/monitoramento/*':{'origins':'*'}})

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    @app.route('/monitoramento/grafico1', methods=['GET'])
    def TotalizacaoRegistro():
       conn = db_connect.connect()
       query = conn.execute(text('SELECT dispositivo, COUNT(dispositivo) as TotalRegistros FROM monitoramento GROUP BY dispositivo limit 20'))
       conn.commit()
       result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
       conn.close()
       return jsonify(result)

    @app.route('/monitoramento', methods=['POST', 'GET', 'DELETE', 'PUT'])
    def monitoramento():
        # origin = request.headers.get('Origin')
        if ( request.method == "GET" ):
            conn = db_connect.connect()
            query = conn.execute(text("SELECT id, temperatura, umidade, dispositivo, luminosidade, presenca, distancia, dt_created FROM monitoramento ORDER BY id DESC LIMIT 20"))
            conn.commit()
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

            return jsonify(result)
        
        elif ( request.method == "POST" ):
            conn = db_connect.connect()
            temperatura = request.json['temperatura']
            umidade = request.json['umidade']
            dispositivo = request.json['dispositivo']        
            luminosidade = request.json['luminosidade']
            conn.execute(text("insert into monitoramento (temperatura, umidade, dispositivo, luminosidade ) values ( '{0}', '{1}', '{2}' , '{3}')".format(temperatura, umidade, dispositivo,luminosidade)))        
                    
            #
            query = conn.execute(text("SELECT id, temperatura, umidade, dispositivo, luminosidade, presenca, distancia, DATE_FORMAT(dt_created, '%d/%m/%Y') AS data FROM monitoramento ORDER BY id DESC LIMIT 20"))
            conn.commit()
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            #
            return jsonify(result) 
 
        elif ( request.method == "PUT" ):
            conn = db_connect.connect()
            id_ = request.json['id']
            temperatura = request.json['temperatura']
            umidade = request.json['umidade']
            dispositivo = request.json['dispositivo'] 
            luminosidade = request.json['luminosidade'] 
            query = conn.execute(text("update monitoramento set temperatura = '{0}' , umidade = '{1}' , dispositivo = '{2}' , luminosidade = '{3}' where Id = {4}".format(temperatura, umidade, dispositivo, luminosidade, id_)))
            conn.commit()        
            query = conn.execute(text("SELECT id, temperatura, umidade, dispositivo, luminosidade, presenca, distancia, DATE_FORMAT(dt_created, '%d/%m/%Y') AS data FROM monitoramento ORDER BY id DESC LIMIT 20"))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]        
            return jsonify(result) 
        
        elif ( request.method == "DELETE" ):
            conn = db_connect.connect()
            id_ = request.json['id']
            query = conn.execute(text("delete from monitoramento where Id = {0}".format(id_)))
            conn.commit()        
            query = conn.execute(text("SELECT id, temperatura, umidade, dispositivo, luminosidade, presenca, distancia, DATE_FORMAT(dt_created, '%d/%m/%Y') AS data FROM monitoramento ORDER BY id DESC LIMIT 20"))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]        
            return jsonify(result) 
        

    @app.route('/monitoramento/<id>', methods=["GET"])
    def monitoramentoId(id):
        conn = db_connect.connect()
        
        query = conn.execute(text("SELECT id, temperatura, umidade, dispositivo, luminosidade, presenca, distancia, DATE_FORMAT(dt_created, '%d/%m/%Y') AS data FROM monitoramento where id = '{0}' order by temperatura".format(id)))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        return jsonify(result)
    
    return app

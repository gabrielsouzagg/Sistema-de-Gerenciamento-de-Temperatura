# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine, text

# config import
from config import app_config, app_active

config = app_config[app_active]

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db_connect = create_engine('mysql+mysqlconnector://admin:admin@192.168.13.236/fatec')

    api = Api(app)

    class Monitoramento(Resource):
        # get-all
        def get(self):
            conn = db_connect.connect()
            query = conn.execute(text('select * from monitoramento order by temperatura'))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return jsonify(result)

        def post(self):
            conn = db_connect.connect()
            temperatura = request.json['temperatura']
            umidade = request.json['umidade']
            dispositivo = request.json['dispositivo']
            conn.execute(text("insert into monitoramento (temperatura, umidade, dispositivo) values ( '{0}', '{1}', '{2}')".format(temperatura, umidade, dispositivo)))
            conn.commit()
            query = conn.execute(text('select * from monitoramento order by temperatura'))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return jsonify(result)


        def delete(self):
            conn = db_connect.connect()
            id_ = request.json['Id']
            query = conn.execute(text("delete from monitoramento where Id = {0}".format(id_)))
            conn.commit()
            query = conn.execute(text('select * from monitoramento order by temperatura'))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return jsonify(result)

    class MonitoramentoByDispositivo(Resource):
        # get by dispositivo
        def get(self, dispositivo):
            conn = db_connect.connect()
            query = conn.execute(text("select * from monitoramento where dispositivo = '{0}' order by temperatura".format(dispositivo)))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return jsonify(result)

    api.add_resource(Monitoramento, '/monitoramento')
    api.add_resource(MonitoramentoByDispositivo, '/monitoramento/<dispositivo>')

    return app

if __name__ == '__main__':
    app = create_app(app_active)
    app.run()

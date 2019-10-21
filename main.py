from datetime import datetime
import json
import requests
import pprint
import time
import os
import MySQLdb
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
from flask_caching import Cache

from flask import Flask, jsonify, request

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
date_time = time.strftime("%Y-%m-%d %H:%M:%S")
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
access_token = os.environ.get('ACCESS_TOKEN')
ssl_ca = os.environ.get('CLOUD_SQL_CA')  # SSL
ssl_key = os.environ.get('CLOUD_SQL_CERT')  # SSL
ssl_cert = os.environ.get('CLOUD_SQL_KEY')  # SSL
key_sheets = os.environ.get('KEY_SHEETS')
plan_id = os.environ.get('PLAN_ID')

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)

cache.init_app(app)


@cache.cached(timeout=3600)
def create_id():
    escopo = ['https://spreadsheets.google.com/feeds',
              'https://www.googleapis.com/auth/drive.readonly']
    credenciais = ServiceAccountCredentials.from_json_keyfile_name(
        key_sheets, escopo)
    autorizacao = gspread.authorize(credenciais)
    sheets = autorizacao.open_by_key(plan_id).worksheet('ID')
    dados = sheets.get_all_records()
    df_sheets = pd.DataFrame(dados, dtype=str)
    lista = list(df_sheets['ID_Facebook'])
    return_list = []
    for string in lista:
        string = string.rstrip()
        if string != '':
            return_list.append(string)
    return return_list


@app.route('/list_id', methods=['GET'])
def verify_form_id(form_id='facebook ids'):
    lista = create_id()
    pprint.pprint(f'lista: {lista}')
    if request.method == 'GET':
        if form_id in lista:
            return str(lista)
        else:
            return str(lista)
    else:
        if form_id in lista:
            return True
        else:
            return False


def read_leadgen(leadgen_id, access_token):
    endpoint = f"https://graph.facebook.com/v3.2/{leadgen_id}?access_token={access_token}"
    retorno_uri = requests.api.get(endpoint, verify=False).json()
    return retorno_uri
# carlos


def save_mysql(email='email', nome='nome', fb_leadgen_id='fb_leadgen_id', fb_form_id='fb_form_id', fb_page_id='fb_page_id', fb_creation_date_stamp='creation_date_stamp', id_vtex='id_vtex', href_vtex='id_vtexhref_vtex', documentId_vtex='documentId_vtex'):
    date_time = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    unix_socket = '/cloudsql/{0}'.format(db_connection_name)
    conn = MySQLdb.connect(
        user=db_user,
        passwd=db_password,
        unix_socket=unix_socket,
        db=db_name, ssl={'ca': ssl_ca, 'key': ssl_key, 'cert': ssl_cert})
    try:
        cursor = conn.cursor()
        sql = '''
        INSERT INTO table_leads_facebook(
            email, 
            nome, 
            fb_leadgen_id, 
            fb_form_id, 
            fb_page_id, 
            fb_created_time_stamp, 
            id_vtex, href_vtex, 
            documentId_vtex, 
            xCodigoParceria, 
            xCodigoParceriaOrigem, 
            date_time)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, 10101698, 10101698, %s);
        '''
        val = (email, nome, fb_leadgen_id, fb_form_id, fb_page_id,
               fb_creation_date_stamp, id_vtex, href_vtex, documentId_vtex, date_time)
        cursor.execute(sql, val)
        conn.commit()
        print('INSERIDO COM SUCESSO NO MYSQL')
    except Exception as Erro:
        conn.rollback()
        pprint.pprint(Erro)
    finally:
        conn.close()
        print('FINALIZANDO CONNEXÃO MYSQL')
#=-=-=--=-=-=-=-=#


def save_vtex(email, nome, fb_leadgen_id, fb_form_id, fb_page_id, fb_creation_date_stamp):
    url = 'url_vtex'
    data = {"email": email, "firstName": nome,
            "xCodigoParceria": 10101698, "xCodigoParceriaOrigem": 10101698}
    headers = {'Content-Type': "application/json"}
    retorno = requests.api.put(
        url=url, data=json.dumps(data), headers=headers).json()
    pprint.pprint(retorno)
    if 'DocumentId' in retorno:
        id_vtex = retorno['Id']
        href_vtex = retorno['Href']
        documentId_vtex = retorno['DocumentId']
        save_mysql(
            email=email,
            nome=nome,
            fb_leadgen_id=fb_leadgen_id,
            fb_form_id=fb_form_id,
            fb_page_id=fb_page_id,
            fb_creation_date_stamp=fb_creation_date_stamp,
            id_vtex=id_vtex,
            href_vtex=href_vtex,
            documentId_vtex=documentId_vtex)
    else:
        save_mysql(
            email=email,
            nome=nome,
            fb_leadgen_id=fb_leadgen_id,
            fb_form_id=fb_form_id,
            fb_page_id=fb_page_id,
            fb_creation_date_stamp=fb_creation_date_stamp,
            id_vtex=None,
            href_vtex=None,
            documentId_vtex=None)
# carlos
@app.route('/real_time', methods=['GET', 'POST'])
def real_time():
    if request.method == 'GET':
        hub_mode = request.args.get('hub.mode')
        hub_verify_token = request.args.get('hub.verify_token')
        hub_challenge = request.args.get('hub.challenge')
        if hub_mode == "subscribe" and hub_verify_token == "access_token":
            return hub_challenge
        else:
            print("ENTROU NO ELSE")
            return "entrou no else"
    elif request.method == 'POST':
        parameters = request.get_json()
        webhook_value = parameters["entry"][0]["changes"][0]["value"]
        pprint.pprint(f'REQUEST1 FACEBOOK\n{webhook_value}\n')
        leadgen_id = webhook_value["leadgen_id"]
        form_id = webhook_value["form_id"]
        page_id = webhook_value["page_id"]
        creation_date_stamp = webhook_value['created_time']

    if verify_form_id(form_id=form_id) == True:
        print('ESTOU NO IF')
        retorno_read_leadgen = read_leadgen(leadgen_id, access_token)
        if 'error' in access_token:
            pprint.pprint(f"{retorno_read_leadgen}")
            return f"Retornou erro{retorno_read_leadgen}"
        else:
            print('FACEBOOK TWO')
            pprint.pprint(retorno_read_leadgen)
            print('FACEBOOK TWO\n\n\n\n\n\n')
            if 'email' in retorno_read_leadgen['field_data'][0]['name']:
                email = str(retorno_read_leadgen['field_data'][0]['values'][0])
                nome = str(retorno_read_leadgen['field_data'][1]['values'][0])
            else:
                email = str(retorno_read_leadgen['field_data'][1]['values'][0])
                nome = str(retorno_read_leadgen['field_data'][0]['values'][0])
            save_vtex(email=email, nome=nome, fb_leadgen_id=leadgen_id, fb_form_id=form_id,
                      fb_page_id=page_id, fb_creation_date_stamp=creation_date_stamp)
            return 'INSERIDO EM VTEX E MYSQL'
    else:
        print('form id inválido')
        return('form id inválido')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

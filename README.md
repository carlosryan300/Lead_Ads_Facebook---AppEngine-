# AppEngine Lead Ads

## main.py

### [def create_id()](https://github.com/carlosryan301/AppEngineTest/blob/master/main.py)
* MÉTODO RESPONSÁVEL POR AUTALIZAR A LISTA DE FORM_ID USANDO A PLANILHA DO GOOGLE SHEETS.
* O MÉTODO FOI CONSTRUIDO PARA QUE USE CACHE COM TIMEOUT DE 3600seg, SENDO ASSIM DIMININUI A LATÊNCIA DE REQUISIÇÕES MEDIANTE AO FACEBOOK.
### [def verify_form_id() ](https://github.com/carlosryan301/AppEngineTest/blob/master/main.py)
* VALIDAR  FORM ID DO FACEBOOK

### [def read_leadgen()](https://github.com/carlosryan301/AppEngineTest/blob/master/main.py)
* FUNÃO DE GET PARA API FACEBOOK LEADGEN USANDO ACCESS_TOKEN
### [def save_mysql()](https://github.com/carlosryan301/AppEngineTest/blob/master/main.py)
* FUNÇÃO RESPONSÁVEL POR CRIAR CONEXÃO COM MYSQL
* CONEXÃO USA UNIX_SOCKET PARA CONEXÃO VIA GCP
* INSERT NO BANCO DE DADOS
* USA VARIÁVEL DE AMBIENTE PARA PEGAR OS PARÂMETROS DE CONEXÃO.
### [def save_vtex()](https://github.com/carlosryan301/AppEngineTest/blob/master/main.py)
* FUNÇÃO DE PUT PARA SERTAR O NOVO CADASTRO NA VTEX
### [def real_time()](https://github.com/carlosryan301/AppEngineTest/blob/master/main.py)
* FUNÇAO FLASK REAL_TIME COM METÓDOS GET E POST
#### GET
> PEGA O HUB_VERIFY_TOKEN NO  HUB DO FACEBOOK
#### POST
> METÓDO RESPONSÁVEL POR RECEBER OS DADOS DE CADATRASDO DO LEADS DO FACEBOOK.
> COLETA AS INFORMAÇÕES DE NOME, EMAIL, FB_ID, FB_LEADGEN, ETC.
> CHAMA AS OUTRAS FUNÇÕES PARA INSERIR NA VTEX E MYSQL
## [app.yaml](https://github.com/carlosryan301/AppEngineTest/blob/master/app.yaml)
### runtime
* VERSÃO DO PYTHON
### env_variables
* VARIAVÉIS DE AMBIENTE
* SETADAS AUTOMÁTICAMENTE NO DEPLOY DO APP ENGINE
## [requirements.txt](https://github.com/carlosryan301/AppEngineTest/blob/master/requirements.txt)
* BIBLIOTECAS NECESSÁRIA NA APLICAÇÃO



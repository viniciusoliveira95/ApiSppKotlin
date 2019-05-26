from flask import Flask, jsonify, request
import json
import urllib.request
import random
import datetime

app = Flask(__name__)


key = "AAAAIr-TAKU:APA91bE-x-a3BLiKNPYuepFTXhhetURsq7-Z5Ocwe6ikbGFkfa4vzzzxtvZVj1J7hiwLQ3JOVakBi274xqrKNoI7VvfXkUuglcZt1gpXj3UMSmoKVQ5q-06-bc2pagt6hRGWKWDSZcHz"
token = "cicwFTl8KuE:APA91bESEuXMkQbHM4tQEjNCmLGOftHTzzRSpbfEHDNxlPHWeQUj5uAwkVxpsB_1k_jAlDliXRs3xMbe9qYwg9bkzPVvnDWofu3oTcM7qfvDxC9ifWEXAlhcJc_ZHCTp-TCaHx-0Zsx4"

#######################################################################################################################
# ORÇAMENTOS

orcamentos = [{"idOrcamento": 1, "nome": "Orçamento prédio Ana Maria", "valorTotal":20000, "cliente": "Jaqueline Amaral", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 2, "nome": "Orcamento prédio Sonia Blade", "valorTotal":15590, "cliente": "Osvaldo de Souza", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 3, "nome": "Orcamento prédio Joaquim nougueira", "valorTotal":35600, "cliente": "Arlindo de Oliveira", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 4, "nome": "Orcamento prédio Girassol", "valorTotal":9800, "cliente": "Maria da Conceição", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 5, "nome": "Orcamento prédio Anchieta", "valorTotal":23000, "cliente": "Mario de Jesus Junior", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 6, "nome": "Orcamento prédio Pombal", "valorTotal":47500, "cliente": "Elaine da Costa", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 7, "nome": "Orcamento prédio Ana Julia", "valorTotal":6500, "cliente":  "Pedro Novaes", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 8, "nome": "Orcamento prédio comercial dos bandeirantes", "valorTotal":18900, "cliente": "Jailto Gonçalves", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 9, "nome": "Orcamento prédio comercial van dublet", "valorTotal":22000, "cliente": "Gabriele Andrade", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 10, "nome": "Orcamento prédio comercial chafuntiformio", "valorTotal":10000, "cliente": "Ana dos Santos", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 11, "nome": "Orcamento prédio João das Neves", "valorTotal":50500, "cliente": "José Bernardes", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 12, "nome": "Orcamento prédio Aramam", "valorTotal":33300, "cliente": "Marcia Oliveira", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 13, "nome": "Orcamento prédio Junqueira de Alencar", "valorTotal":14500, "cliente": "Marcos dos Reis", "statusOrcamento": "pendente"}
                ,{"idOrcamento": 14, "nome": "Orcamento prédio Leonor de Castro", "valorTotal":19400, "cliente": "Ramon Valdez", "statusOrcamento": "pendente"}
                ]

@app.route("/orcamentos", methods=['GET'])
def getListaOrcamento():
    return jsonify(orcamentos)

@app.route("/orcamentos/<int:id>", methods=['GET'])
def getOrcamentoId(id):
    filtro = [e for e in orcamentos if e["idOrcamento"] == id]
    if filtro:
        return jsonify(filtro[0])
    else:
        return jsonify({})

@app.route("/orcamentos", methods=['post'])
def postOrcamento():
    global orcamentos
    try:
        content = request.get_json()

        if content["idOrcamento"] != 0:
            orcamentos.append(content)
        else:
            # gerar id
            ids = [e["idOrcamento"] for e in orcamentos]
            if ids:
                nid = max(ids) + 1
            else:
                nid = 1
            content["idOrcamento"] = nid
            orcamentos.append(content)
        enviarPushOrcamento(content)
        return jsonify({"status":"ok", "msg":"orcamento adicionado com sucesso"})
    except Exception as ex:
        return jsonify({"status":"erro", "msg":str(ex)})

@app.route("/orcamentos/<int:id>", methods=['PUT'])
def putOrcamento(id):
    global orcamentos
    content = request.get_json()

    for orcamento in orcamentos:
        if orcamento["idOrcamento"] == id:
            orcamento["nome"] = content["nome"]
            orcamento["valorTotal"] = content["valorTotal"]
            orcamento["cliente"] = content["cliente"]
            orcamento["statusOrcamento"] = content["statusOrcamento"]

            return jsonify({"status":"OK", "msg":"pedido edidtado com sucesso"})

    return jsonify({"status":"ERRO", "msg": "Erro: não existe pedido com ess Id"})


@app.route("/orcamentos/<int:id>", methods=['DELETE'])
def deleteOrcamento(id):
    global orcamentos
    try:
        orcamentos = [e for e in orcamentos if e["idOrcamento"] != id]
        return jsonify({"status":"OK", "msg":"orcamento removido com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})



def enviarPushOrcamento(orcamento):
    global key
    global token
    data = {
        "to": token,
        "notification" : {
            "title":orcamento["nome"],
            "body":"Você tem um novo orçamento do cliente "+orcamento['cliente']
        },
        "data" : {
            "idOrcamento":orcamento['idOrcamento']
        }
    }
    req = urllib.request.Request('http://fcm.googleapis.com/fcm/send')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'key='+key)
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    print(response)

#################################################################################################
# PEDIDOS

pedidos = [
    {"idPedido": 1, "nomeSolicitante":"Arlindo de Souza", "email":"arlindo.souza@email.com", "telefone": 119563254889, "dtPedido": "20/04/2019", "descricao": "Necessito pintar a fachada de um prédio de 8 andares", "criadoNoApp":0}
    ,{"idPedido": 2, "nomeSolicitante":"Arlete da Costa", "email":"arlete.costa@email.com", "telefone": 11988633256, "dtPedido": "22/04/2019", "descricao": "Necessito fazer a pintura intera de um prédio de 15 andares", "criadoNoApp":0}
    ,{"idPedido": 3, "nomeSolicitante":"Fernanda Barros", "email":"feranda.barros@email.com", "telefone": 11966584122, "dtPedido": "01/05/2019", "descricao": "Necessito pintura interna e externa de um prédio novo de 18 andares", "criadoNoApp":0}
    ,{"idPedido": 4, "nomeSolicitante":"Klaus Thompson", "email":"klaus.thompson@email.com", "telefone": 119563337889, "dtPedido": "04/05/2019", "descricao": "Necessito de uma pintura de um prédio comercial de 25 andares", "criadoNoApp":0}
    ,{"idPedido": 5, "nomeSolicitante":"Juliana Almeida", "email":"juliana.almeida@email.com", "telefone": 11988234257, "dtPedido": "05/05/2019", "descricao": "Necessito de uma pintura completa em um prédio de 7 andares", "criadoNoApp":0}
]

@app.route("/pedidos", methods=['GET'])
def getListaPedidos():
    return jsonify(pedidos)


@app.route("/pedidos/<int:id>", methods=['GET'])
def getPedidoId(id):
    filtro = [e for e in pedidos if e["idPedido"] == id]
    if filtro:
        return jsonify(filtro[0])
    else:
        return jsonify({})


@app.route("/pedidos", methods=['post'])
def postPedido():
    global pedidos
    try:
        content = request.get_json()

        if content["idPedido"] != 0:
            pedidos.append(content)
        else:
            # gerar id
            ids = [e["idPedido"] for e in pedidos]
            if ids:
                nid = max(ids) + 1
            else:
                nid = 1
            content["idPedido"] = nid
            pedidos.append(content)
        if content["criadoNoApp"] == 0:
            enviarPushPedido(content)
        return jsonify({"status":"ok", "msg":"pedido adicionado com sucesso"})
    except Exception as ex:
        return jsonify({"status":"erro", "msg":str(ex)})

@app.route("/pedidos/<int:id>", methods=['PUT'])
def putPedido(id):
    global pedidos
    content = request.get_json()

    for pedido in pedidos:
        if pedido["idPedido"] == id:
            pedido["nomeSolicitante"] = content["nomeSolicitante"]
            pedido["email"] = content["email"]
            pedido["telefone"] = content["telefone"]
            pedido["dtPedido"] = content["dtPedido"]
            pedido["descricao"] = content["descricao"]
            pedido["criadoNoApp"] = content["criadoNoApp"]

            return jsonify({"status":"OK", "msg":"pedido edidtado com sucesso"})

    return jsonify({"status":"ERRO", "msg": "Erro: não existe pedido com ess Id"})



@app.route("/pedidos/<int:id>", methods=['DELETE'])
def deletePedido(id):
    global pedidos
    try:
        pedidos = [e for e in pedidos if e["idPedido"] != id]
        return jsonify({"status":"OK", "msg":"pedido removido com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})


def enviarPushPedido(pedido):
    global key
    global token
    data = {
        "to": token,
        "notification" : {
            "title":"Você tem um novo pedido",
            "body":"Você tem um pedido do cliente "+pedido['nomeSolicitante']
        },
        "data" : {
            "idPedido":pedido['idPedido']
        }
    }
    req = urllib.request.Request('http://fcm.googleapis.com/fcm/send')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'key='+key)
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    print(response)

####################################################################################################################
##################     LOGIN
credenciais = [
    {"usuario":"vini", "senha":"senha"},
    {"usuario":"usuario", "senha":"senha"},
    {"usuario":"teste", "senha":"123"},
    {"usuario":"sppApp", "senha":"senha"},
    ]

@app.route("/login", methods=['post'])
def login():
    global credenciais
    content = request.get_json()

    for credencial in credenciais:
        if content["usuario"] == credencial["usuario"] and content["senha"] == credencial["senha"]:
            return jsonify({"autenticado":"true"})

    return jsonify({"autenticado":"false"})

if __name__ == "__main__":
    app.run()


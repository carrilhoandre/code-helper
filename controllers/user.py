from flask import render_template, jsonify,request
from jinja2 import Environment, FileSystemLoader
import json
import os
from . import routes
import shutil
import hashlib
from pymongo import MongoClient
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)



@routes.route('/user/register', methods=['POST'])
def register():
    user = request.json
    password = hashlib.sha1((user['password']).encode("utf-8")).hexdigest()
    request.json['password'] =  password
    client = MongoClient('mongodb://codehelper:7Noxssci@localhost:27017')
    database = client['codehelper']
    checkIfExists = database.users.find_one({"email":request.json['email']})
    if checkIfExists == None :
        database.users.insert_one(request.json)
        return jsonify("ok")
    else :
        return jsonify("Usuário já existe")

@routes.route('/user/login', methods=['POST'])
def login():
    client = MongoClient('mongodb://codehelper:7Noxssci@localhost:27017')
    database = client['codehelper']
    user = database.users.find_one({"email":request.json['email']})
    if(user["password"] == hashlib.sha1((request.json['password']).encode("utf-8")).hexdigest()) :
        access_token = create_access_token(identity=user["email"])
        return jsonify({"token":access_token}), 200
    else :
        return jsonify("Usuário ou senha incorreto")
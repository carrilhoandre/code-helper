from flask import render_template, jsonify
from jinja2 import Environment, FileSystemLoader
import json
import os
from . import routes
import shutil


@routes.route('/project/generate')
def generate():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    with open('project.json') as f:
        data = json.load(f)

    folders = prepareEnvironment(data)
    generateInfraMongoFiles(env,folders,data)
    generateInfraBusFiles(env,folders,data)

    result = {}
    result["filesCreated"] = 52
    return jsonify(result)
    

def createDirIfNotExists(name):
    if not os.path.exists(name):
        os.makedirs(name)

def prepareEnvironment(data):
    shutil.rmtree("output", ignore_errors=False, onerror=None)
    folders = {}

    folders["apiFolder"] = "output/"+ data["Name"]+"/"+data["Name"]+".Api"
    folders["domainFolder"] = "output/"+ data["Name"]+"/"+data["Name"]+".Domain"
    folders["infraMongoFolder"] = "output/"+ data["Name"]+"/"+data["Name"]+".Infrastructure.MongoDb"
    folders["infraBusFolder"] = "output/"+ data["Name"]+"/"+data["Name"]+".Infrastructure.Bus"

    createDirIfNotExists(folders["apiFolder"])
    createDirIfNotExists(folders["domainFolder"])
    createDirIfNotExists(folders["infraMongoFolder"] + "/Repositories")
    createDirIfNotExists(folders["infraMongoFolder"] + "/Contexts")
    createDirIfNotExists(folders["infraBusFolder"])
    return folders

def generateFile(content, fullPath):
    f = open(fullPath, "x")
    f.write(content)
    f.close()

def generateInfraMongoFiles(env, folders, data):
    generateFile(env.get_template('Infra/Mongo/project.csproj').render(projectName=data["Name"], dotnetVersion = data["DotNetVersion"]),
                 folders["infraMongoFolder"] +"/" +data["Name"]+".Infrastructure.MongoDb.csproj")

    generateFile(env.get_template('Infra/Mongo/Context.cs').render(projectNamespace=data["ProjectNamespace"],databaseName=data["DatabaseName"], dataContext=data["DataContext"]),
                 folders["infraMongoFolder"] +"/Contexts/"+ data["DataContext"] +".cs")

    generateFile(env.get_template('Infra/Mongo/BaseRepository.cs').render(projectName=data["Name"]),
                 folders["infraMongoFolder"] +"/Repositories/BaseRepository.cs")

    for x in data["Entities"]:
        generateFile(env.get_template('Infra/Mongo/Repository.cs').render(className=x["Name"], projectNamespace = data["ProjectNamespace"]),
                 folders["infraMongoFolder"] +"/Repositories/" + x["Name"] + "Repository.cs")

def generateInfraBusFiles(env, folders,data):
    generateFile(env.get_template('Infra/Bus/Bus.csproj').render(projectNamespace=data["ProjectNamespace"], dotnetVersion = data["DotNetVersion"]),
                 folders["infraBusFolder"]  +"/" +data["Name"]+".Infrastructure.Bus.csproj")

    generateFile(env.get_template('Infra/Bus/InMemoryBus.cs').render(projectNamespace=data["ProjectNamespace"]),
                 folders["infraBusFolder"] +"/"+ "InMemoryBus.cs")
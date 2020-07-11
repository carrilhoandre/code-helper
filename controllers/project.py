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
    generateApiFiles(env,folders,data)

    result = {}
    result["filesCreated"] = 52
    return jsonify(result)
    

def createDirIfNotExists(name):
    if not os.path.exists(name):
        os.makedirs(name)

def prepareEnvironment(data):
    if os.path.exists("output"):
        shutil.rmtree("output", ignore_errors=False, onerror=None)
    folders = {}

    folders["apiFolder"] = "output/"+ data["Name"]+"/"+data["Name"]+".Api"
    folders["domainFolder"] = "output/"+ data["Name"]+"/"+data["Name"]+".Domain"
    folders["infraMongoFolder"] = "output/"+ data["Name"]+"/"+data["Name"]+".Infrastructure.MongoDb"
    folders["infraBusFolder"] = "output/"+ data["Name"]+"/"+data["Name"]+".Infrastructure.Bus"

    createDirIfNotExists(folders["apiFolder"] + "/Configurations")
    createDirIfNotExists(folders["apiFolder"] + "/Controllers")
    createDirIfNotExists(folders["apiFolder"] + "/Properties")
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

def generateApiFiles(env, folders,data):

    generateFile(env.get_template('Api/ApiProject.csproj').render(projectNamespace=data["ProjectNamespace"],  dotnetVersion = data["DotNetVersion"]),
                 folders["apiFolder"]  +"/" +data["Name"]+".Api.csproj")

    generateFile(env.get_template('Api/Startup.cs').render(projectNamespace=data["ProjectNamespace"]),
                 folders["apiFolder"]  +"/Startup.cs")

    generateFile(env.get_template('Api/Program.cs').render(projectNamespace=data["ProjectNamespace"]),
                 folders["apiFolder"]  +"/Program.cs")

    generateFile(env.get_template('Api/Dockerfile').render(projectNamespace=data["ProjectNamespace"]),
                 folders["apiFolder"]  +"/Dockerfile")

    generateFile(env.get_template('Api/appsettings.json').render(),
                 folders["apiFolder"]  +"/appsettings.json")
    
    generateFile(env.get_template('Api/appsettings.json').render(),
                 folders["apiFolder"]  +"/appsettings.Development.json")
    
    generateFile(env.get_template('Api/appsettings.json').render(),
                 folders["apiFolder"]  +"/appsettings.Production.json")

    generateFile(env.get_template('Api/SwaggerConfig.cs').render(projectNamespace=data["ProjectNamespace"], author=data["Author"], authorEmail=data["AuthorEmail"]),
                 folders["apiFolder"]  +"/Configurations/SwaggerConfig.cs")

    generateFile(env.get_template('Api/SwaggerFilter.cs').render(projectNamespace=data["ProjectNamespace"]),
                 folders["apiFolder"]  +"/Configurations/SwaggerIgnoreFilter.cs")

    generateFile(env.get_template('Api/launchSettings.json').render(),
                 folders["apiFolder"]  +"/Properties/launchSettings.json")

    generateFile(env.get_template('Api/ApiController.cs').render(projectNamespace=data["ProjectNamespace"]),
                 folders["apiFolder"]  +"/Controllers/ApiController.cs")

    for x in data["Entities"]:
        generateFile(env.get_template('Api/Controller.cs').render(className=x["Name"], projectNamespace = data["ProjectNamespace"], classNameLower=x["Name"].lower() ),
                  folders["apiFolder"]  +"/Controllers/" + x["Name"] + "Controller.cs")

        
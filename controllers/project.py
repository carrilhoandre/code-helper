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
        project = json.load(f)
    


    folders = prepareEnvironment(project)
    #generateInfraMongoFiles(env,folders,project)
    #generateInfraBusFiles(env,folders,project)
    #generateApiFiles(env,folders,project)
    #generateDomainFiles(env,folders,project)

    with open('templates.json') as f:
        templates = json.load(f)

    filesCreated = 0
    for t in templates["BaseFileTemplates"]:
        parameters = {}
        for p in t["Parameters"]:
            parameters[p["Name"]] = project[p["Name"]]
        
        generateFile(env.get_template(t["TemplateFile"]).render(parameters),
                 folders[t["Type"]+ "Folder"] + "/" + t["OutputPath"])
        
        filesCreated = filesCreated + 1

    result = {}
    result["filesCreated"] = filesCreated
    return jsonify(result)
    

def createDirIfNotExists(name):
    if not os.path.exists(name):
        os.makedirs(name)

def prepareEnvironment(project):
    if os.path.exists("output"):
        shutil.rmtree("output", ignore_errors=False, onerror=None)
    folders = {}

    folders["apiFolder"] = "output/"+ project["Name"]+"/"+project["Name"]+".Api"
    folders["domainFolder"] = "output/"+ project["Name"]+"/"+project["Name"]+".Domain"
    folders["infraMongoFolder"] = "output/"+ project["Name"]+"/"+project["Name"]+".Infrastructure.MongoDb"
    folders["infraBusFolder"] = "output/"+ project["Name"]+"/"+project["Name"]+".Infrastructure.Bus"

    createDirIfNotExists(folders["apiFolder"] + "/Configurations")
    createDirIfNotExists(folders["apiFolder"] + "/Controllers")
    createDirIfNotExists(folders["apiFolder"] + "/Properties")
    createDirIfNotExists(folders["domainFolder"]+ "/Entities")
    createDirIfNotExists(folders["domainFolder"]+ "/Commands/Handlers")
    createDirIfNotExists(folders["domainFolder"]+ "/Commands/Inputs/Shared")
    createDirIfNotExists(folders["domainFolder"]+ "/Commands/Validations/Shared")
    createDirIfNotExists(folders["domainFolder"]+ "/Events")
    createDirIfNotExists(folders["domainFolder"]+ "/Repositories")
    createDirIfNotExists(folders["domainFolder"]+ "/Results")
    createDirIfNotExists(folders["domainFolder"]+ "/Enums")
    createDirIfNotExists(folders["infraMongoFolder"] + "/Repositories")
    createDirIfNotExists(folders["infraMongoFolder"] + "/Contexts")
    createDirIfNotExists(folders["infraBusFolder"])
    return folders

def generateFile(content, fullPath):
    f = open(fullPath, "x")
    f.write(content)
    f.close()

def generateDomainFiles(env, folders, project):
    generateFile(env.get_template('Domain/IBaseRepository.cs').render(projectNamespace = project["ProjectNamespace"]),
                 folders["domainFolder"] +"/Repositories/IBaseRepository.cs")
    generateFile(env.get_template('Domain/DeleteCommand.cs').render(projectNamespace = project["ProjectNamespace"]),
                 folders["domainFolder"] +"/Commands/Inputs/Shared/DeleteCommand.cs")
    generateFile(env.get_template('Domain/DeleteValidation.cs').render(projectNamespace = project["ProjectNamespace"]),
                 folders["domainFolder"] +"/Commands/Validations/Shared/DeleteValidation.cs")
    for x in project["Entities"]:
        generateFile(env.get_template('Domain/Entity.cs').render(className=x["Name"], projectNamespace = project["ProjectNamespace"],classType=x["Type"], fields = x["Fields"]),
                 folders["domainFolder"] +"/Entities/" + x["Name"] + ".cs")
        if x["InheritanceClass"]=="":
            generateFile(env.get_template('Domain/IRepository.cs').render(className=x["Name"], plural= x["Plural"], projectNamespace = project["ProjectNamespace"]),
                         folders["domainFolder"] +"/Repositories/I" + x["Name"] + "Repository.cs")
        if x["Type"]=="Class":
            generateFile(env.get_template('Domain/Handler.cs').render(className=x["Name"], plural= x["Plural"], projectNamespace = project["ProjectNamespace"]),
                         folders["domainFolder"] +"/Commands/Handlers/" + x["Name"] + "Handler.cs")
            createDirIfNotExists(folders["domainFolder"] +"/Commands/Inputs/" + x["Plural"])
            generateFile(env.get_template('Domain/CommandBase.cs').render(className=x["Name"], plural= x["Plural"], projectNamespace = project["ProjectNamespace"]),
                         folders["domainFolder"] +"/Commands/Inputs/"+ x["Plural"] + "/" + x["Name"] + "Command.cs")
            generateFile(env.get_template('Domain/Command.cs').render(className=x["Name"], plural= x["Plural"], projectNamespace = project["ProjectNamespace"], type = "Create"),
                         folders["domainFolder"] +"/Commands/Inputs/"+ x["Plural"] + "/Create" + x["Name"] + "Command.cs")
            generateFile(env.get_template('Domain/Command.cs').render(className=x["Name"], plural= x["Plural"], projectNamespace = project["ProjectNamespace"], type = "Update"),
                         folders["domainFolder"] +"/Commands/Inputs/"+ x["Plural"] + "/Update" + x["Name"] + "Command.cs")
            
            createDirIfNotExists(folders["domainFolder"] +"/Commands/Validations/" + x["Plural"])
            generateFile(env.get_template('Domain/ValidationBase.cs').render(className=x["Name"], plural= x["Plural"], projectNamespace = project["ProjectNamespace"]),
                         folders["domainFolder"] +"/Commands/Validations/"+ x["Plural"] + "/" + x["Name"] + "Validation.cs")
            generateFile(env.get_template('Domain/Validation.cs').render(className=x["Name"], plural= x["Plural"], projectNamespace = project["ProjectNamespace"], type = "Create"),
                         folders["domainFolder"] +"/Commands/Validations/"+ x["Plural"] + "/Create" + x["Name"] + "Validation.cs")
            generateFile(env.get_template('Domain/Validation.cs').render(className=x["Name"], plural= x["Plural"], projectNamespace = project["ProjectNamespace"], type = "Update"),
                         folders["domainFolder"] +"/Commands/Validations/"+ x["Plural"] + "/Update" + x["Name"] + "Validation.cs")

    for e in project["Enums"]:
        generateFile(env.get_template('Domain/Enum.cs').render(className=e["Name"], projectNamespace = project["ProjectNamespace"], values = e["Values"]),
                 folders["domainFolder"] +"/Enums/" + e["Name"] + ".cs")        

def generateInfraMongoFiles(env, folders, project):
    generateFile(env.get_template('Infra/Mongo/project.csproj').render(projectName=project["Name"], dotnetVersion = project["DotNetVersion"]),
                 folders["infraMongoFolder"] +"/" +project["Name"]+".Infrastructure.MongoDb.csproj")

    generateFile(env.get_template('Infra/Mongo/Context.cs').render(projectNamespace=project["ProjectNamespace"],projectbaseName=project["DatabaseName"], projectContext=project["DataContext"]),
                 folders["infraMongoFolder"] +"/Contexts/"+ project["DataContext"] +".cs")

    generateFile(env.get_template('Infra/Mongo/BaseRepository.cs').render(projectName=project["Name"]),
                 folders["infraMongoFolder"] +"/Repositories/BaseRepository.cs")

    for x in project["Entities"]:
        if x["InheritanceClass"]=="":
            generateFile(env.get_template('Infra/Mongo/Repository.cs').render(className=x["Name"], projectNamespace = project["ProjectNamespace"]),
                 folders["infraMongoFolder"] +"/Repositories/" + x["Name"] + "Repository.cs")

def generateInfraBusFiles(env, folders,project):
    generateFile(env.get_template('Infra/Bus/Bus.csproj').render(projectNamespace=project["ProjectNamespace"], dotnetVersion = project["DotNetVersion"]),
                 folders["infraBusFolder"]  +"/" +project["Name"]+".Infrastructure.Bus.csproj")

    generateFile(env.get_template('Infra/Bus/InMemoryBus.cs').render(projectNamespace=project["ProjectNamespace"]),
                 folders["infraBusFolder"] +"/"+ "InMemoryBus.cs")

def generateApiFiles(env, folders,project):

    generateFile(env.get_template('Api/ApiProject.csproj').render(projectNamespace=project["ProjectNamespace"],  dotnetVersion = project["DotNetVersion"]),
                 folders["apiFolder"]  +"/" +project["Name"]+".Api.csproj")

    generateFile(env.get_template('Api/Startup.cs').render(projectNamespace=project["ProjectNamespace"]),
                 folders["apiFolder"]  +"/Startup.cs")

    generateFile(env.get_template('Api/Program.cs').render(projectNamespace=project["ProjectNamespace"]),
                 folders["apiFolder"]  +"/Program.cs")

    generateFile(env.get_template('Api/Dockerfile').render(projectNamespace=project["ProjectNamespace"]),
                 folders["apiFolder"]  +"/Dockerfile")

    generateFile(env.get_template('Api/appsettings.json').render(),
                 folders["apiFolder"]  +"/appsettings.json")
    
    generateFile(env.get_template('Api/appsettings.json').render(),
                 folders["apiFolder"]  +"/appsettings.Development.json")
    
    generateFile(env.get_template('Api/appsettings.json').render(),
                 folders["apiFolder"]  +"/appsettings.Production.json")

    generateFile(env.get_template('Api/SwaggerConfig.cs').render(projectNamespace=project["ProjectNamespace"], author=project["Author"], authorEmail=project["AuthorEmail"]),
                 folders["apiFolder"]  +"/Configurations/SwaggerConfig.cs")

    generateFile(env.get_template('Api/SwaggerFilter.cs').render(projectNamespace=project["ProjectNamespace"]),
                 folders["apiFolder"]  +"/Configurations/SwaggerIgnoreFilter.cs")

    generateFile(env.get_template('Api/launchSettings.json').render(),
                 folders["apiFolder"]  +"/Properties/launchSettings.json")

    generateFile(env.get_template('Api/ApiController.cs').render(projectNamespace=project["ProjectNamespace"]),
                 folders["apiFolder"]  +"/Controllers/ApiController.cs")

    for x in project["Entities"]:
        if x["Type"] != "abstract class":
            generateFile(env.get_template('Api/Controller.cs').render(className=x["Name"], projectNamespace = project["ProjectNamespace"], classNameLower=x["Name"].lower() ),
                  folders["apiFolder"]  +"/Controllers/" + x["Name"] + "Controller.cs")

        
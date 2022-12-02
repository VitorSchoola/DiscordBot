import pymongo
import datetime


def connect(dbUsr, dbPss, dbName):
    client = pymongo.MongoClient(
        f"mongodb+srv://{dbUsr}:{dbPss}@{dbName}.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client.TrashVariables
    return db


def addToDb(db, name, variable, variableTag='Name'):
    post = {
        variableTag: name,
        "Variable": variable,
        "date": datetime.datetime.now()
    }
    posts = db.posts
    posts.insert_one(post).inserted_id
    print(f'\tSaved variable: {variableTag} : {post[variableTag]}')


def deleteFromDb(db, name, variableTag='Name'):
    posts = db.posts
    query = {variableTag: name}
    print(f"\tTrying to delete post: {query}")
    if (posts.find_one(query) is not None):
        posts.delete_one(query)
        print('\t\t> Successfuly deleted post.')
        return 0
    else:
        print(f"\t\t> No such variable: {query[variableTag]}")
        return 1


def getVarFromDb(db, name, variableTag='Name'):
    posts = db.posts
    query = {variableTag: name}
    user = posts.find_one(query)
    if (user is not None):
        print("\tDownloading variable:", query[variableTag])
        return user
    else:
        print("\tNo such variable:", query[variableTag])
        return None
    return None

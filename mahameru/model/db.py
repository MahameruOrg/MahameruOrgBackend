import click
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson.son import SON
from bson.json_util import dumps
from bson.objectid import ObjectId

def get_db():
    mongocon = current_app.config['MONGO_CON']
    dbclient = pymongo.MongoClient(mongocon)
    g.db = dbclient[current_app.config['DATABASE']]
    return g.db

def get_collection(colname):
    if 'db' not in g:
        get_db()
    return g.db[colname]

def get_chat_collection():
    col = get_collection("chat")
    pipeline = [ {"$lookup" : {"from" : "user", "localField" : "to_user", "foreignField" : "_id", "as": "chat_details" } }]
    data = col.aggregate(pipeline)
    current_app.logger.debug(data)
    return data

"""
Helper function to query all contact on system 
"""
def get_contact(filter={}):
    collection = get_collection("contact")
    return collection.find(filter)

def get_contact(filter={}):
    collection = get_collection("contact")
    return collection.find_one(filter)

def insert_contact(data):
    collection = get_collection("contact")
    row = collection.insert_one(data)
    return row

def update_contact(filter, update):
    collection = get_collection("contact")    
    return collection.update_one(filter, update, upsert=False)    

def delete_contact(data):
    collection = get_collection("contact")
    collection.delete_one(data)

def get_user(filter={}):
    collection = get_collection("user")
    return collection.find(filter)

def get_user(filter={}):
    collection = get_collection("user")
    return collection.find_one(filter)

def insert_user(data):
    collection = get_collection("user")
    row = collection.insert_one(data)
    return row

def update_user(filter, update):
    collection = get_collection("user")    
    return collection.update_one(filter, update, upsert=False)    

def delete_user(data):
    collection = get_collection("user")
    row = collection.delete_one(data)
    return row


#def close_db(e=None):
    #db = g.pop(current_app.config['DATABASE'], None)
    #if db is not None:
        #db.close()
        
def init_db():
    """clear the existing data and create new tables."""    
    db = get_db()    
    db.client.drop_database(current_app.config['DATABASE'])
    
@click.command('init-db')
@with_appcontext
def init_db_command():    
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    #app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


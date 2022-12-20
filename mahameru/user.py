from flask import Blueprint, render_template, abort, request, jsonify
from jinja2 import TemplateNotFound
from .model.db_user import *
from bson.json_util import dumps
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime

bp = Blueprint('user', __name__,
                        template_folder='templates')

'''
    Feedback : 
    1. Check database diagram, field yg wajib diisi
    2. Untuk route ini pada key created_at dan updated_at digenerate oleh sistem
    '''

@bp.route('/createuser', methods=['POST']) # KELAR
def add_user():
    form = request.form
    user = {}
    user["name"] = form['name']
    user["nickname"] = form['nickname']
    user["notelp"] =form['notelp']
    user["pin"] = form['pin']
    user["createdate"] = datetime.datetime.now() #konversi string ke timestamp
    user["contactid"] = form['contact_id'] #jadikan objectid dari contact

    if request.method == "POST" and form['name']:
        _id = insert_user(user)
        resp = dumps(_id)
        current_app.logger.debug(_id)
        return resp
    else:
        return "Unable to store data into database"


'''
    Feedback : 
    1. Check database diagram, field yg wajib diisi
    2. Untuk route ini pada key created_at dan updated_at digenerate oleh sistem
    3. Akses ke database untuk simpan data seharusnya dipisahkan kedalam file terpisah
    4. Konfiguras baca dari settings.cfg
    5. Pada kondisi " if " pastikan checking kondisinya benar
    6. Kembalikan ObjectID untuk row yang berhasil di update sebagai json
    7. Nama route ubah ke updateuser untuk mencerminkan tujuan
    8. Field updated_at ditarik dari datesystem tanpa menyentuh existing data di field created_at
    
'''

@bp.route('/updateuser/<id>', methods = ['PUT'])
def updateuser(id): # kelar
    form = request.form
    user = {}
    user["name"] = form['name']
    user["nickname"] = form['nickname']
    user["notelp"] =form['notelp']
    user["pin"] = form['pin']
    user["updatedate"] = datetime.datetime.now() # konversi string ke timestamp
    #user["contactid"] = form['contact_id']

    #current_app.logger.debug(id)


    if form['name']:
        _id = update_users(id, user) # db_user belum benar
        resp = dumps(_id)
        #current_app.logger.debug(_id)
        return resp
        #return
    else:
        return "Failed to update user"


'''
    Feedback :
    1. nama route ganti ke /users
    2. Jika tidak ada user yg ditemukan, kembalikan string "Tidak ada user"
'''

@bp.route('/users') #tampilin user (kelar)
def user_all():
    user = get_user()#buat route baru tipr "GET" yang mengembalikan seluruh kontak untuk user yang login sekarang (join 3 table : user, user.contact dan user)      
    resp = dumps(user)
    return resp

'''
    Feedback :
    1. Jika tidak ada user yg ditemukan, kembalikan string "Tidak ada user dengan objectID yang dicari"
'''

@bp.route('/user/<id>') # tampilin user sesuai dengan user ID
def user_one(id):
    user = get_user_wID(id)
    resp = dumps(user)
    return resp


'''
    Feedback :
    1. Nama route ganti ke /deleteuser
    2. check filter query delete row karena row yang diingikan tidak terhapus
'''
@bp.route('/deleteuser/<id>',methods=['DELETE']) # hapus user sesuai dengan user ID
def deleteuser(id):
    user = delete_user(id)
    resp = dumps(user)
    return resp
from app import app
from flask import render_template,request,url_for,redirect,flash
from pymongo import MongoClient
import time
from os import environ
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(environ.get("MONGODB-URI"))
db = client.flask.deyal

@app.route('/',methods=["GET"])
def index():
    items = list(db.find())
    return render_template("index.html",items=items)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/write/',methods=["POST","GET"])
def write():
    if request.method == "POST":
        data = {"post":request.form["writebox"],
                "time":time.asctime(time.localtime(time.time())),
                "author":request.form["author"] or "anonymous"
        }
        secret = str(db.insert_one(data).inserted_id)
        flash(f"Message Added, secret is {secret}.")
        return redirect(url_for('write'))
    return render_template('write.html')

@app.route('/edit/',methods=["POST","GET"])
def mainedit():
    if request.method == "POST":
        return redirect(url_for('mainedit') + request.form['secret'])
    return render_template("edit.html")

@app.route('/edit/<secret>',methods=["POST","GET"])
def edit(secret):
    if request.method == "GET":
        try:
            secret = ObjectId(secret)
        except Exception as e:
            print(e)
        data = db.find_one({'_id':secret})
        if data == None:
            return "Noice"
        return render_template('edit.html',data=data)
    elif request.method == "POST":
        data = db.find_one({"_id":ObjectId(secret)})
        data['post'] = request.form['writebox']
        data['author'] = request.form['author'] or anonymous
        db.update_one({'_id':ObjectId(secret)},
                {"$set":data}
                )
        flash("Updated Message.")
        return redirect(url_for('write'))

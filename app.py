from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId

client=MongoClient('mongodb+srv://tapusahamnb:fjdaZM74M9xbAzY5@cluster0.4hpeghp.mongodb.net/')
db=client["form"]
collection=db["USL"]
credentials_collection = db["credentials"]

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/submit',methods=["GET","POST"])
def submit():  # put application's code here
    name = request.form["name"]
    email = request.form["email"]
    gender = request.form["gender"]
    dob = request.form["dob"]
    massage = request.form["massage"]
    collection.insert_one({"Name":name, "Massage": massage, "Email":email, "Gender":gender, "Date of Birth":dob})
    return render_template("board.html")


@app.route('/admin', methods=["GET",'POST'])
def admin():
    return render_template("admin.html")

@app.route('/login', methods=["GET","POST"])
def login():
    Email = request.form["Email"]
    Password = request.form["Password"]
    user = credentials_collection.find_one({'Email': Email,'Password': Password})
    if user:
        data =collection.find()
        return render_template("test.html",data=data)
    else:
        return render_template("index.html")


@app.route('/update/<string:item_id>', methods=["POST"])
def update(item_id):
        name = request.form.get("name")
        email = request.form.get("email")
        gender = request.form.get("gender")
        dob = request.form.get("dob")
        collection.update_one({"_id": ObjectId(item_id)}, {"$set": {"Name": name, "Email": email, "Gender": gender, "Date of Birth": dob}})
        return render_template('test.html',data=collection.find())



if __name__ == '__main__':
    app.run()

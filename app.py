from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import(
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
import os
from dotenv import load_dotenv
load_dotenv()
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URL")
#secret key used to sign JWT tokens
app.config['JWT_SECRET_KEY']=os.getenv("JWT_KEY")

jwt=JWTManager(app)
db=SQLAlchemy(app)
@app.route("/",methods=["POST"])
@app.route("/register",methods=["POST"])
def register():
    data=request.get_json()
    username=data["username"]   
    password=data["password"]
    user=User(username=username,password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "username":username,
        "password":password,
        "message":"User registered successfully"
    })
@app.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    username=data["username"]
    password=data["password"]
    #fetch user
    user=User.query.filter_by(
        username=username
    ).first()
    if not user:
         return jsonify({
            "message":"User not found"
         }),404
    if user.password!=password:
        return jsonify({
            "message":"Invalid password"

        }),404
    access_token=create_access_token(identity=str(user.id))
    return jsonify({
        "access_token":access_token
    })
#protected route
@app.route("/profile")
@jwt_required()
def profile():
    current_user_id=get_jwt_identity()
    user=User.query.get(int(current_user_id))
    return jsonify({
        "id":user.id,
        "username":user.username
    })

@app.route("/hello",methods=["POST"])
def hello():
    return jsonify({
               "id": 1,
        "username": "alice",
        "email": "alice@gmail.com"
    })
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(100),nullable=False)

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
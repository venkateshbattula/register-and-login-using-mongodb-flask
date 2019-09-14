import re
from time import strftime

from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_pymongo import MongoClient, PyMongo
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
client = MongoClient('localhost')

app.config['MONGO_DBNAME'] = 'dbname'
app.config['MONGO_URI'] = 'mongodb://localhost/dbname'
app.config['JWT_SECRET_KEY'] = 'keyvalue'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'samplemail@gmail.com'
app.config['MAIL_PASSWORD'] = 'mailpassword'
app.config['MAIL_DEFAULT_SENDER'] = 'default_sender_email'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['DEBUG'] = True
app.secret_key = 'my secret key'
app.config['MAIL_ASCII_ATTACHMENTS'] = True
app.config['SESSION_USE_SIGNER'] = True

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

s = URLSafeTimedSerializer('12345')
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)

CORS(app)

@app.route('/send_mail', methods=['POST'])
def email_send():
    email_id = request.json['email_id']
    msg = Message('message', sender="samplemail@gmail.com", recipients=[email_id])
    msg.body = 'message'
    mail.send(msg)

@app.route('/register',methods=['POST'])
def register():
    db = client.dbname
    coll = db.users
    try:
        fullname = request.json['fullname']
        try:
            email_id = request.json['email_id']
        except KeyError:
            email_id = ""
        password = request.json['password']
        confirm_password = request.json['confirm_password']
        sms_key= request.json['sms_key']
        if password != confirm_password:
            return "Passwords do not match. try again"
        mobile_number = request.json['mobile_number']
        created_time = strftime("%Y/%m/%d %H:%M:%S %I%p")
        try:
            msg = Message('message', sender="samplemail@gmail.com", recipients=[email_id])
            msg.body = 'message'
            mail.send(msg)
        except:
            pass
        user_id_list = [i['user_id'] for i in coll.find()]
        if len(user_id_list) is 0:
            user_id = 1
        else:
            user_id = int(user_id_list[-1]) + 1
        er = coll.find({'email_id': email_id})
        mr = coll.find({'mobile_number': mobile_number})
        for m in mr:
            if m['mobile_number'] == mobile_number:
                return "Seems like you have already registered wth us.Please login to continue"

        if re.match(pattern=r'(^(0/91))?([0-9]{10}$)', string=mobile_number):  # check for mobilenumber properly
            if re.match(r'[A-Za-z0-9@#$%^&+=]{6,12}', password):  # check for password properly
                output = []
                coll.insert(
                            {'fullname': fullname, 'email_id': email_id, 'password': password,
                             'confirm_password': confirm_password, 'user_id': user_id,
                             'mobile_number': mobile_number, 'created_time': created_time, 'sms_key': sms_key})
                output.append({'fullname': fullname, 'email_id': email_id, 'password': password,
                             'confirm_password': confirm_password, 'user_id': user_id,
                             'mobile_number': mobile_number, 'created_time': created_time, 'sms_key': sms_key})
                return jsonify({'status': 'success', 'message': 'User is registered', 'result': output})
            else:
                return jsonify({'status': 'failure', 'message': 'Invalid Password.'})
        else:
            return jsonify({'status': 'failure', 'message': 'Invalid Mobile Number'})

    except Exception as e:
        return jsonify({'status': 'Fail', 'message': str(e), 'result': 'Unable to register. Please try again'})


if __name__ == '__main__':
    app.run(debug=True)
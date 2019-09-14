from flask import request, jsonify, app
from flask_jwt_extended import create_access_token

from applicationtest import client


@app.route('/login', methods=['POST'])
def login():
    db = client.dbname
    coll = db.users
    username = request.json['username']
    password = request.json['password']
    try:
        access_token = create_access_token(identity=username)
        details = coll.find({'mobile_number': username, 'password': password})
        info = coll.find({'email_id': username, 'password': password})
        output = []
        for j in details:
            try:
                user_pic = j['user_pic']
            except KeyError:
                user_pic = "None"
            output.append({'user_id': j['user_id'], 'fullname': j['fullname'], 'email_id': j['email_id'],
                           'mobile_number': j['mobile_number'],
                           'created_time': j['created_time'], 'user_pic': user_pic})
        for i in info:
            try:
                user_pic = i['user_pic']
            except KeyError:
                user_pic = "None"
            output.append({'user_id': i['user_id'], 'fullname': i['fullname'], 'email_id': i['email_id'],
                           'mobile_number': i['mobile_number'],
                           'created_time': i['created_time'], 'user_pic': user_pic})
        finaloutput = {}
        if len(output) != 0:
            finaloutput['status'] = 'success'
            finaloutput['message'] = 'login Successful'
            finaloutput['result'] = output
            finaloutput['token'] = access_token
        else:
            finaloutput['status'] = 'failure'
            finaloutput['message'] = 'Invalid Credentials. Please check and try again'
            finaloutput['result'] = []
        return jsonify(finaloutput)
    except Exception as e:
        return jsonify({'status': 'fail', 'result': str(e), 'message': 'Unable to login, Please try again'})


if __name__ == '__main__':
    app.run(debug=True)
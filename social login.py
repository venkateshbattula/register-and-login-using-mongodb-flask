from flask import jsonify, request, app

from applicationtest import client


@app.route('/social_login', methods=['POST'])
def social_login():
    result = []
    fullname = request.json['fullname']
    email_id = str(request.json['email_id'])
    googleid = request.json['googleid']
    facebookid = request.json['facebookid']
    profile_pic = request.json['profile_pic']
    created_time = dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S %I%p")
    db = client.dbname
    coll = db.users
    if googleid != "":
        q = coll.find_one({'googleid': googleid})
    elif facebookid != "":
        q = coll.find_one({'facebookid': facebookid})
    if(q!= None) and (googleid != "" or facebookid != ""):
        user_id = None
        temp_dict = {}
        temp_dict['user_id'] = q['user_id']
        user_id = q['user_id']
        temp_dict['fullname'] = q['fullname']
        temp_dict['email_id'] = q['email_id']
        if googleid != "":
            temp_dict['googleid'] = q['googleid']
        elif facebookid != "":
            temp_dict['facebookid'] = q['facebookid']
        result.append(temp_dict)
        return jsonify({"status": "success", "message": "Login Successful", "result": result})

    else:
        data = coll.find({'email_id': email_id})
        user_id = [i['user_id'] for i in coll.find()]
        if len(user_id) is 0:
            user_id = 1
        else:
            user_id = int(str(user_id[-1])) + 1
        if data.count() != 0:
            return jsonify({'status': 'failure', 'message': 'User is already registered'})
        elif googleid != "":
            coll.insert({'user_id': user_id, 'fullname': fullname, 'email_id': email_id, 'facebookid': facebookid, 'googleid': googleid, 'profile_pic': profile_pic,
                         'created_time': created_time})
            q = coll.find_one({'googleid': googleid})
        elif facebookid != "":
            coll.insert({'user_id': user_id, 'fullname': fullname, 'email_id': email_id, 'facebookid': facebookid, 'googleid': googleid, 'profile_pic': profile_pic,
                         'created_time': created_time})
            q = coll.find_one({'facebookid': facebookid})
        temp_dict = {}
        temp_dict['user_id'] = q['user_id']
        temp_dict['fullname'] = q['fullname']
        temp_dict['email_id'] = q['email_id']
        if googleid != "":
            temp_dict['googleid'] = q['googleid']
        elif facebookid != "":
            temp_dict['facebookid'] = q['facebookid']
        result.append(temp_dict)
        return jsonify({"status": "success", "message": "user registered", "result": result})

if __name__ == '__main__':
    app.run(debug=True)
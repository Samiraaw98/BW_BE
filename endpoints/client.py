from app import app 
from helpers.db_helpers import run_query 
from flask import  request, jsonify
import uuid

@app.get('/api/client')
def client_get():
    client_list = run_query("SELECT * FROM client")
    resp = []
    for client in client_list:
        cl = {}
        cl ['id'] = client[0]
        cl['email'] = client[1]
        cl['username'] = client[2]
        cl['password'] = client[3]
        cl['first_name'] = client[4]
        cl['last_name'] = client[5]
        cl['birthday'] = client[6]
        cl['created_at'] = client[7]
        cl['bio'] = client[8]
        cl['picture_url'] = client[9]
        resp.append(cl)
    return jsonify(resp) , 200


@app.post('/api/client')
def client_post():
    # grabbing data
    data = request.json
    id=data.get('id')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birthday = data.get('birthday')
    created_at = data.get('created_at')
    bio = data.get('bio')
    picture_url = data.get('pictureUrl')

    if not email  :
        return jsonify ("Missing required argument : email / username"), 422 
    if not username:
        return jsonify("Missing required argument : username"), 422
    if not password :
        return jsonify ("Missing required argument : password") , 422
    if not first_name:
        return jsonify ("Missing required argument : first_name") , 422
    if not birthday:
        return jsonify("Missing DOB, please try again"),422

    result= run_query("INSERT INTO client (email,username, password,first_name, last_name,birthday, created_at,bio,picture_url) VALUES (?,?,?,?,?,?,?,?,?)", [email, username, password, first_name, last_name,birthday,created_at,bio,picture_url])
    token = str(uuid.uuid4())
    run_query("INSERT INTO client_session(client_id , token) VALUES (?,?)", [result,token])
    return jsonify ("Client added") , 201 

@app.patch('/api/client')
def client_patch():
        data = request.json
        id = data.get('id')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        token = data.get('token')
        picture_url = data.get('pictureUrl')
        bio = data.get('bio')



        # if password == None and token == None:
        print(id)
        session=run_query("SELECT token FROM client_session WHERE client_id=?",[id])[0][0]
        auth = run_query("SELECT * FROM client WHERE email = ?", [email])
        print(session)
        if token == session and username ==auth:
            run_query("UPDATE client SET username = ? WHERE email = ?" , [username,email])
            return jsonify("username updated"), 200
        if token == session and  first_name == auth:
            run_query("UPDATE client SET first_name =? WHERE email = ?", [first_name, email])
            return jsonify("firstname updated"), 200
        if token == session and last_name == auth:
            run_query("UPDATE client SET last_name = ? WHERE email = ?" , [last_name,email])
            return jsonify("lastName updated"), 200
        if token == session and password == auth:
            run_query("UPDATE client SET password = ? WHERE email = ?" , [password,email])
            return jsonify("password updated"), 200
        if token == session and picture_url == auth:
            run_query("UPDATE client SET picture = ? WHERE email = ?" , [picture_url,email])
            return jsonify("profile picture updated"), 200
        if token == session and bio == auth:
            run_query("UPDATE client SET bio = ? WHERE email = ?" , [bio,email])
            return jsonify("bio updated"), 200
        

@app.delete('/api/client')
def client_delete():
    data=request.json
    password=data.get('password')
    email = data.get('email')
    token = data.get('token')
    id = data.get('id')
    client_id = data.get('client_id')


    result = run_query("SELECT client_id,token,email FROM client INNER JOIN client_session ON client_session.client_id = client.id WHERE email =? and token=? ", [email,token])
    if result == email or token :
        run_query("DELETE FROM client_session WHERE token =?", [token])
        run_query("DELETE FROM client WHERE email =? ", [email])
        return jsonify("Client deleted"), 200



        #     query = []
        #     parents = []
        #     if password :
        #         query.append("password=?")
        #         parents.append(password)
        #     if username:
        #         query.append("username=?")
        #         parents.append(username)
        #         # run_query("UPDATE client SET password = ? WHERE email = ?" , [password,email])
        #         # return jsonify('password updated'), 200
        #     if first_name:
        #         query.append("first_name=?")
        #         parents.append(first_name)
        #     if last_name:
        #         query.append("last_name=?")
        #         parents.append(last_name)
        #     if query:
        #         parents.append(email)
        #         run_query("UPDATE client SET {} WHERE email=?".format(",".join(query)) , parents)
        #         return jsonify(' updated'), 200
                
        #     else:
        #         return jsonify("Nothing to update"),401
        # else:
        #     return jsonify("token is not correct"), 401
            
        #     return jsonify("Wrong password, please try again"),401
        # result = run_query("SELECT token,first_name ,last_name,  email,password ,picture_url FROM client INNER JOIN client_session ON client_session.client_id = client.id WHERE email=? and token=?" , [email, token])

        # if result ==  email  or token:
        #     run_query("UPDATE client SET password = ? WHERE email = ?" , [password,email])
        #     return jsonify("password updated"),200

        # if result == username  or token :
        #     run_query("UPDATE client SET username=? WHERE email=?",[username,email])
        #     return jsonify("username updated"), 200

        # if result == first_name or token:
        #     run_query("UPDATE client SET first_name =? WHERE email =?", [first_name,email])
        #     return jsonify("firstName updated"),200

        # if result == last_name or token:
        #     run_query("UPDATE client SET last_name=? WHERE email = ?", [last_name,email])
        #     return jsonify("last name updated"),200

        # if result == picture_url or token:
        #     run_query("UPDATE client SET picture_url WHERE email= ?", [picture_url,email])
        #     return jsonify("picture updated"),200
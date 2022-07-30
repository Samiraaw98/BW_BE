from asyncio import run
from app import app 
from helpers.db_helpers import run_query
from flask import  request, jsonify
import uuid

@app.post('/api/client-login')
def user_post():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    session = run_query("SELECT * FROM client INNER JOIN client_session ON client_session.client_id = client.id WHERE email =? and password=? ",[email,password])
    print(session)

    if session == email or password:
        token = str(uuid.uuid4())
        run_query("INSERT INTO client_session(token) VALUES(?) ",[token])
        return jsonify ("success"),200    
    else:
        return jsonify("error,user may not exist"),420

    

        
    #     if result == email:
    #         token = str(uuid.uuid4())
    #         run_query("INSERT INTO client_session(client_id,token)VALUES(?,?)",[result,token])
    #         return jsonify ("success"),200
    # else:
    #     return jsonify("error,user may not exist "),422




        #  run_query("SELECT id FROM client where email=? and password=?",[email,password])

    # check=run_query("SELECT id FROM client where email=? and password=?",[email,password])
    # if check == email  :
        # token= str(uuid.uuid4())
        # run_query("INSERT INTO client_session(client_id,token) VALUES (?,?) ",[check,token ])
        # return jsonify ("success"),200

@app.delete('/api/client-logout')
def user_delete():
    data = request.json
    token = data.get('token')
    if token!=None:
        run_query("DELETE FROM client_session WHERE token=?", [token])
    return jsonify("logged out"),200


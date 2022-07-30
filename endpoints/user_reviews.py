from app import app 
from helpers.db_helpers import run_query 
from flask import  request, jsonify

@app.get('/api/reviews')
def reviews_get():
    # join with user
    # client = run_query("SELECT reviews.id,content ")
    review_list = run_query("SELECT * FROM client")
    resp = []
    for review in review_list:
        rv = {}
        rv ['id'] = review[0]
        rv ['content'] = review[1]
        rv ['client_id'] = review[2]
        rv ['created_at'] = review[3]
        resp.append(rv)
    return jsonify(resp),200

@app.post('/api/reviews')
def reviews_post():
    #grabbing data
    data = request.json
    content= data.get('content')
    client_id= data.get('client_id')
    token = data.get('token')

    auth = run_query("SELECT client_id FROM client_session WHERE token=?",[token])
    print(auth)
    run_query("INSERT INTO reviews (content, client_id) VALUES(?,?)",[content,auth])
    return jsonify("comment added"), 201
   


@app.patch('/api/reviews')
def reviews_patch():
    data=request.json
    token = data.get('token')
    content = data.get('content')
    id= data.get('id')

    auth = run_query("SELECT client_id FROM client_session WHERE token=?",[token])
    comment = run_query("SELECT content, id, client_id FROM reviews WHERE client_id=?"[auth])


# TO DO : DELETE 
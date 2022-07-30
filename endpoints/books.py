from app import app 
from helpers.db_helpers import run_query
from flask import  request, jsonify

@app.get('/api/books')
def book_get():
    genre=request.args.get('genre')
    if not genre:
        book_list = run_query("SELECT * FROM books")
    else:
        book_list= run_query("SELECT books.book_id,title,authors,isbn,isbn13,language_code,publication_date,publisher,description FROM genre INNER JOIN books ON books.book_id = genre.id WHERE name =?", [genre])
        print(book_list)
    resp = []
    for book in book_list:
        bk_obj = {}
        bk_obj ['book_id'] = book[0]
        bk_obj ['title'] = book[1]
        bk_obj ['authors'] = book[2]
        bk_obj ['isbn'] = book[3]
        bk_obj ['isbn13'] = book[4]
        bk_obj ['language_code'] = book[5]
        bk_obj ['publication_date'] = book[6]
        bk_obj ['publisher'] = book[7]
        bk_obj ['description'] = book[8]
        resp.append(bk_obj)
    return jsonify (resp) , 200
    
# def genre_get():
#     token = request.args.get('token')
#     run_query("SELECT token FROM client_session INNER JOIN client ON client_session.token = client.id WHERE token= ?" , [token])
#     # genre = run_query('SELECT * from genre')
#     if genre == "fantasy":
#         run_query("SELECT name,title,author,description FROM genre INNER JOIN books ON books.book_id = genre.id WHERE name = 'fantasy")
#     if genre == "romance":
#         run_query("SELECT name,title,author,description  FROM genre INNER JOIN books ON books.book_id = genre.id WHERE name ='romance'")
#     # TO DO add more genres to database 
        


    







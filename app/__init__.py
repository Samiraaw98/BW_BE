from flask import Flask

app = Flask(__name__)


from endpoints import client , client_session,client_follows,books,user_reviews

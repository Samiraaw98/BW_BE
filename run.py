from app import app
from flask_cors import CORS
import sys



if len(sys.argv) >1:
    mode = sys.argv[1]
else :
    print("Missing required mode argument")

if mode == 'testing':
    CORS(app)
    print("Runnng in testing mode !")
    app.run(debug=True)
elif mode == "production" :
        import bjoern
        print("Running in production mode!")
        bjoern.run(app, "0.0.0.0" , 5005)
else:
    print("Invalid mode , must be one of :testing | production")
    exit()
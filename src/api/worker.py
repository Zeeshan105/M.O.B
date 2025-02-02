# --------------------------------
# worker (server)
#
# Workers are responsible for recieving work from the front facing server.
# Each request should include an image of a face which the worker than attempts to match against the available databases
# Using EigRequest, after these processes are completed, the image is sent as a response
#
# NOTE: all workers should be started from inside the src directory
# --------------------------------
from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
import sys, base64, os, base64

sys.path.append(os.getcwd())
from logic.worker.logic import Logic


app = Flask(__name__)  # Flask server instance
api = Api(app)         # Controls the Flask server API

HOST = 'localhost'  # The workers address
PORT = 4000         # The workers port
logic = Logic()


class ProcessImg(Resource):
    def post(self,):
        response = None
        
        if 'img' not in request.files:
            abort(400, description='img not found')
        else:
            img = request.files['img']
            results = logic.runEigenFace(img.read())
            
            if results:
                response = {
                    'name': results.Name,
                    'photo': str(base64.b64encode(results.Photo)),
                    'meanFace': str(base64.b64encode(results.MeanFace))
                }
    
        return jsonify(response)


api.add_resource(ProcessImg, '/')
app.run(host=HOST, port=PORT, debug=True)
from flask import Flask,request,redirect
from flask_restful  import Resource,Api
from flask_cors import CORS
import numpy as np
import os
from tensorflow.keras.models import load_model

app = Flask(__name__)
cors=CORS(app,resources={r"*":{"origins":"*"}})
api=Api(app)
model=load_model("Neural Linear/regression.h5")
class Test(Resource):
    def get(self):
        return "hello AI"
    def post(self):
        try:
            value=request.get_json()
            if(value):
                return {'Post Values':value},201
            return {"error":"Invalid format."}
        except Exception as error:
            return {'error':error}
class GetPredictionOutput(Resource):
    def get(self):
        return {"error":"Invalid Method."}
    def post(self):
        try:
            data=request.get_json()
            features=np.array(data['temperature'],data['pressure']).reshape(1,-1)
            predict=model.predict(features)
            return {'predict':predict[0].tolist()},200
        except Exception as error:
            return {'error':error}
api.add_resource(Test,'/')
api.add_resource(GetPredictionOutput,'/getpredictOutput')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1')
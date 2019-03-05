from flask_restful import Resource, reqparse
import requests
import json
import config

parser = reqparse.RequestParser()
parser.add_argument('nodes', help = 'This field cannot be blank', required = True)
parser.add_argument('wallTime', help = 'This field cannot be blank', required = True)


class NodeReservation(Resource):
    def post(self):
        data = parser.parse_args()
        print(data)
        data2 ={
            "resources": "nodes="+data['nodes']+",walltime="+data['wallTime'],
            "command": "while(true); do sleep 5; echo \"awake\"; done"
        }
        print (data2)
        r = requests.post('https://api.grid5000.fr/3.0/sites/lyon/jobs',auth=(config.G5K_LOGIN ,config.G5K_PASSWORD), data = data2)
        json_data = json.loads(r.text)
        return json_data




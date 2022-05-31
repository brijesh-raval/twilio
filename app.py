from flask import Flask, request
from twilio.rest import Client
import json
 
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Hello, world!"

@app.route('/', methods=['POST'])
def message():
    payload = request.json['payload']
    print(payload)
    from_number = payload['from_number']
    body_text = payload['body']
    to_number = payload['to_number']
    account_sid = payload['account_sid']
    auth_token = payload['auth_token'] 

    client = Client(account_sid, auth_token) 

    message = client.messages.create( 
                                from_='whatsapp:'+from_number,  
                                body=body_text,
                                to='whatsapp:'+to_number
                            ) 

    data = {'messageSID': message.sid}
    print (json.dumps(data))

    return data

if __name__ == "__main__":
    app.run(debug=True)


'''
{
    'payload' : {
        'from_number': '+14155238886',
        'body': 'Hello, Welcome to the Repair pro service'
        'to_number': '+919313730667'
    }
}

{
    "payload" : {
        "from_number": "+14155238886",
        "body": "Hello, Welcome to the Repair pro service",
        "to_number": "+919313730667"
    }
}
'''
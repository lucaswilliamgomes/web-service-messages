import web
import json

class Message:

    def __init__(self, sender, receiver, subject, body):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body

    def serialize(self):
        data = {
            "sender": self.sender,
            "receiver": self.receiver,
            "subject": self.subject,
            "body": self.body
        }
        return json.dumps(data)
    
    def deserialize(self, data):
        return json.loads(data)
    


class Login:
    def POST(self):
        params = web.input()
        if params.get("name"):
            name = params.get("name")
            with open("data.json", "r") as jsonData:
                data = json.load(jsonData)

            for element in data:
                if (element.get("user") == name):
                    response = {
                        "statusCode": 200,
                        "data": element
                    }
                    return response
                
            response = {
                "statusCode": 404,
                "data": ""
            }
            return response
            
        else: 
            response = {
                "statusCode": 404,
                "data": ""
            }
            return response


class ListMessages:
    pass


urls = (
    "/login", Login
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
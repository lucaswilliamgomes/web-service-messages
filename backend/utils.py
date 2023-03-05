import json

responseNotFound = {
    "statusCode": 404,
    "data": ""
}

def search_user_by_name(user_name):
    with open("data/users.json", "r") as jsonData:
        data = json.load(jsonData)

    print (data)
    for user in data:
        if (user.get("name") == user_name):
            return user

    return False


def search_messages_sended_by_user(user_name):
    messages = []
    with open("./data/messages.json", "r") as jsonData:
        data = json.load(jsonData)

    for message in data:
        if (message.get("name_sender") == user_name):
            messages.append(message)
    
    return messages


def search_messages_received_by_user(user_name):
    messages = []
    with open("./data/messages.json", "r") as jsonData:
        data = json.load(jsonData)

    for message in data:
        if (message.get("name_receiver") == user_name):
            messages.append(message)
    
    return messages


def search_message_by_id(id_message):
    with open("./data/messages.json", "r") as jsonData:
        data = json.load(jsonData)

    for message in data:
        if (message.get("id") == id_message):
            return message
    
    return None

def delete_message_by_id(id_message):
    deleted = False
    with open("./data/messages.json", "r") as jsonData:
        data = json.load(jsonData)

    for i, message in enumerate(data):
        if message['id'] == id_message:
            data.pop(i)
            deleted = True
            break

    with open('./data/messages.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    return deleted

    
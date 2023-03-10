import json


def register_user_by_name(user_name):
    with open("data/users.json", "r") as jsonData:
        data = json.load(jsonData)

    for user in data:
        if (user.get("name") == user_name):
            return user
        
    data.append({
        "name": user_name,
    })

    with open('./data/users.json', 'w') as f:
        json.dump(data, f, indent=4)

    return True

def search_user_by_name(user_name):
    with open("data/users.json", "r") as jsonData:
        data = json.load(jsonData)

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


def find_new_message_id():
    with open("./data/messages.json", "r") as jsonData:
        messages = json.load(jsonData)

    if (len(messages) > 0):
        return messages[len(messages) - 1]["id"] + 1

    return 0


def create_new_message(message, id):
    with open("./data/messages.json", "r") as jsonData:
        messages = json.load(jsonData)

    messages.append({
        "id": id,
        "name_sender": message.sender,
        "name_receiver": message.receiver,
        "subject": message.subject,
        "body": message.body
    })

    with open('./data/messages.json', 'w') as f:
        json.dump(messages, f, indent=4)

    
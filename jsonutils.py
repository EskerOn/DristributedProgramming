import json

messageType = {
    'Operation': 0,
    'Data': 1
}

def decodeJSON(message):
    return json.loads(message.decode('utf-8'))
        
def encodeJSON(type, operation= None, result = None):
    msg = {
        'type' : type,
        'operation' : operation,
        'res': result
    }
    return bytes(json.dumps(msg), 'utf-8')

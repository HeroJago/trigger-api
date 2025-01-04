from flask import * 
import json, re
from routes.decorators import RouteDecorators
from funcs.string import sanitize, str_validation

Admin = Blueprint("Admin", __name__)

@Admin.route("/addkey", methods=["GET"])
@RouteDecorators.log
def index_addkey():
    if 'adminkey' in request.args and 'keyname' in request.args and 'expired' in request.args and 'maxtime' in request.args and 'maxconc' in request.args:
        adminkey = sanitize(request.args.get('adminkey', default=None, type=str))
        keyname = sanitize(request.args.get('keyname', default=None, type=str))
        expired = sanitize(request.args.get('expired', default=None, type=str))
        maxtime = sanitize(request.args.get('maxtime', default=None, type=str))
        maxcons = sanitize(request.args.get('maxconc', default=None, type=str))
    else:
        return jsonify({"response_message": "Missing argument(s)."})
    
    if not all([adminkey, keyname, expired, maxtime, maxcons]):
        return jsonify({"response_message": "Missing argument(s). Null values."})
    
    with open("./data/database.json") as e:
        db = json.load(e)
    
    with open("./data/admin_key.json") as e:
        admkey = json.load(e)

    if str_validation(adminkey):
        return jsonify({"response_message": "Error, Malcious character detected."})
    
    if str_validation(keyname):
        return jsonify({"response_message": "Error, Malcious character detected."})
    
    if str_validation(expired):
        return jsonify({"response_message": "Error, Malcious character detected."})
    
    if str_validation(maxtime):
        return jsonify({"response_message": "Error, Malcious character detected."})
    
    if str_validation(maxcons):
        return jsonify({"response_message": "Error, Malcious character detected."})
    
    if not maxtime.isdigit():
        return jsonify({"response_message": "Maxtime must digit."})
    
    if not maxcons.isdigit():
        return jsonify({"response_message": "Maxconc must digit."})
    
    if not maxtime.isdigit():
        return jsonify({"response_message": "Curconc cmust digit."})
    
    if re.match(r'^\d{4}-\d{2}-\d{2}$', expired):
        return jsonify({"response_message": "Format must YEAR-MONTH-DAY, ex: 2045-12-2."})
    else:
        expired = expired

    if adminkey not in admkey['keys']:
        return jsonify({"response_message": "Key invalid."})
    
    try:
        db["keys"][keyname]= {"exp": expired, "maxTime": maxtime, "maxCons": maxcons, "curCons": 0}
        with open("./data/database.json", "w") as json_file:
            json.dump(db, json_file, indent=4)
        return jsonify({"response_message": "Data successfully added."})
    except Exception as e:
        print(e)
        return jsonify({"response_message": "An error occurred."})

@Admin.route("/deletekey", methods=["GET"])
@RouteDecorators.log
def index_deleted_key():
    if 'adminkey' in request.args and 'keyname' in request.args:
        adminkey = sanitize(request.args.get('adminkey', default=None, type=str))
        keyname = sanitize(request.args.get('keyname', default=None, type=str))
    else:
        return jsonify({"response_message": "Missing argument(s)."})
    
    if not all([adminkey, keyname]):
        return jsonify({"response_message": "Missing argument(s). Null values."})
    
    with open("./data/database.json") as e:
        db = json.load(e)
    
    with open("./data/admin_key.json") as e:
        admkey = json.load(e)

    if str_validation(adminkey):
        return jsonify({"response_message": "Error, Malcious character detected."})
    
    if str_validation(keyname):
        return jsonify({"response_message": "Error, Malcious character detected."})

    if adminkey not in admkey['keys']:
        return jsonify({"response_message": "Key invalid."})
    
    try:
        del db["keys"][keyname]
        with open("./data/database.json", "w") as json_file:
            json.dump(db, json_file, indent=4)
        return jsonify({"response_message": "Data successfully deleted."})
    except Exception as e:
        print(e)
        return jsonify({"response_message": "An error occurred."})
        
@Admin.route("/addservers", methods=["GET"])
def index_add_server():
    if 'adminkey' in request.args and 'address' in request.args and 'username' in request.args and 'password' in request.args:
        adminkey = sanitize(request.args.get('adminkey', default=None, type=str))
        address = sanitize(request.args.get('address', default=None, type=str))
        username = sanitize(request.args.get('username', default=None, type=str))
        password = sanitize(request.args.get('password', default=None, type=str))
    else:
        return jsonify({"response_message": "Missing argument(s)."})
    
    if not all([adminkey, address, username, password]):
        return jsonify({"response_message": "Missing argument(s). Null values."})

    with open("./data/vps_servers.json") as e:
        db = json.load(e)

    with open("./data/admin_key.json") as e:
        admkey = json.load(e)
    
    if str_validation(adminkey):
        return jsonify({"response_message": "Error, Malcious character detected."})

    if adminkey not in admkey['keys']:
        return jsonify({"response_message": "Key invalid."})

    try:
        db.append({"address": address, "username": username, "password": password})
        with open("./data/vps_servers.json", "w") as json_file:
            json.dump(db, json_file, indent=4)
        return jsonify({"response_message": "Add Servers successfully"})
    except Exception as e:
        print(e)
        return jsonify({"response_message": "An error occurred."})
# Code by Senkaizen

# Importing necessary libraries
from flask import Flask
from waitress import serve
import logging, os
from colorama import Fore, init
from routes.admin_routes import Admin
from routes.attack_routes import Attack

# Logging
logging.basicConfig(filename='data/record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# Configuration Routes
app = Flask(__name__, None, "static")
app.secret_key = "senkaizen" # Change to ur secret key

# Routes
app.register_blueprint(Attack)
app.register_blueprint(Admin)

@app.route('/')
def indexpage():
    return "[ HI WELCOME TO API Service ]"

@app.errorhandler(404)
def error_404(e):
    return "[ERROR] 404 PAGE NOT FOUND", 404

@app.errorhandler(505)
def error_505(e):
    return "[ERROR] 505 PAGE NOT FOUND", 505

# Start API
if __name__ == "__main__":
    os.system('clear || cls')
    init()
    print(Fore.BLUE, "API servers started.", Fore.RESET)
    serve(app, host="0.0.0.0", port=8080)
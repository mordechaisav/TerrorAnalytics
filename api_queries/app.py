from flask import Flask
from api_queries.routes.map_routes import map_bp
app = Flask(__name__, template_folder='templates')
app.register_blueprint(map_bp)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

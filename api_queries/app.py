from flask import Flask
from api_queries.blueprint.avg_casualties_bp import regions_severity_locations_bp
from api_queries.blueprint.queries_bp import queries_bp
from api_queries.blueprint.region_max_diff import regions_max_diff_bp

app = Flask(__name__)
app.register_blueprint(regions_severity_locations_bp)
app.register_blueprint(regions_max_diff_bp)
app.register_blueprint(queries_bp)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

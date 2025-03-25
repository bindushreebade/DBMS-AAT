from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from routes import app as routes_app
from models import db

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

@app.route("/get-started")
def get_started():
    return render_template("get_started.html")

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(routes_app)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from models import db, Application

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Internship Application API is running."})

@app.route('/apply', methods=['POST'])
def apply():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    domain = data.get('domain')
    duration = data.get('duration')

    if not all([name, email, domain, duration]):
        return jsonify({"error": "All fields are required"}), 400

    application = Application(name=name, email=email, domain=domain, duration=duration)
    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Application submitted successfully", "application_id": application.id}), 201

@app.route('/verify/<int:app_id>', methods=['GET'])
def verify(app_id):
    application = Application.query.get(app_id)
    if application:
        return jsonify({
            "name": application.name,
            "email": application.email,
            "domain": application.domain,
            "duration": application.duration
        })
    else:
        return jsonify({"error": "Application not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

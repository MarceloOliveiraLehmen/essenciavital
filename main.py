import os
import sys
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configure CORS to accept requests from https://meu-frontend.netlify.app
CORS(app, resources={r"/api/*": {"origins": "https://meu-frontend.netlify.app"}})

app.register_blueprint(user_bp, url_prefix='/api')

# Ebooks routes
@app.route('/api/ebooks', methods=['GET'])
def get_ebooks():
    # This is a placeholder. In a real application, you would fetch data from a database.
    ebooks = [
        {"id": 1, "title": "Mindfulness Diário", "price": 19.90, "category": "Bem-Estar"},
        {"id": 2, "title": "Alimentação Saudável", "price": 24.90, "category": "Nutrição"}
    ]
    return jsonify(ebooks)

@app.route('/api/ebooks/<int:ebook_id>', methods=['GET'])
def get_ebook(ebook_id):
    # Placeholder for fetching a single ebook
    ebook = {"id": ebook_id, "title": f"Ebook {ebook_id}", "price": 9.99, "category": "Geral"}
    return jsonify(ebook)

# Categories routes
@app.route('/api/categories', methods=['GET'])
def get_categories():
    # Placeholder for fetching categories
    categories = [
        {"id": 1, "name": "Bem-Estar"},
        {"id": 2, "name": "Saúde Mental"},
        {"id": 3, "name": "Nutrição"},
        {"id": 4, "name": "Exercícios"},
        {"id": 5, "name": "Mindfulness"}
    ]
    return jsonify(categories)

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



from flask import Blueprint, jsonify, request
from models import db, Documentation

documentation_bp = Blueprint('documentation_routes', __name__, url_prefix='/documentation')

@documentation_bp.route('/', methods=['GET'])
def get_documentation():
    documentation = Documentation.query.first()
    if documentation:
        return jsonify({"documentation": documentation.serialize()})
    else:
        return jsonify({"message": "Documentation not found"}), 404

@documentation_bp.route('/', methods=['PUT'])
def update_documentation():
    data = request.get_json()
    if 'content' not in data:
        return jsonify({"error": "Content not provided"}), 400

    documentation = Documentation.query.first()
    if documentation:
        documentation.content = data['content']
    else:
        documentation = Documentation(content=data['content'])
        db.session.add(documentation)

    db.session.commit()
    return jsonify({"message": "Documentation updated successfully."})

@documentation_bp.route('/', methods=['POST'])
def create_documentation():
    data = request.get_json()
    if 'content' not in data:
        return jsonify({"error": "Content not provided"}), 400

    documentation = Documentation(content=data['content'])
    db.session.add(documentation)
    db.session.commit()

    return jsonify({"message": "Documentation created successfully"})
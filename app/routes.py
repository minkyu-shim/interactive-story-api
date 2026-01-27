from flask import Blueprint, jsonify, request
from .models import Story, Page, Choice
from . import db

# Create a Blueprint named 'api'
api_bp = Blueprint('api', __name__)

@api_bp.route('/stories', methods=['GET'])
def get_stories():
    # Fetch only published stories
    stories = Story.query.filter_by(status='published').all()
    # Convert the list of objects into a list of dictionaries (JSON)
    return jsonify([story.to_dict() for story in stories])

@api_bp.route('/stories/<int:story_id>', methods=['GET'])
def get_story(story_id):
    story = Story.query.get_or_404(story_id)
    return jsonify(story.to_dict())

@api_bp.route('/stories', methods=['POST'])
def create_story():
    data = request.get_json()
    new_story = Story(
        title=data.get('title'),
        description=data.get('description'),
        status='published'
    )
    db.session.add(new_story)
    db.session.commit()
    return jsonify(new_story.to_dict()), 201

@api_bp.route('/stories/<int:story_id>/start', methods=['GET'])
def get_story_start(story_id):
    """Fetches the first page of a specific story."""
    story = Story.query.get_or_404(story_id)
    if not story.start_page_id:
        return jsonify({"error": "This story has no start page defined"}), 400

    # We find the start page and return its data
    page = Page.query.get(story.start_page_id)
    return jsonify(page.to_dict())


@api_bp.route('/pages/<int:page_id>', methods=['GET'])
def get_page(page_id):
    """Fetches a specific page and its choices."""
    page = Page.query.get_or_404(page_id)
    return jsonify(page.to_dict())
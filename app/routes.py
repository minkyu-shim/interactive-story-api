from flask import Blueprint, jsonify, request
from .models import Story, Page, Choice
from . import db

# Create a Blueprint named 'api'
api_bp = Blueprint('api', __name__)


@api_bp.route('/stories', methods=['GET'])
def get_stories():
    # Allow filtering by status via URL parameters (?status=published)
    status_filter = request.args.get('status')

    if status_filter:
        stories = Story.query.filter_by(status=status_filter).all()
    else:
        # Default behavior: show everything
        stories = Story.query.all()

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
        status=data.get('status', 'draft')
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


@api_bp.route('/stories/<int:story_id>/pages', methods=['POST'])
def create_page(story_id):
    """Creates a new page for a specific story."""
    story = Story.query.get_or_404(story_id)
    data = request.get_json()

    new_page = Page(
        text=data.get('text'),
        is_ending=data.get('is_ending', False),
        ending_label=data.get('ending_label'),
        story_id=story.id
    )

    db.session.add(new_page)
    db.session.commit()
    return jsonify(new_page.to_dict()), 201


@api_bp.route('/pages/<int:page_id>/choices', methods=['POST'])
def create_choice(page_id):
    """Creates a choice that leads out of a specific page."""
    page = Page.query.get_or_404(page_id)
    data = request.get_json()

    new_choice = Choice(
        text=data.get('text'),
        page_id=page.id,
        next_page_id=data.get('next_page_id')  # The ID of the destination page
    )

    db.session.add(new_choice)
    db.session.commit()
    return jsonify(new_choice.to_dict()), 201


@api_bp.route('/stories/<int:story_id>', methods=['PUT'])
def update_story(story_id):
    story = Story.query.get_or_404(story_id)
    data = request.get_json()

    # Update fields if they are provided in the request
    story.title = data.get('title', story.title)
    story.description = data.get('description', story.description)
    story.status = data.get('status', story.status)
    story.start_page_id = data.get('start_page_id', story.start_page_id)

    db.session.commit()
    return jsonify(story.to_dict())


@api_bp.route('/stories/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    """Deletes a story and all its associated pages/choices via cascade."""
    story = Story.query.get_or_404(story_id)
    db.session.delete(story)
    db.session.commit()
    return '', 204

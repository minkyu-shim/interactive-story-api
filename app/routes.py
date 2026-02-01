from flask import Blueprint, jsonify, request
from flask.views import MethodView
from .models import Story, Page, Choice
from . import db

api_bp = Blueprint('api', __name__)


class StoryListAPI(MethodView):
    """
    Handles operations for the collection of Stories.
    URL: /stories
    """

    def get(self):
        # Filter logic
        status_filter = request.args.get('status')
        if status_filter:
            stories = Story.query.filter_by(status=status_filter).all()
        else:
            stories = Story.query.all()

        return jsonify([story.to_dict() for story in stories])

    def post(self):
        # Creation logic
        data = request.get_json()
        new_story = Story(
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status', 'draft')
        )
        db.session.add(new_story)
        db.session.commit()
        return jsonify(new_story.to_dict()), 201


class StoryDetailAPI(MethodView):
    """
    Handles operations for a single Story entity.
    URL: /stories/<story_id>
    """

    def get(self, story_id):
        story = Story.query.get_or_404(story_id)
        return jsonify(story.to_dict())

    def put(self, story_id):
        story = Story.query.get_or_404(story_id)
        data = request.get_json()

        story.title = data.get('title', story.title)
        story.description = data.get('description', story.description)
        story.status = data.get('status', story.status)
        story.start_page_id = data.get('start_page_id', story.start_page_id)

        db.session.commit()
        return jsonify(story.to_dict())

    def delete(self, story_id):
        story = Story.query.get_or_404(story_id)
        db.session.delete(story)
        db.session.commit()
        return '', 204


class StoryStartAPI(MethodView):
    """
    Specific logic to retrieve the starting page of a story.
    URL: /stories/<story_id>/start
    """

    def get(self, story_id):
        story = Story.query.get_or_404(story_id)
        if not story.start_page_id:
            return jsonify({"error": "This story has no start page defined"}), 400

        page = Page.query.get(story.start_page_id)
        # Handle case where ID exists on story but Page was deleted
        if not page:
            return jsonify({"error": "Start page not found"}), 404

        return jsonify(page.to_dict())


class PageCreationAPI(MethodView):
    """
    Handles creating a page linked to a specific story.
    URL: /stories/<story_id>/pages
    """

    def post(self, story_id):
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


class PageDetailAPI(MethodView):
    """
    Handles fetching a single page.
    URL: /pages/<page_id>
    """

    def get(self, page_id):
        page = Page.query.get_or_404(page_id)
        return jsonify(page.to_dict())


class ChoiceCreationAPI(MethodView):
    """
    Handles creating a choice for a specific page.
    URL: /pages/<page_id>/choices
    """

    def post(self, page_id):
        page = Page.query.get_or_404(page_id)
        data = request.get_json()

        new_choice = Choice(
            text=data.get('text'),
            page_id=page.id,
            next_page_id=data.get('next_page_id')
        )
        db.session.add(new_choice)
        db.session.commit()
        return jsonify(new_choice.to_dict()), 201


# --- Route Registration ---

api_bp.add_url_rule('/stories', view_func=StoryListAPI.as_view('story_list'))
api_bp.add_url_rule('/stories/<int:story_id>', view_func=StoryDetailAPI.as_view('story_detail'))
api_bp.add_url_rule('/stories/<int:story_id>/start', view_func=StoryStartAPI.as_view('story_start'))
api_bp.add_url_rule('/stories/<int:story_id>/pages', view_func=PageCreationAPI.as_view('page_creation'))
api_bp.add_url_rule('/pages/<int:page_id>', view_func=PageDetailAPI.as_view('page_detail'))
api_bp.add_url_rule('/pages/<int:page_id>/choices', view_func=ChoiceCreationAPI.as_view('choice_creation'))
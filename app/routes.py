from flask import Blueprint, abort, current_app, jsonify, request
from flask.views import MethodView

from . import db
from .models import Choice, Story, StoryNode

api_bp = Blueprint("api", __name__)


@api_bp.before_request
def require_api_key():
    expected_api_key = (current_app.config.get("FLASK_API_KEY") or "").strip()
    if not expected_api_key:
        return None

    provided_api_key = request.headers.get("X-API-KEY", "").strip()
    if provided_api_key != expected_api_key:
        return jsonify({"error": "Unauthorized: invalid API key"}), 401

    return None


def _json_payload():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def _normalize_content(data, fallback=None):
    if "content" in data and isinstance(data.get("content"), list):
        return data.get("content")
    if "dialogue" in data and isinstance(data.get("dialogue"), list):
        return data.get("dialogue")
    if "text" in data:
        return [{"speaker": "System", "text": data.get("text", "")}]
    return fallback if fallback is not None else []


def _resolve_choice_payload(data):
    text = data.get("text") or data.get("label")
    target = data.get("next_page_id") or data.get("target_node")
    effect = data.get("effect")
    return text, target, effect


def _resolve_story_id_from_request_payload():
    story_id = request.args.get("story_id", type=int)
    if story_id is not None:
        return story_id
    payload = _json_payload()
    value = payload.get("story_id")
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _get_node_by_custom_id_or_404(custom_id):
    matches = StoryNode.query.filter_by(custom_id=custom_id).order_by(StoryNode.id.asc()).all()
    if not matches:
        abort(404)
    if len(matches) == 1:
        return matches[0]

    story_id = _resolve_story_id_from_request_payload()
    if story_id is not None:
        for node in matches:
            if node.story_id == story_id:
                return node

    # Fallback for legacy clients that only send custom_id.
    return matches[0]


def _apply_node_updates(node, data):
    if "type" in data and data.get("type"):
        node.node_type = data.get("type")
    if "background" in data:
        node.background = data.get("background")
    if "affinity_change" in data:
        node.affinity_change = data.get("affinity_change") or {}
    if any(key in data for key in ("content", "dialogue", "text")):
        node.content_data = _normalize_content(data, fallback=node.content_data)
    if "is_ending" in data:
        node.is_ending = bool(data.get("is_ending"))
    if "ending_label" in data:
        node.ending_outcome = data.get("ending_label")
    elif "outcome" in data:
        node.ending_outcome = data.get("outcome")
    if node.node_type == "ending":
        node.is_ending = True


class StoryListAPI(MethodView):
    def get(self):
        status = request.args.get("status")
        query = Story.query
        if status:
            query = query.filter(Story.status == status)
        stories = query.order_by(Story.id.asc()).all()
        return jsonify([story.to_dict() for story in stories])

    def post(self):
        data = _json_payload()
        new_story = Story(
            title=data.get("title") or "Untitled",
            description=data.get("description"),
            genre=data.get("genre", "General"),
            author=data.get("author", "Anonymous"),
            initial_state=data.get("initial_state") or data.get("player_state") or {},
            status=data.get("status", "draft"),
        )
        db.session.add(new_story)
        db.session.commit()
        return jsonify(new_story.to_dict()), 201


class StoryDetailAPI(MethodView):
    def get(self, story_id):
        story = Story.query.get_or_404(story_id)
        return jsonify(story.to_dict(include_pages=True))

    def put(self, story_id):
        story = Story.query.get_or_404(story_id)
        data = _json_payload()

        story.title = data.get("title", story.title)
        story.description = data.get("description", story.description)
        story.genre = data.get("genre", story.genre)
        story.initial_state = data.get("initial_state", story.initial_state)
        story.status = data.get("status", story.status)

        db.session.commit()
        return jsonify(story.to_dict(include_pages=True))

    def delete(self, story_id):
        story = Story.query.get_or_404(story_id)
        db.session.delete(story)
        db.session.commit()
        return "", 204


class StoryNodeListAPI(MethodView):
    def get(self, story_id):
        nodes = StoryNode.query.filter_by(story_id=story_id).order_by(StoryNode.id.asc()).all()
        return jsonify([node.to_dict() for node in nodes])

    def post(self, story_id):
        story = Story.query.get_or_404(story_id)
        data = _json_payload()

        custom_id = data.get("custom_id") or data.get("id")
        if not custom_id:
            return jsonify({"error": "Missing node id. Provide 'custom_id' or 'id'."}), 400

        existing = StoryNode.query.filter_by(story_id=story_id, custom_id=custom_id).first()
        if existing:
            return jsonify({"error": f"Node ID '{custom_id}' already exists in this story."}), 400

        node_type = data.get("type")
        if not node_type:
            node_type = "ending" if data.get("is_ending") else "dialogue"

        node = StoryNode(
            story_id=story.id,
            custom_id=custom_id,
            node_type=node_type,
            background=data.get("background"),
            content_data=_normalize_content(data, fallback=[]),
            affinity_change=data.get("affinity_change", {}),
            is_ending=bool(data.get("is_ending") or node_type == "ending"),
            ending_outcome=data.get("ending_label") if "ending_label" in data else data.get("outcome"),
        )
        db.session.add(node)
        db.session.commit()
        return jsonify(node.to_dict()), 201


class StoryNodeDetailAPI(MethodView):
    def get(self, story_id, custom_id):
        node = StoryNode.query.filter_by(story_id=story_id, custom_id=custom_id).first_or_404()
        return jsonify(node.to_dict())

    def put(self, story_id, custom_id):
        node = StoryNode.query.filter_by(story_id=story_id, custom_id=custom_id).first_or_404()
        data = _json_payload()
        _apply_node_updates(node, data)
        db.session.commit()
        return jsonify(node.to_dict())

    def delete(self, story_id, custom_id):
        node = StoryNode.query.filter_by(story_id=story_id, custom_id=custom_id).first_or_404()
        db.session.delete(node)
        db.session.commit()
        return "", 204


class NodeAliasDetailAPI(MethodView):
    def get(self, custom_id):
        node = _get_node_by_custom_id_or_404(custom_id)
        return jsonify(node.to_dict())

    def put(self, custom_id):
        node = _get_node_by_custom_id_or_404(custom_id)
        data = _json_payload()
        _apply_node_updates(node, data)
        db.session.commit()
        return jsonify(node.to_dict())

    def delete(self, custom_id):
        node = _get_node_by_custom_id_or_404(custom_id)
        db.session.delete(node)
        db.session.commit()
        return "", 204


class StoryStartAPI(MethodView):
    def get(self, story_id):
        start_node = StoryNode.query.filter(
            StoryNode.story_id == story_id,
            StoryNode.custom_id.in_(["00_prologue", "start", "root", "prologue"]),
        ).first()

        if not start_node:
            start_node = StoryNode.query.filter_by(story_id=story_id).order_by(StoryNode.id.asc()).first()

        if not start_node:
            return jsonify({"error": "No nodes found for this story"}), 404

        return jsonify(start_node.to_dict())


class ChoiceCreationAPI(MethodView):
    def post(self, story_id, node_custom_id):
        parent_node = StoryNode.query.filter_by(story_id=story_id, custom_id=node_custom_id).first_or_404()
        data = _json_payload()
        text, target, effect = _resolve_choice_payload(data)
        if not text or not target:
            return jsonify({"error": "Choice requires text/label and next_page_id/target_node."}), 400

        choice = Choice(
            text=text,
            node_id=parent_node.id,
            target_node_custom_id=target,
            effect_description=effect,
        )
        db.session.add(choice)
        db.session.commit()
        return jsonify(choice.to_dict()), 201


class ChoiceCreationAliasAPI(MethodView):
    def post(self, node_custom_id):
        parent_node = _get_node_by_custom_id_or_404(node_custom_id)
        data = _json_payload()
        text, target, effect = _resolve_choice_payload(data)
        if not text or not target:
            return jsonify({"error": "Choice requires text/label and next_page_id/target_node."}), 400

        choice = Choice(
            text=text,
            node_id=parent_node.id,
            target_node_custom_id=target,
            effect_description=effect,
        )
        db.session.add(choice)
        db.session.commit()
        return jsonify(choice.to_dict()), 201


class ChoiceDetailAPI(MethodView):
    def get(self, choice_id):
        choice = Choice.query.get_or_404(choice_id)
        return jsonify(choice.to_dict())

    def put(self, choice_id):
        choice = Choice.query.get_or_404(choice_id)
        data = _json_payload()
        text, target, effect = _resolve_choice_payload(data)
        if text is not None:
            choice.text = text
        if target is not None:
            choice.target_node_custom_id = target
        if "effect" in data:
            choice.effect_description = effect

        db.session.commit()
        return jsonify(choice.to_dict())

    def delete(self, choice_id):
        choice = Choice.query.get_or_404(choice_id)
        db.session.delete(choice)
        db.session.commit()
        return "", 204


class StoryImportAPI(MethodView):
    def post(self):
        data = _json_payload()

        story_info = data.get("project_meta", {})
        player_state = data.get("initial_state") or data.get("player_state") or {}

        new_story = Story(
            title=story_info.get("title", "Untitled"),
            description=f"Version: {story_info.get('version')}",
            genre=story_info.get("genre"),
            author=story_info.get("author"),
            initial_state=player_state,
            status=story_info.get("status", "draft"),
        )
        db.session.add(new_story)
        db.session.commit()

        nodes_data = data.get("story_nodes", [])
        for node_data in nodes_data:
            node = StoryNode(
                story_id=new_story.id,
                custom_id=node_data.get("custom_id") or node_data.get("id"),
                node_type=node_data.get("type", "dialogue"),
                background=node_data.get("background"),
                content_data=_normalize_content(node_data, fallback=[]),
                affinity_change=node_data.get("affinity_change", {}),
                is_ending=bool(node_data.get("is_ending") or node_data.get("type") == "ending"),
                ending_outcome=node_data.get("ending_label")
                if "ending_label" in node_data
                else node_data.get("outcome"),
            )
            db.session.add(node)
        db.session.commit()

        for node_data in nodes_data:
            parent_custom_id = node_data.get("custom_id") or node_data.get("id")
            parent_node = StoryNode.query.filter_by(story_id=new_story.id, custom_id=parent_custom_id).first()
            if not parent_node:
                continue

            for choice_data in node_data.get("choices", []):
                text, target, effect = _resolve_choice_payload(choice_data)
                if not text or not target:
                    continue
                choice = Choice(
                    text=text,
                    node_id=parent_node.id,
                    target_node_custom_id=target,
                    effect_description=effect,
                )
                db.session.add(choice)

        db.session.commit()
        return jsonify({"message": "Import successful", "story_id": new_story.id}), 201


api_bp.add_url_rule("/stories", view_func=StoryListAPI.as_view("story_list"))
api_bp.add_url_rule("/stories/<int:story_id>", view_func=StoryDetailAPI.as_view("story_detail"))
api_bp.add_url_rule("/stories/<int:story_id>/start", view_func=StoryStartAPI.as_view("story_start"))

api_bp.add_url_rule("/stories/<int:story_id>/nodes", view_func=StoryNodeListAPI.as_view("node_list"))
api_bp.add_url_rule(
    "/stories/<int:story_id>/nodes/<string:custom_id>",
    view_func=StoryNodeDetailAPI.as_view("node_detail"),
)

api_bp.add_url_rule("/nodes/<string:custom_id>", view_func=NodeAliasDetailAPI.as_view("node_alias_detail"))
api_bp.add_url_rule(
    "/stories/<int:story_id>/nodes/<string:node_custom_id>/choices",
    view_func=ChoiceCreationAPI.as_view("choice_creation"),
)
api_bp.add_url_rule(
    "/nodes/<string:node_custom_id>/choices",
    view_func=ChoiceCreationAliasAPI.as_view("choice_creation_alias"),
)
api_bp.add_url_rule("/choices/<int:choice_id>", view_func=ChoiceDetailAPI.as_view("choice_detail"))

api_bp.add_url_rule("/import", view_func=StoryImportAPI.as_view("story_import"))

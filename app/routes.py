from flask import Blueprint, jsonify, request, abort
from flask.views import MethodView
from .models import Story, StoryNode, Choice
from . import db

api_bp = Blueprint('api', __name__)


# --- 1. Story Management ---

class StoryListAPI(MethodView):
    """
    스토리 목록 조회 및 새 스토리 생성
    URL: /stories
    """

    def get(self):
        stories = Story.query.all()
        return jsonify([story.to_dict() for story in stories])

    def post(self):
        data = request.get_json()
        new_story = Story(
            title=data.get('title'),
            description=data.get('description'),
            genre=data.get('genre', 'General'),
            author=data.get('author', 'Anonymous'),
            initial_state=data.get('initial_state', {}),  # 플레이어 초기 스탯 JSON
            status=data.get('status', 'draft')
        )
        db.session.add(new_story)
        db.session.commit()
        return jsonify(new_story.to_dict()), 201


class StoryDetailAPI(MethodView):
    """
    단일 스토리 관리
    URL: /stories/<int:story_id>
    """

    def get(self, story_id):
        story = Story.query.get_or_404(story_id)
        return jsonify(story.to_dict())

    def put(self, story_id):
        story = Story.query.get_or_404(story_id)
        data = request.get_json()

        story.title = data.get('title', story.title)
        story.description = data.get('description', story.description)
        story.genre = data.get('genre', story.genre)
        story.initial_state = data.get('initial_state', story.initial_state)
        story.status = data.get('status', story.status)

        db.session.commit()
        return jsonify(story.to_dict())

    def delete(self, story_id):
        story = Story.query.get_or_404(story_id)
        db.session.delete(story)
        db.session.commit()
        return '', 204


# --- 2. Node (Scene) Management ---

class StoryNodeListAPI(MethodView):
    """
    특정 스토리에 노드(장면) 추가
    URL: /stories/<int:story_id>/nodes
    """

    def get(self, story_id):
        # 해당 스토리의 모든 노드 조회 (디버깅/편집용)
        nodes = StoryNode.query.filter_by(story_id=story_id).all()
        return jsonify([node.to_dict() for node in nodes])

    def post(self, story_id):
        story = Story.query.get_or_404(story_id)
        data = request.get_json()

        # custom_id 중복 체크 (스토리 내에서 유일해야 함)
        existing = StoryNode.query.filter_by(story_id=story_id, custom_id=data.get('id')).first()
        if existing:
            return jsonify({"error": f"Node ID '{data.get('id')}' already exists in this story."}), 400

        new_node = StoryNode(
            story_id=story.id,
            custom_id=data.get('id'),  # JSON의 "node_01..."
            node_type=data.get('type', 'dialogue'),
            background=data.get('background'),
            content_data=data.get('content', []),  # 대화 리스트 JSON
            affinity_change=data.get('affinity_change', {}),
            is_ending=data.get('is_ending', False),
            ending_outcome=data.get('outcome')
        )
        db.session.add(new_node)
        db.session.commit()
        return jsonify(new_node.to_dict()), 201


class StoryNodeDetailAPI(MethodView):
    """
    게임 플레이 중 다음 노드 불러오기 (핵심 로직)
    URL: /stories/<int:story_id>/nodes/<string:custom_id>
    """

    def get(self, story_id, custom_id):
        # DB ID가 아닌, JSON 상의 custom_id(예: "node_01")로 조회
        node = StoryNode.query.filter_by(story_id=story_id, custom_id=custom_id).first_or_404()
        return jsonify(node.to_dict())

    def put(self, story_id, custom_id):
        node = StoryNode.query.filter_by(story_id=story_id, custom_id=custom_id).first_or_404()
        data = request.get_json()

        # 필드 업데이트
        node.background = data.get('background', node.background)
        node.content_data = data.get('content', node.content_data)
        node.affinity_change = data.get('affinity_change', node.affinity_change)
        node.is_ending = data.get('is_ending', node.is_ending)

        db.session.commit()
        return jsonify(node.to_dict())


class StoryStartAPI(MethodView):
    """
    스토리의 시작점(프롤로그) 자동 탐색
    URL: /stories/<int:story_id>/start
    """

    def get(self, story_id):
        # 1. 'prologue'나 'start'라는 custom_id가 있는지 먼저 찾음
        start_node = StoryNode.query.filter(
            StoryNode.story_id == story_id,
            StoryNode.custom_id.in_(['00_prologue', 'start', 'root', 'prologue'])
        ).first()

        # 2. 없으면 DB에 제일 먼저 등록된 노드(id가 가장 작은)를 시작점으로 간주
        if not start_node:
            start_node = StoryNode.query.filter_by(story_id=story_id).order_by(StoryNode.id.asc()).first()

        if not start_node:
            return jsonify({"error": "No nodes found for this story"}), 404

        return jsonify(start_node.to_dict())


# --- 3. Choice Management ---

class ChoiceCreationAPI(MethodView):
    """
    특정 노드에 선택지 추가
    URL: /stories/<int:story_id>/nodes/<string:node_custom_id>/choices
    """

    def post(self, story_id, node_custom_id):
        # 부모 노드 찾기
        parent_node = StoryNode.query.filter_by(story_id=story_id, custom_id=node_custom_id).first_or_404()
        data = request.get_json()

        new_choice = Choice(
            text=data.get('label'),  # JSON의 label
            node_id=parent_node.id,
            target_node_custom_id=data.get('target_node'),  # 이동할 노드의 custom_id
            effect_description=data.get('effect')
        )
        db.session.add(new_choice)
        db.session.commit()
        return jsonify(new_choice.to_dict()), 201


# --- 4. Bulk Import (Optional but Recommended) ---

class StoryImportAPI(MethodView):
    """
    JSON 통짜 데이터를 받아서 Story, Nodes, Choices를 한 번에 생성
    URL: /import
    """

    def post(self):
        data = request.get_json()

        # 1. Story 생성
        story_info = data.get('project_meta', {})
        player_state = data.get('initial_state', {})

        new_story = Story(
            title=story_info.get('title', 'Untitled'),
            description=f"Version: {story_info.get('version')}",
            genre=story_info.get('genre'),
            author=story_info.get('author'),
            initial_state=player_state
        )
        db.session.add(new_story)
        db.session.commit()  # ID 생성을 위해 커밋

        # 2. Nodes & Choices 생성
        nodes_data = data.get('story_nodes', [])

        # Node 먼저 생성 (Choice가 참조할 custom_id가 필요하므로)
        for node_data in nodes_data:
            node = StoryNode(
                story_id=new_story.id,
                custom_id=node_data.get('id'),
                node_type=node_data.get('type'),
                background=node_data.get('background'),
                content_data=node_data.get('dialogue') or [{"text": node_data.get('text', '')}],  # 대화 포맷 통일
                affinity_change=node_data.get('affinity_change'),
                is_ending=node_data.get('is_ending', False),
                ending_outcome=node_data.get('outcome')
            )
            db.session.add(node)
        db.session.commit()

        # 3. Choices 생성 (이제 Node들이 DB에 있으므로 연결 가능)
        # SQLAlchemy 세션을 새로고침하여 방금 넣은 Node들을 인식
        for node_data in nodes_data:
            if 'choices' in node_data:
                parent_node = StoryNode.query.filter_by(story_id=new_story.id, custom_id=node_data['id']).first()
                for choice_data in node_data['choices']:
                    choice = Choice(
                        text=choice_data['label'],
                        node_id=parent_node.id,
                        target_node_custom_id=choice_data.get('target_node'),
                        effect_description=choice_data.get('effect')
                    )
                    db.session.add(choice)

        db.session.commit()
        return jsonify({"message": "Import successful", "story_id": new_story.id}), 201


# --- Register Rules ---

# Story
api_bp.add_url_rule('/stories', view_func=StoryListAPI.as_view('story_list'))
api_bp.add_url_rule('/stories/<int:story_id>', view_func=StoryDetailAPI.as_view('story_detail'))
api_bp.add_url_rule('/stories/<int:story_id>/start', view_func=StoryStartAPI.as_view('story_start'))

# Nodes (custom_id 사용)
api_bp.add_url_rule('/stories/<int:story_id>/nodes', view_func=StoryNodeListAPI.as_view('node_list'))
api_bp.add_url_rule('/stories/<int:story_id>/nodes/<string:custom_id>',
                    view_func=StoryNodeDetailAPI.as_view('node_detail'))

# Choices
api_bp.add_url_rule('/stories/<int:story_id>/nodes/<string:node_custom_id>/choices',
                    view_func=ChoiceCreationAPI.as_view('choice_creation'))

# Import
api_bp.add_url_rule('/import', view_func=StoryImportAPI.as_view('story_import'))
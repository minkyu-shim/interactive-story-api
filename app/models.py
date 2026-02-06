from . import db
from sqlalchemy.dialects.postgresql import JSON


class Story(db.Model):
    __tablename__ = 'story'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(50))  # 추가: 장르
    author = db.Column(db.String(50))  # 추가: 작가

    # 중요: 게임 시작 시 플레이어의 초기 스탯(돈, 로직 등)을 저장
    initial_state = db.Column(db.JSON, default=dict)

    status = db.Column(db.String(20), default='published')

    # Relationship
    # Page 대신 Node라는 용어가 게임 로직에 더 적합하여 변경 권장 (테이블명은 page 유지 가능)
    nodes = db.relationship('StoryNode', backref='story', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "genre": self.genre,
            "initial_state": self.initial_state,
            "start_node_id": self.nodes[0].custom_id if self.nodes else None  # 첫 노드 찾기 로직 필요
        }


class StoryNode(db.Model):
    """
    기존 Page 모델의 확장판.
    단순 텍스트가 아니라 '대화', '이벤트', '배경' 등을 모두 포함합니다.
    """
    __tablename__ = 'story_node'

    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)

    # JSON의 "id": "node_01_prologue" 처럼 문자열 ID를 저장해두면 관리가 편합니다.
    custom_id = db.Column(db.String(50), index=True)

    # 노드 타입 (dialogue, narrative, choice, ending 등)
    node_type = db.Column(db.String(20), default='dialogue')

    # 배경 이미지 파일명 (예: "pc_bang_chaos")
    background = db.Column(db.String(100))

    # 중요: 단순 text가 아니라, 화자와 대사가 분리된 구조를 통째로 저장
    # 예: [{"speaker": "차수연", "text": "너 바보니?"}, ...]
    content_data = db.Column(db.JSON, default=list)

    # 이 노드를 지나갈 때 변하는 스탯 (예: {"cha_sooyeon": 10})
    affinity_change = db.Column(db.JSON, default=dict)

    # 엔딩 여부
    is_ending = db.Column(db.Boolean, default=False)
    ending_outcome = db.Column(db.String(100), nullable=True)  # 엔딩 결과 요약

    # Choices
    choices = db.relationship('Choice', backref='source_node', foreign_keys='Choice.node_id')

    def to_dict(self):
        return {
            "id": self.custom_id,  # 내부 DB id보다 custom_id를 쓰는 게 프론트엔드에서 편함
            "type": self.node_type,
            "background": self.background,
            "content": self.content_data,  # JSON 그대로 반환
            "affinity_change": self.affinity_change,
            "is_ending": self.is_ending,
            "outcome": self.ending_outcome,
            "choices": [choice.to_dict() for choice in self.choices]
        }


class Choice(db.Model):
    __tablename__ = 'choice'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    node_id = db.Column(db.Integer, db.ForeignKey('story_node.id'), nullable=False)

    # 다음으로 이동할 노드의 custom_id를 저장하거나, FK를 걸 수 있습니다.
    # 여기서는 유연성을 위해 target_node_id (custom_id string)를 추천합니다.
    target_node_custom_id = db.Column(db.String(50), nullable=True)

    # 선택 시 발생하는 효과 텍스트 (예: "자금 확보, 의리 상승")
    effect_description = db.Column(db.String(100))

    def to_dict(self):
        return {
            "label": self.text,
            "target_node": self.target_node_custom_id,
            "effect": self.effect_description
        }
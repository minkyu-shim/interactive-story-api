from . import db


class Story(db.Model):
    __tablename__ = "story"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(50))
    author = db.Column(db.String(50))
    initial_state = db.Column(db.JSON, default=dict)
    status = db.Column(db.String(20), default="published")

    nodes = db.relationship("StoryNode", backref="story", cascade="all, delete-orphan")

    def to_dict(self, include_pages=False):
        payload = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "genre": self.genre,
            "initial_state": self.initial_state,
            "status": self.status,
            "start_node_id": self.nodes[0].custom_id if self.nodes else None,
        }
        if include_pages:
            payload["pages"] = [node.to_dict() for node in self.nodes]
        return payload


class StoryNode(db.Model):
    __tablename__ = "story_node"

    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("story.id"), nullable=False)
    custom_id = db.Column(db.String(50), index=True)
    node_type = db.Column(db.String(20), default="dialogue")
    background = db.Column(db.String(100))
    content_data = db.Column(db.JSON, default=list)
    affinity_change = db.Column(db.JSON, default=dict)
    is_ending = db.Column(db.Boolean, default=False)
    ending_outcome = db.Column(db.String(100), nullable=True)

    choices = db.relationship("Choice", backref="source_node", foreign_keys="Choice.node_id")

    def to_dict(self):
        text = ""
        if isinstance(self.content_data, list) and self.content_data:
            first_item = self.content_data[0]
            if isinstance(first_item, dict):
                text = first_item.get("text", "") or ""

        return {
            "id": self.custom_id,
            "custom_id": self.custom_id,
            "title": self.custom_id,
            "type": self.node_type,
            "background": self.background,
            "content": self.content_data,
            "text": text,
            "affinity_change": self.affinity_change,
            "is_ending": bool(self.is_ending or self.node_type == "ending"),
            # Django editor expects this key. Stored in ending_outcome for compatibility.
            "ending_label": self.ending_outcome,
            "outcome": self.ending_outcome,
            "choices": [choice.to_dict() for choice in self.choices],
        }


class Choice(db.Model):
    __tablename__ = "choice"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    node_id = db.Column(db.Integer, db.ForeignKey("story_node.id"), nullable=False)
    target_node_custom_id = db.Column(db.String(50), nullable=True)
    effect_description = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "next_page_id": self.target_node_custom_id,
            "label": self.text,
            "target_node": self.target_node_custom_id,
            "effect": self.effect_description,
        }

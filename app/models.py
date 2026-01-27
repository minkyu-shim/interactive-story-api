from . import db


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='published')
    start_page_id = db.Column(db.Integer, nullable=True)

    # Relationship: One story has many pages
    pages = db.relationship('Page', backref='story', cascade="all, delete-orphan")

    def to_dict(self):
        """Example: Converts a database row into a Python dictionary for JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "start_page_id": self.start_page_id
        }


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    is_ending = db.Column(db.Boolean, default=False)
    ending_label = db.Column(db.String(50), nullable=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)

    # Relationship: A page has many choices leading out
    choices = db.relationship('Choice', backref='source_page', foreign_keys='Choice.page_id')

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_ending": self.is_ending,
            "ending_label": self.ending_label,
            "choices": [choice.to_dict() for choice in self.choices]  # Nested choices!
        }


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "next_page_id": self.next_page_id
        }
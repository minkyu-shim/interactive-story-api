from . import db


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='published')

    # Relationship: One story has many pages
    pages = db.relationship('Page', backref='story', cascade="all, delete-orphan")

    def to_dict(self):
        """Example: Converts a database row into a Python dictionary for JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    is_ending = db.Column(db.Boolean, default=False)
    ending_label = db.Column(db.String(50), nullable=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)

    # Relationship: A page has many choices leading out
    choices = db.relationship('Choice', backref='source_page', foreign_keys='Choice.page_id')


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=True)
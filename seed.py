from app import create_app, db
from app.models import Story

app = create_app()

# seed db for testing since the db is currently empty with no stories
with app.app_context():
    # Clear existing data if you want a fresh start
    # db.drop_all()
    # db.create_all()

    s1 = Story(title="Elden Ring", description="good game", status="published")
    s2 = Story(title="Lies of P", description="perry perry", status="published")

    db.session.add_all([s1, s2])
    db.session.commit()
    print("Database seeded with two stories!")
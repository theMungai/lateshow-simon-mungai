# seed.py
import csv
from app import app, db
from models import Episode, Guest

with app.app_context():
    db.drop_all()
    db.create_all()

    with open('seed.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            episode = Episode(date=row['date'], number=row['number'])
            db.session.add(episode)

    db.session.commit()

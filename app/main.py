#nain.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config.from_object('app.config.Config')

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# ROUTES
@app.route('/episodes')
def episodes():
    eps = Episode.query.all()
    return jsonify([ep.to_dict() for ep in eps])


@app.route('/episodes/<int:id>')
def episode_by_id(id):
    ep = Episode.query.get(id)
    if not ep:
        return jsonify({'error': 'Episode not found'}), 404

    return jsonify({
        'id': ep.id,
        'date': ep.date,
        'number': ep.number,
        'appearances': [
            {
                'id': a.id,
                'rating': a.rating,
                'guest_id': a.guest_id,
                'episode_id': a.episode_id,
                'guest': a.guest.to_dict()
            } for a in ep.appearances
        ]
    })


@app.route('/guests')
def guests():
    gs = Guest.query.all()
    return jsonify([g.to_dict() for g in gs])


@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    try:
        new_app = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        db.session.add(new_app)
        db.session.commit()

        return jsonify(new_app.to_dict()), 201

    except Exception as e:
        return jsonify({'errors': [str(e)]}), 400

app = app

if __name__ == '__main__':
    app.run(debug=True)
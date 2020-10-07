from pathlib import Path
import json

from project import create_app
from project.models import db, Room

app = create_app()
db.create_all(app=app)

with app.app_context():
    # Agregamos la data hard-coded (Salas)
    curr_dir = Path(__file__).resolve().parent
    with open(curr_dir.joinpath('data/room_data.json')) as file:
        rooms = json.load(file)['rooms']

    for room in rooms:
        new_room = Room(name=room['name'], id=room['id'], capacity=room['capacity'])
        db.session.add(new_room)
        db.session.commit()
 
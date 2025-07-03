from app import create_app
from app.models import db, Slot

app = create_app()

with app.app_context():
    db.create_all()
    # Add initial slots if none exist
    if Slot.query.count() == 0:
        times = ['09:00', '10:00', '11:00', '14:00']
        for t in times:
            slot = Slot(time=t, available=True)
            db.session.add(slot)
        db.session.commit()
        print('Database initialized and slots added.')
    else:
        print('Slots already exist. No changes made.') 

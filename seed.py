from app import app
from models import db, Hotel, User

with app.app_context():
    # Add sample hotels
    hotel1 = Hotel(name="Hotel Taj", city="Mumbai", price=5000, rating=4.8)
    hotel2 = Hotel(name="The Oberoi", city="Mumbai", price=7000, rating=4.9)
    hotel3 = Hotel(name="Marriott", city="Delhi", price=4500, rating=4.6)

    db.session.add_all([hotel1, hotel2, hotel3])
    db.session.commit()

    print("Sample hotels added!")

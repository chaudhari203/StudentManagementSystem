from app import app
from models.student import db, Admin

with app.app_context():
    admin = Admin.query.filter_by(username="admin").first()

    if not admin:
        admin = Admin(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully!")
    else:
        print("Admin already exists.")
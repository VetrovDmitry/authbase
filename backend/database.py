from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Base:
    def update(self):
        db.session.commit()
        return self

    def upload(self):
        db.session.add(self)
        return self.update()

    def delete(self):
        db.session.delete(self)
        self.update()
        return

"""
Goal: simplify the code when interacting with entities

Usage when declaring a model:

import db
class MyEntity(db.Model, CRUDMixin):
    id = db.Column('myID', db.Integer, primary_key=True)
    data = db.Column('myData', db.String(255))

MyTableEntity.create(data="abc")

my = MyTableEntity(data="abc")
db.session.save(my, commit=False)

found = MyTableEntity.get_by_id(1) is not None
"""

from app.main import db

class CRUDMixin(object):
    """ Helper class flask-sqlalchemy entities """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, basestring) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None


    @classmethod
    def create(cls, **kwargs):
        """ Helper for session.add() + session.commit() """
        instance = cls(**kwargs)
        return instance.save()


    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self


    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self


    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

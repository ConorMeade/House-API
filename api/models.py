from . import db


class House(db.Model):
    # taken from houses.csv
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(20))
    street = db.Column(db.String(30))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zip = db.Column(db.String(6))
    propertyType = db.Column(db.String(30))

    # create a readable string format for a db entry
    def __repr__(self):
        return f"House('{self.id}', '{self.firstName}', '{self.lastName}', '{self.street}' , '{self.city}', '{self.state}', '{self.zip}', '{self.propertyType}')"
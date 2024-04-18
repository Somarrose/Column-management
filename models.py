from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.Integer, nullable=False, unique=True)

class ColumnInfo(db.Model):
    sn = db.Column(db.String(100), primary_key=True)
    supplier = db.Column(db.String(100), nullable=False)
    dimension = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

class UsageEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    column_id = db.Column(db.String(100), db.ForeignKey('column_info.sn'), nullable=False)
    project = db.Column(db.String(100), nullable=False)
    technique = db.Column(db.String(100), nullable=False)
    mobile_phase_a = db.Column(db.String(100), default=False)
    mobile_phase_b = db.Column(db.String(100), default=False)

    user = db.relationship('User', backref=db.backref('usage_entries', lazy=True))
    column = db.relationship('ColumnInfo', backref=db.backref('usage_entries', lazy=True))

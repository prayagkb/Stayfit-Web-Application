from .database import db

class User_to_Tracker(db.Model):
    __tablename__ = 'user_to_tracker'
    ut_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    user_uid = db.Column(db.Integer,db.ForeignKey("user.userid"),nullable=False)
    tracker_tid = db.Column(db.Integer,db.ForeignKey("tracker.t_id"),nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact=db.Column(db.Integer,nullable=True)
    subscriber = db.relationship('Tracker',secondary = 'user_to_tracker',backref='trackers')


class Tracker(db.Model):
    __tablename__ = 'tracker'
    t_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    t_name = db.Column(db.String, nullable=False)
    t_dscp = db.Column(db.String)
    t_type = db.Column(db.String, nullable=False)
    t_owner = db.Column(db.Integer,db.ForeignKey("user.userid"),nullable=False)
    t_values =db.Column(db.String)

class LogTable(db.Model):
    __tablename__ = 'log_table'
    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    userlog_id = db.Column(db.Integer, db.ForeignKey("user.userid"),nullable=False)
    tlog_id = db.Column(db.Integer, db.ForeignKey("tracker.t_id"),nullable=False)
    timestamp=db.Column(db.String)
    log_note=db.Column(db.String)
    log_value=db.Column(db.String, nullable=False)
from dev.extensions import db


class TrainingSession(db.Model):
    __tablename__ = 'training_sessions'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.String(50), nullable=False)
    vehicle_id = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='ongoing')
    # A session can have multiple feedbacks
    feedbacks = db.relationship('DrivingFeedback', backref='session', lazy=True)
    # A session can have only one report
    report = db.relationship('TrainingReport', uselist=False, backref='session')


class DrivingFeedback(db.Model):
    __tablename__ = 'driving_feedback'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('training_sessions.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    details = db.Column(db.String(255))


class TrainingReport(db.Model):
    __tablename__ = 'training_reports'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('training_sessions.id'), nullable=False, unique=True)
    summary = db.Column(db.String(255))
    score = db.Column(db.Float)
    recommendations = db.Column(db.String(255))

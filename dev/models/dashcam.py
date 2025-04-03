from dev.extensions import db


class DashcamAlert(db.Model):
    __tablename__ = 'dashcam_alerts'
    id = db.Column(db.Integer, primary_key=True)
    dashcam_id = db.Column(db.String(50), nullable=False)
    vehicle_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    lane_deviation = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    severity = db.Column(db.String(20), nullable=False)


class SafetyReport(db.Model):
    __tablename__ = 'safety_reports'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(50), nullable=False)
    total_alerts = db.Column(db.Integer, nullable=False)
    alerts_summary = db.Column(db.String(255))
    safety_score = db.Column(db.Float)
    recommendations = db.Column(db.String(255))

from dev.extensions import db


class RoadAssessmentRequest(db.Model):
    __tablename__ = 'road_assessment_requests'
    id = db.Column(db.Integer, primary_key=True)
    road_id = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    media_url = db.Column(db.String(255), nullable=False)
    additional_notes = db.Column(db.String(255))


class RoadAssessmentReport(db.Model):
    __tablename__ = 'road_assessment_reports'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('road_assessment_requests.id'), nullable=False, unique=True)
    faded = db.Column(db.Boolean, default=False)
    broken = db.Column(db.Boolean, default=False)
    missing = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(255))
    overall_rating = db.Column(db.Float)
    recommendations = db.Column(db.String(255))
    generated_at = db.Column(db.DateTime)

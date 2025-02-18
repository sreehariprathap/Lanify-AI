from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields

from dev.extensions import ma, db
from dev.models.dashcam import DashcamAlert, SafetyReport

blp = Blueprint('Dashcam', __name__, url_prefix='/api/dashcam', description='Low-Cost Smart Dashcam API')


class DashcamAlertSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DashcamAlert
        load_instance = True

    id = fields.Int(dump_only=True)
    dashcam_id = fields.Str(required=True)
    vehicle_id = fields.Str(required=True)
    timestamp = fields.DateTime(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    lane_deviation = fields.Float(required=True)
    description = fields.Str()
    severity = fields.Str(required=True)


class SafetyReportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SafetyReport
        load_instance = True

    id = fields.Int(dump_only=True)
    vehicle_id = fields.Str(required=True)
    total_alerts = fields.Int(required=True)
    alerts_summary = fields.Str()
    safety_score = fields.Float()
    recommendations = fields.Str()


class DashcamAlertQueryArgsSchema(ma.Schema):
    vehicle_id = fields.Str(required=False)


@blp.route('/alerts')
class DashcamAlertList(MethodView):

    @blp.arguments(DashcamAlertQueryArgsSchema, location='query')
    @blp.response(200, DashcamAlertSchema(many=True))
    def get(self, query_args):
        """
        Get all dashcam alerts, or filter by vehicle_id
        """
        vehicle_id = query_args.get('vehicle_id')
        filters = []
        if vehicle_id:
            filters.append(DashcamAlert.vehicle_id.ilike(f'%{vehicle_id}%'))
        return DashcamAlert.query.filter(*filters).all()

    @blp.arguments(DashcamAlertSchema)
    @blp.response(201, DashcamAlertSchema)
    def post(self, new_alert):
        """
        Create a new dashcam alert
        """
        db.session.add(new_alert)
        db.session.commit()
        return new_alert


@blp.route('/alerts/<int:alert_id>')
class DashcamAlertById(MethodView):

    @blp.response(200, DashcamAlertSchema)
    def get(self, alert_id):
        """
        Get details of a dashcam alert by ID
        """
        return DashcamAlert.query.get_or_404(alert_id)

    @blp.arguments(DashcamAlertSchema)
    @blp.response(200, DashcamAlertSchema)
    def put(self, updated_alert, alert_id):
        """
        Update a dashcam alert by ID
        """
        alert = DashcamAlert.query.get_or_404(alert_id)
        alert.timestamp = updated_alert.timestamp
        alert.latitude = updated_alert.latitude
        alert.longitude = updated_alert.longitude
        alert.lane_deviation = updated_alert.lane_deviation
        alert.description = updated_alert.description
        alert.severity = updated_alert.severity
        db.session.commit()
        return alert

    @blp.response(204)
    def delete(self, alert_id):
        """
        Delete a dashcam alert by ID
        """
        alert = DashcamAlert.query.get_or_404(alert_id)
        db.session.delete(alert)
        db.session.commit()
        return None


@blp.route('/safety-report/<string:vehicle_id>')
class SafetyReportAPI(MethodView):

    @blp.response(200, SafetyReportSchema)
    def get(self, vehicle_id):
        """
        Get safety report for a specific vehicle
        """
        report = SafetyReport.query.filter_by(vehicle_id=vehicle_id).first()
        if not report:
            blp.abort(404, message="Safety report not found")
        return report


@blp.route('/safety-reports')
class FleetSafetyReportsAPI(MethodView):

    @blp.response(200, SafetyReportSchema(many=True))
    def get(self):
        """
        Get safety reports for all vehicles (fleet-level)
        """
        return SafetyReport.query.all()

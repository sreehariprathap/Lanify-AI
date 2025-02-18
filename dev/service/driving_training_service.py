from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields

from dev.extensions import ma, db
from dev.models.driving_training import TrainingSession, DrivingFeedback, \
    TrainingReport

blp = Blueprint('DrivingTraining', __name__, url_prefix='/api/driving-training',
                description='Driving Training System API')


class TrainingSessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingSession
        load_instance = True

    id = fields.Int(dump_only=True)
    driver_id = fields.Str(required=True)
    vehicle_id = fields.Str(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(allow_none=True)
    status = fields.Str(dump_only=True)


class DrivingFeedbackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DrivingFeedback
        load_instance = True

    id = fields.Int(dump_only=True)
    session_id = fields.Int(required=True, load_only=True)
    timestamp = fields.DateTime(required=True)
    event_type = fields.Str(required=True)
    severity = fields.Str(required=True)
    details = fields.Str()


class TrainingReportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingReport
        load_instance = True

    id = fields.Int(dump_only=True)
    session_id = fields.Int(required=True)
    summary = fields.Str()
    score = fields.Float()
    recommendations = fields.Str()


class TrainingSessionQueryArgsSchema(ma.Schema):
    driver_id = fields.Str(required=False)
    vehicle_id = fields.Str(required=False)


@blp.route('/sessions')
class TrainingSessionList(MethodView):

    @blp.arguments(TrainingSessionQueryArgsSchema, location='query')
    @blp.response(200, TrainingSessionSchema(many=True))
    def get(self, query_args):
        """
        Get all training sessions, or filter by driver_id and/or vehicle_id
        """
        driver_id = query_args.get('driver_id')
        vehicle_id = query_args.get('vehicle_id')
        filters = []
        if driver_id:
            filters.append(TrainingSession.driver_id.ilike(f'%{driver_id}%'))
        if vehicle_id:
            filters.append(TrainingSession.vehicle_id.ilike(f'%{vehicle_id}%'))
        return TrainingSession.query.filter(*filters).all()

    @blp.arguments(TrainingSessionSchema)
    @blp.response(201, TrainingSessionSchema)
    def post(self, new_session):
        """
        Create a new training session
        """
        db.session.add(new_session)
        db.session.commit()
        return new_session


@blp.route('/sessions/<int:session_id>')
class TrainingSessionById(MethodView):

    @blp.response(200, TrainingSessionSchema)
    def get(self, session_id):
        """
        Get training session details by ID
        """
        return TrainingSession.query.get_or_404(session_id)

    @blp.arguments(TrainingSessionSchema)
    @blp.response(200, TrainingSessionSchema)
    def put(self, updated_session, session_id):
        """
        Update a training session (e.g. end the session)
        """
        session = TrainingSession.query.get_or_404(session_id)
        session.end_time = updated_session.end_time
        session.status = updated_session.status or 'completed'
        db.session.commit()
        return session

    @blp.response(204)
    def delete(self, session_id):
        """
        Delete a training session
        """
        session = TrainingSession.query.get_or_404(session_id)
        db.session.delete(session)
        db.session.commit()
        return None


@blp.route('/sessions/<int:session_id>/feedback')
class DrivingFeedbackAPI(MethodView):

    @blp.arguments(DrivingFeedbackSchema)
    @blp.response(201, DrivingFeedbackSchema)
    def post(self, feedback_data, session_id):
        """
        Submit driving feedback for a specific session
        """
        feedback_data.session_id = session_id
        db.session.add(feedback_data)
        db.session.commit()
        return feedback_data

    @blp.response(200, DrivingFeedbackSchema(many=True))
    def get(self, session_id):
        """
        Get all feedbacks for a specific session
        """
        feedbacks = DrivingFeedback.query.filter_by(session_id=session_id).all()
        return feedbacks


@blp.route('/sessions/<int:session_id>/report')
class TrainingReportAPI(MethodView):

    @blp.response(200, TrainingReportSchema)
    def get(self, session_id):
        """
        Get training report for a specific session
        """
        report = TrainingReport.query.filter_by(session_id=session_id).first()
        if not report:
            blp.abort(404, message="Report not found")
        return report

    @blp.arguments(TrainingReportSchema)
    @blp.response(201, TrainingReportSchema)
    def post(self, report_data, session_id):
        """
        Create a training report for a specific session
        """
        report_data.session_id = session_id
        db.session.add(report_data)
        db.session.commit()
        return report_data

    @blp.arguments(TrainingReportSchema)
    @blp.response(200, TrainingReportSchema)
    def put(self, report_data, session_id):
        """
        Update training report for a specific
        """
        report = TrainingReport.query.filter_by(session_id=session_id).first()
        if not report:
            blp.abort(404, message="Report not found")
        report.summary = report_data.summary
        report.score = report_data.score
        report.recommendations = report_data.recommendations
        db.session.commit()
        return report

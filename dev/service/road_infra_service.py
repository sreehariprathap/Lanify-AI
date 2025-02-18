from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields

from dev.extensions import ma, db
from dev.models.road_infra import RoadAssessmentRequest, RoadAssessmentReport

blp = Blueprint('RoadInfrastructure', __name__, url_prefix='/api/road-infra/assessment',
                description='Road Infrastructure Assessment API')


class RoadAssessmentRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoadAssessmentRequest
        load_instance = True

    id = fields.Int(dump_only=True)
    road_id = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    timestamp = fields.DateTime(required=True)
    media_url = fields.Str(required=True)
    additional_notes = fields.Str()


class RoadAssessmentReportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoadAssessmentReport
        load_instance = True

    id = fields.Int(dump_only=True)
    request_id = fields.Int(required=True)
    faded = fields.Bool()
    broken = fields.Bool()
    missing = fields.Bool()
    notes = fields.Str()
    overall_rating = fields.Float()
    recommendations = fields.Str()
    generated_at = fields.DateTime()


class RoadAssessmentQueryArgsSchema(ma.Schema):
    road_id = fields.Str(required=False)
    startTime = fields.DateTime(required=False)
    endTime = fields.DateTime(required=False)


@blp.route('/upload')
class RoadAssessmentUploadAPI(MethodView):

    @blp.arguments(RoadAssessmentRequestSchema)
    @blp.response(201, RoadAssessmentRequestSchema)
    def post(self, assessment_data):
        """
        Submit a new road assessment request
        """
        db.session.add(assessment_data)
        db.session.commit()
        return assessment_data


@blp.route('/<int:assessment_id>')
class RoadAssessmentById(MethodView):

    @blp.response(200, RoadAssessmentReportSchema)
    def get(self, assessment_id):
        """
        Get road assessment report details by ID
        """
        report = RoadAssessmentReport.query.filter_by(id=assessment_id).first()
        if not report:
            blp.abort(404, message="Assessment report not found")
        return report

    @blp.arguments(RoadAssessmentRequestSchema)
    @blp.response(200, RoadAssessmentRequestSchema)
    def put(self, updated_request, assessment_id):
        """
        Upda te road assessment request (e.g. update media data or add additional notes)
        """
        request_obj = RoadAssessmentRequest.query.get_or_404(assessment_id)
        request_obj.media_url = updated_request.media_url
        request_obj.timestamp = updated_request.timestamp
        request_obj.additional_notes = updated_request.additional_notes
        db.session.commit()
        return request_obj

    @blp.response(204)
    def delete(self, assessment_id):
        """
        Delete road assessment request
        """
        report = RoadAssessmentReport.query.get_or_404(assessment_id)
        db.session.delete(report)
        db.session.commit()
        return None


@blp.route('/reports')
class RoadAssessmentReportListAPI(MethodView):

    @blp.arguments(RoadAssessmentQueryArgsSchema, location='query')
    @blp.response(200, RoadAssessmentReportSchema(many=True))
    def get(self, query_args):
        """
        Get a list of road assessment reports, optionally filtered by road_id and time interval
        """
        road_id = query_args.get('road_id')
        filters = []
        if road_id:
            filters.append(RoadAssessmentRequest.road_id.ilike(f'%{road_id}%'))
        return RoadAssessmentReport.query.filter(*filters).all()


@blp.route('/summary')
class RoadAssessmentSummaryAPI(MethodView):

    @blp.response(200)
    def get(self):
        """
        Get summary statistics for road assessments
        """
        summary = {
            "region": "default",
            "totalAssessments": RoadAssessmentReport.query.count(),
            "averageRating": 0,
            "commonIssues": "faded, broken",
            "recommendations": "Increase maintenance frequency"
        }
        return summary

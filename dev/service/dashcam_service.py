import hashlib
import os
import tempfile

import eventlet
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_socketio import SocketIO
from marshmallow import fields
from moviepy.video.io.VideoFileClip import VideoFileClip

from dev.ai_models.lane_marking_overlay import LaneDetector
from dev.extensions import ma, db
from dev.models.dashcam import DashcamAlert, SafetyReport

# Initialize Flask Blueprint
blp = Blueprint('Dashcam', __name__, url_prefix='/api/dashcam', description='Low-Cost Smart Dashcam API')

# Initialize SocketIO (Assuming 'app' is defined in your main Flask app)
socketio = SocketIO(cors_allowed_origins="*")  # Will attach this to the Flask app later


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
        Create a new dashcam alert and emit an event every 10 seconds for demonstration purposes
        """
        db.session.add(new_alert)
        db.session.commit()

        def emit_alert_repeatedly():
            while True:
                socketio.emit("alertEvent", {
                    "id": new_alert.id,
                    "dashcam_id": new_alert.dashcam_id,
                    "vehicle_id": new_alert.vehicle_id,
                    "timestamp": str(new_alert.timestamp),
                    "latitude": new_alert.latitude,
                    "longitude": new_alert.longitude,
                    "lane_deviation": new_alert.lane_deviation,
                    "description": new_alert.description,
                    "severity": new_alert.severity
                })
                eventlet.sleep(10)

        eventlet.spawn_n(emit_alert_repeatedly)

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


class VideoUploadSchema(ma.Schema):
    vehicle_id = fields.Str(required=True)
    dashcam_id = fields.Str(required=True)


class VideoResponseSchema(ma.Schema):
    safety_report = fields.Nested(SafetyReportSchema)
    video_url = fields.Str()


@blp.route('/upload-video')
class DashcamVideoUpload(MethodView):

    @staticmethod
    def process_lane_detection_video(input_video_path, output_video_path):
        # Initialize the LaneDetector with the specified model
        self_dir = os.path.dirname(__file__)
        model_path = os.path.abspath(os.path.join(self_dir, '../ai_models/cnn_lane_detection_model.h5'))
        lane_detector = LaneDetector(model_path)

        # Load input video and process frame-by-frame
        input_clip = VideoFileClip(input_video_path)
        processed_clip = input_clip.fl_image(lane_detector.detect_lane)

        # Write the output video
        processed_clip.write_videofile(output_video_path, audio=False)

    @blp.arguments(VideoUploadSchema, location='form')
    @blp.response(201, VideoResponseSchema)
    def post(self, upload_data):
        """
        Upload a dashcam video for processing

        Returns a safety report and the URL to the processed video
        """
        if 'video' not in request.files:
            blp.response(400, description="No video file provided")

        file = request.files['video']
        vehicle_id = upload_data['vehicle_id']
        dashcam_id = upload_data['dashcam_id']

        # Create temp directory if it doesn't exist
        temp_dir = tempfile.gettempdir()
        file_hash = hashlib.md5(file.read()).hexdigest()
        file_extension = os.path.splitext(file.filename)[1]
        temp_file_path = os.path.join(temp_dir, f"{file_hash}{file_extension}")

        # Save uploaded file to temp location
        file.seek(0)
        file.save(temp_file_path)

        # Process the video and save to destination folder
        output_dir = '/app/frontend/dashcam/lane-videos'
        os.makedirs(output_dir, exist_ok=True)
        output_filename = f"{file_hash}.mp4"
        output_file_path = os.path.join(output_dir, output_filename)
        self.process_lane_detection_video(temp_file_path, output_file_path)

        # Generate a safety report
        # In a real scenario, this would be based on video analysis
        safety_report = SafetyReport(
            vehicle_id=vehicle_id,
            total_alerts=0,  # Placeholder
            alerts_summary=f"Video analysis completed for dashcam {dashcam_id}",
            safety_score=0.0,  # Placeholder
            recommendations="No recommendations available yet"
        )

        db.session.add(safety_report)
        db.session.commit()

        # Generate video URL
        video_url = f"/dashcam/lane-videos/{output_filename}"

        # Return response with safety report and video URL
        return {
            "safety_report": SafetyReportSchema().dump(safety_report),
            "video_url": video_url
        }

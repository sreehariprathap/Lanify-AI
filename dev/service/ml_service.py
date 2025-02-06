from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields

from dev.extensions import ma, db
from dev.models.student import Student

blp = Blueprint('ML', __name__, url_prefix='/api', description='Test API')


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    student_number = fields.Int(required=True)


class StudentQueryArgsSchema(ma.Schema):
    name = fields.Str(required=False)
    student_number = fields.Int(required=False)


@blp.route('/service')
class StudentList(MethodView):

    @blp.arguments(StudentQueryArgsSchema, location='query')
    @blp.response(200, StudentSchema(many=True))
    def get(self, query_args):
        """
        Get all students, or filter by name and/or student number
        """
        name = query_args.get('name')
        student_number = query_args.get('student_number')

        # build filters
        filters = []
        if name:
            filters.append(Student.name.ilike(f'%{name}%'))
        if student_number:
            filters.append(Student.student_number.ilike(f'%{student_number}%'))

        return Student.query.filter(*filters).all()

    @blp.arguments(StudentSchema)
    @blp.response(201, StudentSchema)
    def post(self, student):
        """
        Create a new student
        """
        db.session.add(student)
        db.session.commit()
        return student


@blp.route('/service/<int:student_id>')
class StudentById(MethodView):

    @blp.response(200, StudentSchema)
    def get(self, student_id):
        """
        Get a student by ID
        """
        return Student.query.get_or_404(student_id)

    @blp.arguments(StudentSchema)
    @blp.response(200, StudentSchema)
    def put(self, new_student, student_id):
        """
        Update a student by ID
        """
        student = Student.query.get_or_404(student_id)

        student.name = new_student.name
        student.student_number = new_student.student_number

        db.session.commit()
        return student

    @blp.response(204)
    def delete(self, student_id):
        """
        Delete a student by ID
        """
        student = Student.query.get_or_404(student_id)

        db.session.delete(student)
        db.session.commit()
        return None

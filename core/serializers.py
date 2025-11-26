from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Timetable, Session

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_student', 'is_professor']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class TimetableSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = Timetable
        fields = '__all__'


class StartSessionSerializer(serializers.Serializer):
    """Serializer for starting a new session"""
    timetable_id = serializers.IntegerField(required=True)
    
    def validate_timetable_id(self, value):
        """Validate that timetable exists"""
        try:
            Timetable.objects.get(id=value)
        except Timetable.DoesNotExist:
            raise serializers.ValidationError("Timetable with this ID does not exist.")
        return value


class SessionSerializer(serializers.ModelSerializer):
    """Serializer for Session objects (QR and attendance data)"""
    timetable_info = serializers.SerializerMethodField()
    course_info = serializers.SerializerMethodField()
    attendance_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Session
        fields = '__all__'
        read_only_fields = ['started_at', 'qr_code', 'qr_secret', 'nonce']
    
    def get_timetable_info(self, obj):
        """Return timetable details"""
        return {
            'id': obj.timetable.id,
            'day_of_week': obj.timetable.day_of_week,
            'day_of_week_display': obj.timetable.get_day_of_week_display(),
            'start_time': obj.timetable.start_time,
            'end_time': obj.timetable.end_time,
            'room': obj.timetable.room,
        }
    
    def get_course_info(self, obj):
        """Return course details"""
        return {
            'id': obj.timetable.course.id,
            'name': obj.timetable.course.name,
            'code': obj.timetable.course.code,
        }
    
    def get_attendance_count(self, obj):
        """Return count of attendance records for this session"""
        return obj.attendances.count()



from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import secrets
import hmac
import hashlib
import uuid
from .models import Course, Timetable, Session
from .serializers import (
    UserSerializer, CourseSerializer, TimetableSerializer, 
    SessionSerializer, StartSessionSerializer
)

User = get_user_model()


def compute_sig(session_id, nonce, expires_at, qr_secret):
    """
    Compute HMAC signature for QR code using session_id + nonce + expires_at.
    
    Args:
        session_id: Session ID (integer)
        nonce: Random nonce string
        expires_at: Expiration datetime
        qr_secret: Secret key for HMAC signing
    
    Returns:
        HMAC signature (hex string)
    """
    # Convert expires_at to timestamp string
    expires_timestamp = str(int(expires_at.timestamp()))
    
    # Create data string: session_id:nonce:expires_at
    data = f"{session_id}:{nonce}:{expires_timestamp}"
    
    # Compute HMAC-SHA256 signature
    signature = hmac.new(
        qr_secret.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return signature

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


class TimetableViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Timetable records (admin side).
    """
    queryset = Timetable.objects.all().select_related('course')
    serializer_class = TimetableSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Optionally filter by course if course_id is provided in query params.
        """
        queryset = Timetable.objects.all().select_related('course')
        course_id = self.request.query_params.get('course_id', None)
        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)
        return queryset


class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing Session objects (for QR and attendance data).
    Read-only to view session information, QR codes, and attendance records.
    """
    queryset = Session.objects.all().select_related('timetable', 'timetable__course')
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter sessions by various query parameters:
        - timetable_id: Filter by specific timetable
        - course_id: Filter by course (through timetable)
        - is_active: Filter by active status
        - qr_code: Find specific session by QR code
        """
        queryset = Session.objects.all().select_related('timetable', 'timetable__course')
        
        timetable_id = self.request.query_params.get('timetable_id', None)
        if timetable_id is not None:
            queryset = queryset.filter(timetable_id=timetable_id)
        
        course_id = self.request.query_params.get('course_id', None)
        if course_id is not None:
            queryset = queryset.filter(timetable__course_id=course_id)
        
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active_bool = is_active.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(is_active=is_active_bool)
        
        qr_code = self.request.query_params.get('qr_code', None)
        if qr_code is not None:
            queryset = queryset.filter(qr_code=qr_code)
        
        return queryset


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def start_session(request):
    """
    Start a new session for a timetable.
    Automatically generates QR code and secret using HMAC.
    """
    serializer = StartSessionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    timetable_id = serializer.validated_data['timetable_id']
    
    try:
        timetable = Timetable.objects.select_related('course').get(id=timetable_id)
    except Timetable.DoesNotExist:
        return Response(
            {'error': 'Timetable not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Generate QR secret (random secure string)
    qr_secret = secrets.token_urlsafe(32)
    
    # Generate random nonce for security
    nonce = secrets.token_urlsafe(32)
    
    # Calculate expiration time (default: 2 hours from now)
    expires_at = timezone.now() + timedelta(hours=2)
    
    # Create session first (to get session_id)
    # Use temporary unique QR code, will be updated after signature computation
    temp_qr_code = f"temp_{uuid.uuid4().hex}"
    session = Session.objects.create(
        timetable=timetable,
        qr_code=temp_qr_code,  # Temporary unique value, will be updated
        qr_secret=qr_secret,
        nonce=nonce,
        is_active=True,
        expires_at=expires_at
    )
    
    # Compute HMAC signature using session_id + nonce + expires_at
    hmac_signature = compute_sig(
        session_id=session.id,
        nonce=nonce,
        expires_at=expires_at,
        qr_secret=qr_secret
    )
    
    # Generate QR code: session_id:nonce:expires_timestamp:signature
    expires_timestamp = str(int(expires_at.timestamp()))
    qr_code = f"{session.id}:{nonce}:{expires_timestamp}:{hmac_signature}"
    
    # Update session with the generated QR code
    session.qr_code = qr_code
    session.save(update_fields=['qr_code'])
    
    # Return created session with full details
    response_serializer = SessionSerializer(session)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)

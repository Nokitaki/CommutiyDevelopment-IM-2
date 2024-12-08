# calendar_events/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import CalendarEvent
import json
from datetime import datetime

@login_required
@require_POST
def create_event(request):
    try:
        data = json.loads(request.body)
        event = CalendarEvent.objects.create(
            title=data['title'],
            description=data.get('description', ''),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
            time=datetime.strptime(data['time'], '%H:%M').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M').time() if data.get('end_time') else None,
            created_by=request.user
        )
        return JsonResponse({
            'status': 'success',
            'event': {
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'date': event.date.strftime('%Y-%m-%d'),
                'end_date': event.end_date.strftime('%Y-%m-%d') if event.end_date else None,
                'time': event.time.strftime('%H:%M'),
                'end_time': event.end_time.strftime('%H:%M') if event.end_time else None
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def get_events(request):
    events = CalendarEvent.objects.filter(created_by=request.user)
    return JsonResponse({
        'events': [{
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'end_date': event.end_date.strftime('%Y-%m-%d') if event.end_date else None,
            'time': event.time.strftime('%H:%M'),
            'end_time': event.end_time.strftime('%H:%M') if event.end_time else None
        } for event in events]
    })
    
@login_required
@require_POST
def delete_event(request, event_id):
    try:
        event = CalendarEvent.objects.get(id=event_id, created_by=request.user)
        event.delete()
        return JsonResponse({'status': 'success'})
    except CalendarEvent.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Event not found'}, status=404)
    

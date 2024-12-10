# chat/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Message
from users.models import User
import json
from datetime import datetime
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.timezone import localtime

@login_required
def chat_home(request):
    """Main chat interface view"""
    # Get all users except the current user
    all_users = User.objects.exclude(userId=request.user.userId).order_by('firstname')
    return render(request, 'chat/home.html', {'all_users': all_users})

@login_required
def get_unread_count(request):
    unread_count = Message.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    return JsonResponse({'unread_count': unread_count})

@login_required
def get_user_contacts(user):
    """Get all users who have exchanged messages with the current user"""
    sent_to = Message.objects.filter(sender=user).values_list('recipient', flat=True)
    received_from = Message.objects.filter(recipient=user).values_list('sender', flat=True)
    contact_ids = set(list(sent_to) + list(received_from))
    return User.objects.filter(userId__in=contact_ids).order_by('firstname')

# chat/views.py

@login_required
def get_contacts(request):
    try:
        messages = Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).select_related('sender', 'recipient').order_by('-timestamp')
        
        # Use a dictionary to keep track of the latest message for each contact
        contacts_dict = {}
        
        for message in messages:
            # Determine if the contact is the sender or recipient
            contact = message.recipient if message.sender == request.user else message.sender
            contact_id = str(contact.userId)
            
            # Only process if this is a new contact or a more recent message
            if contact_id not in contacts_dict:
                # Get unread count for this contact
                unread_count = Message.objects.filter(
                    sender=contact,
                    recipient=request.user,
                    is_read=False
                ).count()
                
                contacts_dict[contact_id] = {
                    'userId': contact_id,
                    'firstname': contact.firstname,
                    'lastname': contact.lastname,
                    'lastMessage': message.content,
                    'lastMessageTime': localtime(message.timestamp).strftime('%I:%M %p'),
                    'unreadCount': unread_count
                }
        
        # Convert dictionary values to list
        contacts_list = list(contacts_dict.values())
        
        return JsonResponse({'contacts': contacts_list})
        
    except Exception as e:
        # Log the error (you should set up proper logging)
        print(f"Error in get_contacts: {str(e)}")
        return JsonResponse(
            {'error': 'An error occurred while fetching contacts'}, 
            status=500
        )

@login_required
def get_messages(request, user_id):
    """Get message history with a specific user"""
    other_user = get_object_or_404(User, userId=user_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        Q(sender=other_user) & Q(recipient=request.user)
    ).order_by('timestamp')

    messages_data = [{
        'id': msg.id,  # Add this line
        'content': msg.content,
        'sender_id': str(msg.sender.userId),
        'timestamp': localtime(msg.timestamp).strftime('%I:%M %p'),
        'is_unsent': msg.is_unsent  # Add this line
    } for msg in messages]

    return JsonResponse({'messages': messages_data})

@login_required
def send_message(request):
    """Send a new message"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        recipient = get_object_or_404(User, userId=data['recipient_id'])
        
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content=data['content']
        )

        return JsonResponse({
            'status': 'success',
            'message': {
                'id': message.id,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%I:%M %p'),
            }
        })
    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@login_required
@require_POST
def mark_messages_read(request, user_id):
    Message.objects.filter(
        sender_id=user_id,
        recipient=request.user,
        is_read=False
    ).update(is_read=True)
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def edit_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id, sender=request.user)
        data = json.loads(request.body)
        message.content = data['content']
        message.save()
        return JsonResponse({
            'status': 'success',
            'message': {
                'content': message.content,
                'timestamp': localtime(message.timestamp).strftime('%I:%M %p'),
            }
        })
    except Message.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)
    
@login_required
@require_POST
def unsend_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id, sender=request.user)
        message.is_unsent = True
        message.save()
        return JsonResponse({'status': 'success'})
    except Message.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Message not found or you do not have permission to unsend it'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
from django.shortcuts import render, redirect


# Create your views here.
from chat.models import ChatDialog, ChatMessage


def room(request, room_name):
    """Комната"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            cur_dialog = ChatDialog.objects.get(id=room_name).id
            messages = ChatMessage.objects.select_related('user').filter(dialog_id=room_name)
            return render(request, 'chat/room.html', {'messages': messages, 'room_name': cur_dialog})
        else:
            try:
                cur_dialog = ChatDialog.objects.get(id=request.user.id)
                messages = ChatMessage.objects.filter(dialog_id=cur_dialog)
                return render(request, 'chat/room.html', {
                    'room_name': room_name, 'cur_dialog': cur_dialog, 'messages': messages})
            except ChatDialog.DoesNotExist:
                cur_dialog = ChatDialog.objects.create(id=request.user.id, user_id=request.user.id)
                admin_message = ChatMessage.objects.get(dialog_id='5')
                print(cur_dialog)
                return render(request, 'chat/room.html', {
                    'room_name': room_name,
                    'cur_dialog': cur_dialog,
                    'admin_message': admin_message

                })
    else:
        return redirect('user:login_view')


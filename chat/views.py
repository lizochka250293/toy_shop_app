from django.shortcuts import render, redirect


# Create your views here.
from chat.models import ChatDialog, ChatMessage


def room(request, room_name):
    """Комната"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            cur_dialog = ChatDialog.objects.get(id=room_name).id
            messages = ChatMessage.objects.filter(dialog_id=room_name)
            return render(request, 'chat/room_2.html', {'messages': messages, 'cur_dialog': cur_dialog})
        else:
            try:
                cur_dialog = ChatDialog.objects.filter(user_id=request.user.id).last()
                messages = ChatMessage.objects.filter(dialog_id=cur_dialog.id)
                return render(request, 'chat/room_2.html', {
                    'room_name': room_name, 'messages': messages, 'cur_dialog': cur_dialog})
            except:
                cur_dialog = ChatDialog.objects.create(user_id=request.user.id)
                return render(request, 'chat/room_2.html', {
                    'room_name': room_name,
                    'cur_dialog': cur_dialog

                })
    else:
        return redirect('user:login_view')


def chat_close(request, cur_dialog):
    dialog = ChatDialog.objects.get(id=cur_dialog)
    dialog.is_active = False
    dialog.save()
    return redirect('admin_app:chats')

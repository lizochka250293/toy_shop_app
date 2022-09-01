from django.shortcuts import render, redirect


# Create your views here.
from chat.models import ChatDialog, ChatMessage


def room(request, room_name):
    """Комната"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            cur_dialog = ChatDialog.objects.get(id=room_name).id
            print(cur_dialog)
            messages = ChatMessage.objects.filter(dialog_id=room_name)
            return render(request, 'chat/room.html', {'messages': messages, 'room_name': cur_dialog})
        else:
            try:
                cur_dialog = ChatDialog.objects.get(id=request.user.id)
                if not cur_dialog.is_active:
                    message = ChatMessage.objects.get(dialog_id='5')
                    print(message)
                    return render(request, 'chat/room.html', {
                    'room_name': room_name, 'message': message, 'cur_dialog': cur_dialog})
                else:
                    print(cur_dialog.is_active)
                    messages = ChatMessage.objects.filter(dialog_id=cur_dialog.id)
                    return render(request, 'chat/room.html', {
                        'room_name': room_name, 'messages': messages, 'cur_dialog': cur_dialog})
            except ChatDialog.DoesNotExist:
                cur_dialog = ChatDialog.objects.create(id=request.user.id, user_id=request.user.id)
                print(cur_dialog)
                return render(request, 'chat/room.html', {
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

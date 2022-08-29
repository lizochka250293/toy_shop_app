from django.shortcuts import render, redirect


# Create your views here.
from chat.models import ChatDialog, ChatMessage


def room(request, room_name):
    """Комната"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            pass
        else:
            try:
                cur_dialog = ChatDialog.objects.filter(user_id=request.user.id).last()
                print(cur_dialog.is_active)
                messages = ChatMessage.objects.filter(dialog_id=cur_dialog.id)
                print(messages)
                return render(request, 'chat/room_2.html', {
                    'room_name': room_name, 'messages': messages})
            except:
                dialog = ChatDialog.objects.create(user_id=request.user.id)
                return render(request, 'chat/room_2.html', {
                    'room_name': room_name

                })
    else:
        return redirect('user:login_view')

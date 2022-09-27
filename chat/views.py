from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect


# Create your views here.
from django.views.generic import DetailView

from chat.models import ChatDialog, ChatMessage


class Room(DetailView):
    model = ChatDialog
    pk_url_kwarg = "room_name"
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['messages'] = ChatMessage.objects.select_related('user').filter(dialog_id=self.kwargs.get('room_name'))
        context['room_name'] = self.kwargs.get('room_name')
        print('room_name', context['room_name'])
        return context

    def get(self, request, *args, **kwargs):
        print(self.kwargs.get('room_name'))
        self.object = None
        if self.request.user.is_superuser:
            self.object = ChatDialog.objects.get(id=self.kwargs.get('room_name')).id
        else:
            try:
                self.object = ChatDialog.objects.get(id=self.request.user.id)
                print('cur', self.object)
            except ChatDialog.DoesNotExist:
                self.object = ChatDialog.objects.create(id=self.request.user.id, user_id=self.request.user.id)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

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

                })
    else:
        return redirect('user:login_view')


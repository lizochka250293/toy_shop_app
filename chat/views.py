from django.shortcuts import render, redirect


# Create your views here.


def room(request, room_name):
    if request.user.is_authenticated:
        return render(request, 'chat/room.html', {
            'room_name': room_name
        })
    else:
        return redirect('user:login_view')

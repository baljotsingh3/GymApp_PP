from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404



from Member.models import Member, Trainer
from gymApp.models import CustomUser


@login_required
def user_list(request):
    users = CustomUser.objects.exclude(id=request.user.id).exclude(is_superuser=True)
    context = {
        'users': users,
    }
    return render(request, 'chat/user_list.html', context)


@login_required
def user_profiles(request):
    users = CustomUser.objects.exclude(id=request.user.id).exclude(is_superuser=True)
    context = {
        'users': users,
    }
    return render(request, 'chat/user_profiles.html', context)




@login_required
def room(request, user_id):
    # Find the user you're chatting with
    chat_user = get_object_or_404(CustomUser, id=user_id)
    
    room_name = "_".join(sorted([str(request.user.id), str(chat_user.id)]))
    
    print(chat_user.username, room_name)
    return render(request, 'chat/collapsible_room.html', {
        'chat_user': chat_user,
        'room_name': room_name
    })
    
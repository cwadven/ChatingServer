from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


# Create your views here.
def index(request):
    return render(request, "home.html", {})


def chat_room(request, room):
    return render(request, "room.html", {'room_name_json': mark_safe(json.dumps(room)), })

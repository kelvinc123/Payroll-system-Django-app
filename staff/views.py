from django.shortcuts import render, get_object_or_404
from staff.models import Teacher
from django.utils import timezone
from datetime import datetime

# Create your views here.
def home(request):
    return render(request, 'home.html')

def help(request):
    return render(request, 'staff/help.html')

def index(request):
    teachers_list = Teacher.objects.all()
    context = {'teachers_list':teachers_list}
    return render(request, 'staff/index.html', context)


checked_in = {}
def check(request):

    if request.method == "POST":

        global checked_in
        full_name = request.POST.get('choice').replace("_", " ")
        teacher = get_object_or_404(Teacher, full_name = full_name)

        if teacher.full_name not in checked_in:
            button_word = "Check in"

        else:
            button_word = "Check out"

        context = {'teacher':teacher, "button_word":button_word}
        return render(request, 'staff/check.html', context)


    else:
        return render(request, 'home.html')


def success(request):

    if request.method == "POST":

        global checked_in
        full_name = request.POST.get('button').replace("_", " ")
        teacher = get_object_or_404(Teacher, full_name = full_name)


        if teacher.full_name not in checked_in:
            teacher_clock = teacher.teacherclock_set.create(clock_in = timezone.now())
            checked_in[teacher.full_name] = teacher_clock
            word = "checked in!"
        else:
            checked_in[teacher.full_name].clock_out = timezone.now()
            checked_in[teacher.full_name].save()
            del checked_in[teacher.full_name]
            word = "checked out!"

        context = {'word':word}
        return render(request, 'staff/success.html', context)

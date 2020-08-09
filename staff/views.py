from django.shortcuts import render, get_object_or_404
from staff.models import Teacher, TeacherClock
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


def check(request):

    if request.method == "POST":

        global checked_in
        full_name = request.POST.get('choice').replace("_", " ")
        teacher = get_object_or_404(Teacher, full_name = full_name)

        if len(TeacherClock.objects.filter(teacher = teacher, clock_out = None)) == 0:
            button_word = "Check in"
        else:
            button_word = "Check out"

        context = {'teacher':teacher, "button_word":button_word}
        return render(request, 'staff/check.html', context)


    else:
        return render(request, 'home.html')


def success(request):

    if request.method == "POST":

        full_name = request.POST.get('button').replace("_", " ")

        #query val from DB
        teacher = get_object_or_404(Teacher, full_name = full_name)

        if len(TeacherClock.objects.filter(teacher = teacher, clock_out = None)) == 0:
            teacher_clock = teacher.teacherclock_set.create(clock_in = timezone.now())
            word = "checked in!"
            clock_in = teacher_clock.clock_in
            clock_out = None
            td = None
        else:
            teacher_clock = TeacherClock.objects.get(teacher = teacher, clock_out = None)
            teacher_clock.clock_out = timezone.now()
            teacher_clock.save()
            word = "checked out!"
            clock_in = teacher_clock.clock_in
            clock_out = teacher_clock.clock_out
            td = clock_out - clock_in

        context = {"word":word, "clock_in": clock_in, "clock_out": clock_out, "duration": td}
        return render(request, 'staff/success.html', context)

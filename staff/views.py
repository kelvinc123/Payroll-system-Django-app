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


checked_in = {} #declare dict {key: value}
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
        td = None
        full_name = request.POST.get('button').replace("_", " ")

        #query val from DB
        teacher = get_object_or_404(Teacher, full_name = full_name)


        if teacher.full_name not in checked_in:
            teacher_clock = teacher.teacherclock_set.create(clock_in = timezone.now())
            checked_in[teacher.full_name] = teacher_clock

            word = "checked in!"
            clock_in = checked_in[teacher.full_name].clock_in
            clock_out = None
        else:
            checked_in[teacher.full_name].clock_out = timezone.now()
            checked_in[teacher.full_name].save()
            
            #accessing check-in and check-out time
            clock_in = checked_in[teacher.full_name].clock_in
            clock_out = checked_in[teacher.full_name].clock_out
            
            td = clock_out - clock_in
            #compute the duration of the duration of working hour

            del checked_in[teacher.full_name]
            
            word = "checked out!"
        #this value "checked out" is being passed to success.html
        context = {"word":word, "clock_in": clock_in, "clock_out": clock_out, "duration": td}
        return render(request, 'staff/success.html', context)

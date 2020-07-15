from django.db import models

# Create your models here.
class Teacher(models.Model):
    full_name = models.CharField("Full Name", max_length = 64, unique = True, primary_key = True)
    hourly_rate = models.DecimalField("Hourly Rate", max_digits = 5, decimal_places = 2)

    def __str__(self):
        return self.full_name

class TeacherClock(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(blank = True)

    def __str__(self):
        return self.teacher.full_name

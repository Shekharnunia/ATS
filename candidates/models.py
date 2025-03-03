from django.db import models


class GenderChoices(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    OTHER = "O", "Other"


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    # age = models.IntegerField()
    date_of_birth = models.DateField()  # age can be calculated from this field
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

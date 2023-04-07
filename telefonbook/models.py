
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


class Persone(models.Model):
    name = models.CharField("Contact name", max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_persone", default=1)

    def __str__(self):
        return self.name

    def all_phones_to_string(self):
        return ", ".join([phone.phone for phone in self.phones.all()])


class Phone(models.Model):
    phone = models.CharField("Phone", max_length=50, validators=[RegexValidator(regex=r"^(\+375|80)(29|25|44|33)$")])
    contact = models.ForeignKey(Persone, on_delete=models.CASCADE, related_name="phones")

    def __str__(self):
        return self.phone


class Importance(models.Model):
    color = models.CharField("Color", max_length=50)
    description = models.CharField("Description", max_length=50)

    def __str__(self):
        return self.description


class Record(models.Model):
    name = models.CharField("Name", max_length=200)
    description = models.CharField("Description", max_length=300, blank=True)
    colors = models.ForeignKey(Importance, on_delete=models.CASCADE, related_name="colors")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_record", default=1)

    def __str__(self):
        return self.name
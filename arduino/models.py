from __future__ import unicode_literals

from django.db import models

# Create your models here.

class CommandHistory(models.Model):
    command = models.CharField(max_length=200)
    command_date = models.DateTimeField('date of command')

    SUCCESS = 'SCS'
    COULD_NOT_CONNECT_TO_ARDUINO = 'CNC'
    COMMAND_STATUS_CHOICES = (
        (SUCCESS, 'Success'),
        (COULD_NOT_CONNECT_TO_ARDUINO, 'Could not connect to Arduino'),
    )
    command_status = models.CharField(max_length=3, choices=COMMAND_STATUS_CHOICES, default=SUCCESS)

    def __str__(self):
        return "{}: {} ({})".format(str(self.command_date), self.command, self.command_status)

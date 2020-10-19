from django.db import models


class Log(models.Model):
    time = models.DateTimeField()
    host = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    ip = models.CharField(max_length=20)
    port = models.IntegerField()
    # True => Login; False => Logout
    activity = models.BooleanField()

    def __str__(self):
        return f"{self.user}@{self.host}"

from django.db import models


class Log(models.Model):
    '''
        Model storing the logs
        Fields:
        time: Timestamp provided by serverside
        host: SSH server
        user: User at SSH Server
        ip  : ip of the SSH client
        port: port
        activity:
            LOGIN_SSH_KEY: Login with SSH Key
            LOGIN_SSH_PWD: Login with SSH using password
            LOGOUT_SSH:    Logout SSH session
        client: Client device details
    '''

    time = models.DateTimeField()
    host = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    ip = models.CharField(max_length=20)
    port = models.IntegerField()
    activity = models.CharField(max_length=20)
    client = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user}@{self.host}"

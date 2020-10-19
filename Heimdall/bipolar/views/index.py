from django.http import HttpResponse


# Index view
def index(request):
    return HttpResponse("You have reached Bipolar. Sorry, but Bipolar only transports The Gods of Asgard and information. You are neither...")

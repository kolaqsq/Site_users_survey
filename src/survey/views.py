from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Survey


@login_required
def index(request):
    survey_list = Survey.objects.all()
    context = {'survey_list': survey_list}
    return render(request, 'survey/index.html', context)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'survey'
urlpatterns = [
                  path('', login_required(views.IndexView.as_view()), name='index'),  # index
                  path('survey/create/', login_required(views.CreateView.as_view()), name='create'),  # create survey
                  path('survey/save_new/', views.save, name='save_new'),  # save
                  # path('dashboard/', views.dashboard_with_pivot, name='dashboard_with_pivot'),
                  # path('dashboard/data/', views.pivot_data, name='pivot_data'),
                  path('survey/<str:survey_id>/', views.survey, name='survey'),  # survey
                  path('survey/<str:survey_id>/result/', views.result, name='result'),  # result
                  path('survey/<str:survey_id>/submit/', views.submit, name='submit'),  # submit
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

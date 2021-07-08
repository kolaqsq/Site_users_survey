from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'survey'
urlpatterns = [
                  # path('', views.index, name='index'),  # index
                  path('', views.IndexView.as_view(), name='index'),  # index
                  path('<str:survey_id>/', views.survey, name='survey'),  # survey
                  path('<str:survey_id>/result/', views.result, name='result'),  # result
                  path('<str:survey_id>/submit/', views.submit, name='submit'),  # submit
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

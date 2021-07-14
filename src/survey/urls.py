from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'survey'
urlpatterns = [
                  path('', login_required(views.IndexView.as_view()), name='index'),  # index
                  path('survey/create/', login_required(views.CreateView.as_view()), name='create'),  # create survey
                  path('survey/create/save/', views.save, name='save_new'),  # save
                  path('survey/create/<str:survey_id>/success/', views.saveSuccess, name='save_success'),  # saved
                  path('survey/<str:survey_id>/update/',
                       login_required(views.UpdateView.as_view()), name='update'),  # update survey
                  path('survey/<str:survey_id>/update/save/', views.save_update, name='save_update'),  # save update
                  path('survey/<str:survey_id>/update/success/', views.updateSuccess, name='update_success'),  # updated
                  path('survey/delete/success/', views.deleteSuccess, name='delete_success'),  # deleted
                  path('survey/<str:survey_id>/answers/',
                       login_required(views.AnswerListView.as_view()), name='answer_list'),  # answers list
                  path('survey/<str:survey_id>/answers/<str:answer_id>',
                       login_required(views.AnswerView.as_view()), name='answer'),  # answer
                  # path('dashboard/', views.dashboard_with_pivot, name='dashboard_with_pivot'),
                  # path('dashboard/data/', views.pivot_data, name='pivot_data'),
                  path('survey/<str:survey_id>/', views.survey, name='survey'),  # survey
                  path('survey/<str:survey_id>/result/', views.result, name='result'),  # result
                  path('survey/<str:survey_id>/submit/', views.submit, name='submit'),  # submit
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

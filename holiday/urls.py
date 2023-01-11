from django.contrib import admin
from django.urls import path, include
from . import views
# import your views here


# Add your views to the url patterns

urlpatterns = [
    path('create/', views.HolidayCreateView.as_view(), name='Create'), #pass
    path('holidays/all/', views.HolidayListView.as_view(), name='List-all'), #pass
    path('cities/', views.CityListView.as_view(), name='List-all-cities'),  #
    path('upload/', views.UploadCreateView.as_view(), name='Upload'), #
    path('monthly/', views.MonthlyHolidayView.as_view(), name='Month'), #
    path('daily/', views.DailyHolidayView.as_view(), name='Daily'),
    path('updateholidayinfo/<int:pk>/', views.HolidayEditView.as_view(), name='Holiday-Edit'), #done
    path('deleteholidayinfo/<int:pk>/', views.HolidayDeleteView.as_view(), name='Holiday-Delete'),  #done
    path('admin/login/', views.AdminLoginView.as_view(), name='Admin-Login'), #pass
]


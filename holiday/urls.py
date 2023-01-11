from django.contrib import admin
from django.urls import path, include
from . import views
# import your views here


# Add your views to the url patterns

urlpatterns = [
    path('create/', views.HolidayCreateView.as_view(), name='Create'), #pass
    path('holidays/all/', views.HolidayListView.as_view(), name='List-all'), #pass
    path('cities/', views.CityListView.as_view(), name='List-all-cities'),  #pass
    path('upload/', views.UploadCreateView.as_view(), name='Upload'), #pass
    path('monthly/', views.MonthlyHolidayView.as_view(), name='Month'), #pass
    path('daily/', views.DailyHolidayView.as_view(), name='Daily'), #pass
    path('updateholidayinfo/<int:pk>/', views.HolidayEditView.as_view(), name='Holiday-Edit'), #?
    path('deleteholidayinfo/<int:pk>/', views.HolidayDeleteView.as_view(), name='Holiday-Delete'),  #pass
    path('admin/login/', views.AdminLoginView.as_view(), name='Admin-Login'), #pass
]


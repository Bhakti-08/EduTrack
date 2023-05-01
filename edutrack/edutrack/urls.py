"""djangoProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from edutrack import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index,name='login'),
    path('registration/',views.registration,name='registration'),
    path('logout/', views.logoutPage,name='logout'),
    path('profHome/',views.profHome,name='profHome'),
    path('studentHome/',views.studentHome,name='studentHome'),
    path('selectTest/',views.selectTest,name='selectTest'),
    path('testsForResults/',views.testsForResults,name='testsForResults'),
    path('testResults/<int:test_id>',views.testResults,name='testResults'),
    path('studentResults/',views.studentResults,name='studentResults'),
    path('test-question/<int:test_id>',views.test_question,name='test_question'),
    path('testSubmitted/<int:test_id>',views.testSubmitted,name='testSubmitted'),

    path('upload_questionBank/',views.upload_questionBank,name='upload_questionBank'),
    path('addingTest/',views.addingTest,name='addingTest'),  
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



'''
path('profRegistrationForm/',views.profRegistrationForm,name='profRegistrationForm'),
path('studentRegistrationForm/',views.studentRegistrationForm,name='studentRegistrationForm'),
path('upload_questionBank/',views.upload_questionBank,name='upload_questionBank'),
path('addingTest/',views.addingTest,name='addingTest'),    
path('updateStudentProfile/',views.updateStudentProfile,name='updateStudentProfile'),
path('updateProfessorProfile/',views.updateProfessorProfile,name='updateProfessorProfile'),
'''
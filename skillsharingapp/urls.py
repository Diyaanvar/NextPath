from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('editprofile/',views.editprofile,name='editprofile'),
   
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('studentlist/', views.studentlist, name='studentlist'),
    path('delete_student/<int:id>/',views.delete_student,name='delete_student'),
    path('institutelist/', views.institutes_list, name='institutelist'),
    path('userlistcourses/',views.userlistcourses,name='userlistcourses'),
    
    path('my-admin/courses/', views.admin_course_list, name='admin_course_list'),
    path('institute/register/', views.institute_register, name='institute_register'),
    path('institute/login/', views.institute_login, name='institute_login'),
    path('institutes/', views.institutes_list, name='institutes_list'),
    path('institutes/approve/<int:institute_id>/', views.approve_institute, name='approve_institute'),
    path('institutes/reject/<int:institute_id>/', views.reject_institute, name='reject_institute'),
    path('institutes/delete/<int:institute_id>/', views.delete_institute, name='delete_institute'),

    path('courses/', views.institute_courses, name='institute_courses'),
    path('courses/add/', views.institute_add_course, name='institute_add_course'),
    path('courses/edit/<int:course_id>/', views.institute_edit_course, name='institute_edit_course'),
    path('courses/delete/<int:course_id>/', views.institute_delete_course, name='institute_delete_course'),
    path('courses/<int:course_id>/lessons/', views.institute_lessons_list, name='institute_lessons_list'),
    path('lessons/delete/<int:lesson_id>/', views.institute_delete_lesson, name='institute_delete_lesson'),
    path('institute/logout/', views.institute_logout, name='institute_logout'),
    path('enter-skills/', views.enter_skills, name='enter_skills'),

    
    

    path(
    'user/lessons/<int:course_id>/',
    views.user_lessons_list,
    name='user_lessons_list'),

    path(
    'course/payment/<int:course_id>/',
    views.course_payment,
    name='course_payment'),

    path(
        'payment/success/',
        views.payment_success,
        name='paymentsuccess'
    ),



    # chatbot
    path('chatbot/', views.chatbot, name='chatbot'),

    

]



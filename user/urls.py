from django.conf.urls import url

from user.views import user_detail, register

urlpatterns = [
    # url(r'^<uid>', UserView.as_view()),
    url(r'^v1/user/reg', register),
    url(r'^v1/user/detail', user_detail),
]
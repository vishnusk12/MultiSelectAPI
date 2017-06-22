'''
Created on Jan 16, 2017

@author: vishnu.sk
'''

from django.conf.urls import url, include
from .views import PricingViewSet
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'pricingstats', PricingViewSet, 'PricingViewSet')
urlpatterns = [url(r'^', include(router.urls))]

from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from . import views

# urls checks if the subpart of the url matches then run the view funciotn e.g. views.car_list_view.
# you can also name the urls so that in code easily reference the url through its name instead of its url.

# Defualt urls are used to combine the urls like reviews to show the review lists and reviews/{int} to retieve specific reivew by giving id, instead of defining two routes for this task we can use the single one.
router = DefaultRouter()
router.register('reviews',views.ReviewModelViewSet, basename='reviews')

urlpatterns = [
    path('list/',views.car_list_view,name='car_list'),
    path('showrooms/',views.showroom_view.as_view(), name = 'showroom_list'),
    path('showrooms/<int:pk>', views.showroomdetial_view.as_view(), name = 'showroom'),
    path('<int:pk>',views.car_detail_view,name='car_detail'),
    path('showroom/<int:pk>/create-review',views.ReviewCreate.as_view(), name = 'review_create'),
    path('showroom/<int:pk>/review',views.ReviewList.as_view(), name = 'review_list'),
    path('showroom/review/<int:pk>',views.ReviewDetail.as_view(), name = 'review_detial'),
    # path('',include(router.urls)),
    # path('reviews/',views.ReviewView.as_view(), name='reviews_list'),
    # path('review/<int:pk>',views.ReviewDetailView.as_view(), name='review'),

]
from django.urls import path
from .views import QuestionViewSet, AnswerViewSet

urlpatterns = [

    path('api/questions/', QuestionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/questions/<int:pk>/', QuestionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),

    path('api/answers/', AnswerViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/answers/<int:pk>/', AnswerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]

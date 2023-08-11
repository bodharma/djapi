from django.urls import path
from . import views

urlpatterns = [
    path('table', views.TableViewSet.as_view({'post': 'create'}), name='create-table'),
    path('table/<int:pk>', views.TableViewSet.as_view({'put': 'update'}), name='update-table'),
    path('table/<int:pk>/row', views.TableViewSet.as_view({'post': 'create_row'}), name='create-row'),
    path('table/<int:pk>/rows', views.TableViewSet.as_view({'get': 'list_rows'}), name='list-rows'),
    path('table/', views.TableListView.as_view(), name='table-list'), # This is your new line
    path('table/<int:pk>/', views.TableViewSet.as_view({
        'post': 'create',
        'put': 'update'
    }), name='table-detail'),
    path('table/<int:table_id>/row/', views.TableRowViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='table-row-list'),

]

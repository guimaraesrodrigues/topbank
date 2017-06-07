from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from server import views

from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'contas', views.ContaViewSet)

schema_view = get_swagger_view(title='TopBank API')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^admin/', admin.site.urls),
	#url(r'^contas/', views.ContaList.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^docs/', schema_view),
]

#urlpatterns = format_suffix_patterns(urlpatterns)

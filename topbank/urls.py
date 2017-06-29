from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from server import views

from rest_framework_swagger.views import get_swagger_view

'''O objeto router realiza a criacao de urls de acordo com a view'''

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'contas', views.ContaViewSet)
router.register(r'agencias', views.AgenciaViewSet)

schema_view = get_swagger_view(title='TopBank API')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^admin/', admin.site.urls),#url para o django admin
    url(r'^', include(router.urls)),#urls geradas pela classe router
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),#url para a api do restful
	url(r'^docs/', schema_view),#url para o swagger
]

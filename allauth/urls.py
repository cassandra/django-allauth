from importlib import import_module

from django.urls import include, path

from allauth.socialaccount import providers

from . import app_settings

# TODO: Change by ARC to support lp_game 2020/4/1. We use our own urls for
# main pages to allow easier overrides.
#
#  urlpatterns = [path('', include('allauth.account.urls'))]
#
urlpatterns = []

if app_settings.SOCIALACCOUNT_ENABLED:
    urlpatterns += [path('social/', include('allauth.socialaccount.urls'))]

# Provider urlpatterns, as separate attribute (for reusability).
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns

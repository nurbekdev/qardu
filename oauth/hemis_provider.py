import requests
from allauth.socialaccount import providers
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from django.conf import settings


class HemisProvider(OAuth2Provider):
    id = "hemis"
    name = "Hemis"


class HemisOAuth2Adapter(OAuth2Adapter):
    provider_id = HemisProvider.id
    access_token_url = settings.OAUTH2_TOKEN_URL
    authorize_url = settings.OAUTH2_AUTHORIZE_URL
    profile_url = settings.OAUTH2_USER_INFO_URL

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": f"Bearer {token.token}"}
        extra_data = requests.get(self.profile_url, headers=headers).json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


providers.registry.register(HemisProvider)

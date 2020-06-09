from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

  def get_login_redirect_url(self, request):
      return '/log-in'

  def get_email_confirmation_redirect_url(self, request):
      return '/log-in'
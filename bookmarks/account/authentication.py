from django.contrib.auth.models import User
class EmailAuthBackend(object):
    """
    Authenticate using e-mail account.
    This is the additional method which is used for authentication along with the default method.
    """
    def authenticate(self, username=None, password=None):
        try:
            #get the user for the username ,where user enters email for the username
            user = User.objects.get(email=username)
            #use the default method to check password
            if user.check_password(password):
                #return the user if the password matches
                return user
            #else return None
            return None
        except User.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            #return the user for the user_id
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            #return nothing if user not available
            return None

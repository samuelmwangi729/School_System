from Users.models import User
class userVerifier:
    def verifyUser(self,username):
        user = User.objects.get(username=username)
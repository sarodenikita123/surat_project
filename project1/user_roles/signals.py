from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver, Signal
from .models import UserLogs, UserRole

user_logged_in= Signal()
user_logged_out = Signal()

class UserStore:
    def user_login(self,request,user):
        user_logged_in.send(sender=self.__class__, request=request, user=user )
    def user_logout(self,request,user):
       user_logged_out.send(sender=self.__class__, request=request, user=user )


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserLogs.objects.create(user=user, message='login')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserLogs.objects.create(user=user, message='logout')

@receiver(post_save, sender=UserRole)
def log_role_change(sender, instance, created, **kwargs):
    try:
         
        if not created:
            u = UserRole.objects.get(pk=instance.id)
            previous_role = u.role.role
            new_role = instance.role.role
            if previous_role != new_role :
                UserLogs.objects.create(user=instance.user,message=f"user role changed from {previous_role} to {new_role}")
    except:
        pass
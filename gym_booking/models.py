# # myapp/models.py
# from datetime import timedelta
# from enum import Enum

# myapp/models.py
import secrets
from datetime import timedelta

# from django.conf import settings
# # myapp/models.py
# # models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .paystack import Paystack

# from django.core.mail import send_mail
# from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone

# from .paystack import Paystack

# # models.py



# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(username, email, password, **extra_fields)

# class CustomUser(AbstractUser):
#     user_id = models.IntegerField(unique=True, blank=True, null=True)

#     # Add unique related_name attributes for groups and user_permissions
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_groups',
#         blank=True,
#         verbose_name='groups',
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_user_permissions',
#         blank=True,
#         verbose_name='user permissions',
#         help_text='Specific permissions for this user.',
#     )
#     objects = CustomUserManager()

#     def __str__(self):
#         return self.username


# from datetime import timedelta

# from django.core.mail import send_mail
# from django.db import models
# from django.utils import timezone

# from .models import \
#     CustomUser  # Assuming your CustomUser model is in a 'models' module
# from .paystack import Paystack

# # class Plan(Enum):
# #     BRONZE = 500
# #     SILVER = 1000
# #     GOLD = 1500


# class GymMembership(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, db_column='user_id')
#     plan = models.CharField(max_length=10, choices=[
#         ('bronze', 'Bronze'),
#         ('silver', 'Silver'),
#         ('gold', 'Gold'),
#     ], default='bronze')
#     expiry_date = models.DateTimeField(null="True", blank="True")
#     plan_status = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now, null=True)
    

#     def set_membership_plan(self, amount):
#         if amount == Plan.BRONZE.value:
#             self.plan = Plan.BRONZE.name
#             self.set_expiration_date(14)
#         elif amount == Plan.SILVER.value:
#             self.plan = Plan.SILVER.name
#             self.set_expiration_date(30)
#         elif amount == Plan.GOLD.value:
#             self.plan = Plan.GOLD.name
#             self.set_expiration_date(60)


#     def __str__(self):
#         return f"{self.user.username}'s Gym Membership"

#     def set_expiration_date(self, days):
#         self.expiration_date = timezone.now() + timedelta(days=days)
#         self.save()

#     def send_expiration_email(self):
#         three_days_from_now = timezone.now() + timedelta(days=3)
#         if self.expiration_date and self.expiration_date <= three_days_from_now:
#             subject = 'Gym Membership Expiration Reminder'
#             message = f"Dear {self.user.first_name},\n\nYour gym membership is expiring on {self.expiration_date}. " \
#                       f"Please renew your membership to continue enjoying our services.\n\nBest regards,\nThe Zircon Gym Team"
#             from_email = 'ucheemma@swebslimited.com'
#             to_email = [self.user.email]
#             send_mail(subject, message, from_email, to_email, fail_silently=False)

#     def set_plan_status(self):
#         new_plan_status = self.expiration_date is not None and self.expiration_date > timezone.now()
#         if self.plan_status != new_plan_status:
#             self.plan_status = new_plan_status
#             self.save()

#     def get_plan_status(self):
#         return self.plan_status

#     @property
#     def first_name(self):
#         return self.user.first_name if self.user else None

#     @property
#     def last_name(self):
#         return self.user.last_name if self.user else None

# @receiver(post_save, sender=CustomUser)
# def create_user_membership(sender, instance, created, **kwargs):
#     if created:
#         GymMembership.objects.create(user=instance)

# class Payment(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
#     first_name = models.CharField(max_length=10, default='')
#     last_name = models.CharField(max_length=10, default='')
#     username = models.CharField(max_length=10, default='')
#     plan = models.ForeignKey(GymMembership, default='', on_delete=models.CASCADE, null=True, blank=True)

#     amount = models.PositiveIntegerField()
#     ref = models.CharField(max_length=50)
#     email = models.EmailField()
#     verified = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ('-date_created',)

#     def __str__(self):
#         return f"Payment: {self.amount}"

#     def save(self, *args, **kwargs):
#         while not self.ref:
#             ref = secrets.token_urlsafe(50)
#             object_with_similar_ref = Payment.objects.filter(ref=ref)
#             if not object_with_similar_ref:
#                 self.ref = ref
#         super().save(*args, **kwargs)

#     def amount_value(self):
#         return int(self.amount) * 100

#     def verify_payment(self):
#         paystack = Paystack()
#         status, result = paystack.verify_payment(self.ref, self.amount)
#         if status:
#             if result['amount'] / 100 == self.amount:
#                 self.verified = True
#             self.save()
#         if self.verified:
#             return True
#         return False

#     # @property
#     # def user_id(self):
#     #     return self.user.id if self.user else None

#     @property
#     def username(self):
#         return self.user.username if self.user else None






class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    user_id = models.IntegerField(unique=True, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class GymMembership(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, db_column='user_id')
    plan = models.CharField(max_length=10, choices=[
        ('No Plan', 'No Plan'),
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ], default='No Plan')
    expiry_date = models.DateTimeField(null=True, blank=True)
    plan_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def set_membership_plan(self, amount):
        if amount == 500:
            self.plan = 'bronze'
            self.set_expiration_date(14)
        elif amount == 1000:
            self.plan = 'silver'
            self.set_expiration_date(30)
        elif amount == 1500:
            self.plan = 'gold'
            self.set_expiration_date(60)

    def __str__(self):
        return f"{self.user.username}'s Gym Membership"

    def set_expiration_date(self, days):
        self.expiry_date = timezone.now() + timedelta(days=days)
        self.save()

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10,default='No Plan',
        null=True,
        blank=True, choices=[
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ])
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s Subscription for {self.plan}"

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=10, default='')
    last_name = models.CharField(max_length=10, default='')
    username = models.CharField(max_length=10, default='')
    plan = models.CharField(
        max_length=10,
        default='No Plan',
        null=True,
        blank=True,
        choices=[
            ('No Plan', 'No Plan'),
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
        ]
    )


    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=50)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return int(self.amount) * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False

    @property
    def username(self):
        return self.user.username if self.user else None

@receiver(post_save, sender=CustomUser)
def create_user_membership(sender, instance, created, **kwargs):
    if created:
        GymMembership.objects.create(user=instance)

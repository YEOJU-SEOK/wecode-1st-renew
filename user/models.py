from django.db import models
from product.models import Product
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Gender(models.Model):
    name = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'genders'


class User(AbstractBaseUser):
    member_seq = models.AutoField(
        primary_key=True, help_text="회원 고유 키"
    )
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    nickname = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender_id = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    birth_date = models.DateField(auto_now=False, null=True)
    profile_image = models.URLField(max_length=256, null=True, default="https://image.ohou.se/i/bucketplace-v2-development/uploads/default_images/avatar.png?gif=1&amp;w=640&amp;h=640&amp;c=c&amp;webp=1")
    note = models.CharField(max_length=50, null=True)

    # django 기본의 User Model 은 username 을 pk 로 사용하므로 이를 account 로 변경
    USERNAME_FIELD = 'member_seq'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'histories'

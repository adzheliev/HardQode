from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    name = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_products')
    min_users_in_group = models.IntegerField(default=1)
    max_users_in_group = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=255)
    video_url = models.URLField()

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='groups')
    users = models.ManyToManyField(User, related_name='user_groups')


class Access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accesses')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='accesses')


@receiver(post_save, sender=Access)
def distribute_user_to_group(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        user = instance.user
        group = product.groups.annotate(count=models.Count('users')).filter(count__lt=models.F('max_users')).order_by(
            'count').first()
        if group:
            group.users.add(user)
            return group
        else:
            new_group = Group.objects.create(
                name=f"Новая группа для {product.name}",
                product=product,
                min_users=1,
                max_users=10
            )
            new_group.users.add(user)
            return new_group

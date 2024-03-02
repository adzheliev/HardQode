from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, F
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    """
    A model that represents a product.

    Attributes:
        name (str): The name of the product.
        start_datetime (datetime): The datetime when the product starts.
        cost (Decimal): The cost of the product.
        creator (User): The user who created the product.
        min_users_in_group (int): The minimum number of users in a group.
        max_users_in_group (int): The maximum number of users in a group.

    """
    name = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_products'
    )
    min_users_in_group = models.IntegerField(default=1)
    max_users_in_group = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    A model that represents a lesson in a product.

    Attributes:
        product (ForeignKey): The product that the lesson is associated with.
        name (CharField): The name of the lesson.
        video_url (URLField): The URL of the video that corresponds to the lesson.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    name = models.CharField(max_length=255)
    video_url = models.URLField()

    def __str__(self):
        return self.name


class Group(models.Model):
    """
    A model that represents a group of users who are participating in a product.

    Attributes:
        name (CharField): The name of the group.
        product (ForeignKey): The product that the group is associated with.
        users (ManyToManyField): The users who are members of the group.
    """
    name = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    users = models.ManyToManyField(
        User,
        related_name='user_groups'
    )


class Access(models.Model):
    """
    A model that represents a user's access to a specific product.

    Attributes:
        user (ForeignKey): The user who has access to the product.
        product (ForeignKey): The product that the user has access to.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accesses'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='accesses'
    )


"""
This function is triggered when a new Access object is created.
It ensures that the user has access to a group for the given product,
by either adding the user to an existing group or creating a new group
if there are no available groups.

Args:
    sender (Model): The model class that triggered the signal.
    instance (Model): The newly created Access object.
    created (bool): A boolean indicating whether the object was created
        or updated.
    **kwargs (dict): Any additional keyword arguments.

Returns:
    Group: The group that the user was added to, or None if no group was
        created.
"""


@receiver(post_save, sender=Access)
def distribute_user_to_group(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        user = instance.user
        group = product.groups.annotate(count=Count('users')).filter(
            count__lt=F('max_users')).order_by('count').first()
        if group:
            group.users.add(user)
            return group
        else:
            new_group = Group.objects.create(
                name=f"New group for {product.name}",
                product=product,
                min_users=1,
                max_users=10
            )
            new_group.users.add(user)
            return new_group

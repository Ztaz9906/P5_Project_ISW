from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

def for_client(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_cliente or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def for_repartidor_or_dependiente(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    group = Group.objects.filter(name="repartidor").first()
    group1 = Group.objects.filter(name="dependiente").first()
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (group in u.groups.all()) or (
            group1 in u.groups.all()) or u.is_superuser ,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
def for_cliente_repartidor_or_dependiente(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    group = Group.objects.filter(name="repartidor").first()
    group1 = Group.objects.filter(name="dependiente").first()
    group2 = Group.objects.filter(name="cliente").first()
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (group in u.groups.all()) or ( group1 in u.groups.all()) or (group2 in u.groups.all()) or u.is_superuser ,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
def for_admin(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    group = Group.objects.filter(name="admin").first()
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (group in u.groups.all()) or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
def for_repartidor(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    group = Group.objects.filter(name="repartidor").first()
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (group in u.groups.all()) or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

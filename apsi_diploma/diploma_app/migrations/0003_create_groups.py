# Generated by Django 4.0.4 on 2022-06-14 17:13

from django.db import migrations
from django.apps import apps
from django.contrib.auth.models import Group, Permission, User


def create_groups(apps, schema_editor):

    group, created = Group.objects.get_or_create(name="student")
    if created:
        student_perm = ["can_start_dissertationprocess", "view_dissertationprocess"]
        for name in student_perm:
            p = Permission.objects.get(codename=name)
            group.permissions.add(p)
        group.save()
    common_perm = [
        "can_choose_reviewer_dissertationprocess",
        "can_choose_reviewer_again_dissertationprocess",
        "can_add_exam_results_dissertationprocess",
        "can_add_exam_details_dissertationprocess",
        "can_add_exam_details_again_dissertationprocess",
        "view_dissertationprocess",
        "view_scientificpublishingprocess",
    ]

    group, created = Group.objects.get_or_create(name="scientist")
    if created:
        p = Permission.objects.get(codename="can_start_scientificpublishingprocess")
        group.permissions.add(p)
        for name in common_perm:
            p = Permission.objects.get(codename=name)
            group.permissions.add(p)
        group.save()

    group, created = Group.objects.get_or_create(name="office_worker")
    if created:
        office_perm = [
            "manage_process",
            "delete_scientificpublishingprocess",
            "delete_process",
            "delete_dissertationprocess",
        ]
        for name in common_perm + office_perm:
            p = Permission.objects.get(codename=name)
            group.permissions.add(p)
        group.save()


def create_users(schema, group):
    User.objects.create_superuser("admin", password="admin").save()

    u = User.objects.create_user("student", password="student")
    u.groups.add(Group.objects.get(name="student"))
    u.save()
    u = User.objects.create_user("student1", password="student")
    u.groups.add(Group.objects.get(name="student"))
    u.save()
    u = User.objects.create_user("student2", password="student")
    u.groups.add(Group.objects.get(name="student"))
    u.save()

    u = User.objects.create_user("scientist", password="scientist")
    u.groups.add(Group.objects.get(name="scientist"))
    u.save()
    u = User.objects.create_user("scientist1", password="scientist")
    u.groups.add(Group.objects.get(name="scientist"))
    u.save()
    u = User.objects.create_user("scientis2", password="scientist")
    u.groups.add(Group.objects.get(name="scientist"))
    u.save()
    u = User.objects.create_user("scientist3", password="scientist")
    u.groups.add(Group.objects.get(name="scientist"))
    u.save()

    u = User.objects.create_user("office", password="office")
    u.groups.add(Group.objects.get(name="office_worker"))
    u.save()


class Migration(migrations.Migration):

    dependencies = [
        ("diploma_app", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_groups),
        migrations.RunPython(create_users),
    ]

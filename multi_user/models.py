from django.db import models

from django.contrib.auth.models import AbstractUser, Permission

# Create your models here.
class User(AbstractUser):
    ACCESS_LEVEL_CHOICES = [
        ('head_office', 'Head Office'),
        ('district_office', 'District Office'),
        ('branch_location', 'Branch Location'),
    ]
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES, default='head_office')
    account_owner = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.access_level == 'head_office':
            self.user_permissions.add(Permission.objects.get(codename='all_head_office'))
            self.user_permissions.add(Permission.objects.get(codename='all_district_office'))
            self.user_permissions.add(Permission.objects.get(codename='all_branch_location'))
        elif self.access_level == 'district_office':
            self.user_permissions.add(Permission.objects.get(codename='all_district_office'))
            self.user_permissions.add(Permission.objects.get(codename='all_branch_location'))
        elif self.access_level == 'branch_location':
            self.user_permissions.add(Permission.objects.get(codename='all_branch_location'))


class HeadOffice(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("all_head_office", "All head office permissions")
        ]

    def __str__(self):
        return self.name
    

class DistrictOffice(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(HeadOffice, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("all_district_office", "All district office permissions")
        ]

    def __str__(self):
        return self.name


class BranchLocation(models.Model):
    name = models.CharField(max_length=50)
    district_office = models.ForeignKey(DistrictOffice, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("all_branch_location", "All branch location permissions")
        ]

    def __str__(self):
        return self.name



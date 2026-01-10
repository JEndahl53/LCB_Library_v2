# organizations/models.py

from django.db import models
from django.urls import reverse

# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    notes = models.TextField(blank=True)

    # Address (optional)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text='Soft-disable organization without deleting history'
    )

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('organizations:organization_detail', args=[self.pk])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Organizations'
        verbose_name = 'Organization'


class OrganizationRoleType(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text='Stable identifier (e.g. LENDER, BORROWER, RENTAL_VENDOR, PUBLISHER)'
    )
    name = models.CharField(
        max_length=100,
        help_text='Human-readable name of the organization role (e.g. Publisher)',
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Organization Role Types'
        verbose_name = 'Organization Role Type'

    def __str__(self):
        return self.name


class OrganizationRole(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='roles',
    )

    role_type = models.ForeignKey(
        OrganizationRoleType,
        on_delete=models.PROTECT,
        related_name='organization_roles',
    )

    is_active = models.BooleanField(default=True)

    notes = models.TextField(blank=True)

    class Meta:
        unique_together = (('organization', 'role_type'),)

    def __str__(self):
        return f'{self.organization} - {self.role_type}'


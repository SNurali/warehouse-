from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    name = models.CharField(_('Company Name'), max_length=100)
    slug = models.SlugField(unique=True)
    address = models.TextField(_('Address'), blank=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    tax_id = models.CharField(_('Tax ID'), max_length=50, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    COMPANY_ROLES = (
        ('owner', _('Owner')),
        ('admin', _('Administrator')),
        ('manager', _('Manager')),
        ('staff', _('Staff')),
        ('agent', _('Agent')),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name=_('Company')
    )
    role = models.CharField(
        _('Role'),
        max_length=20,
        choices=COMPANY_ROLES,
        default='staff'
    )
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    department = models.CharField(_('Department'), max_length=50, blank=True)
    is_verified = models.BooleanField(_('Verified'), default=False)
    last_activity = models.DateTimeField(_('Last Activity'), null=True, blank=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"{self.get_full_name()} ({self.company})"


class CompanySubscription(models.Model):
    PLAN_CHOICES = (
        ('basic', _('Basic')),
        ('standard', _('Standard')),
        ('premium', _('Premium')),
        ('enterprise', _('Enterprise')),
    )

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    plan = models.CharField(
        _('Plan'),
        max_length=20,
        choices=PLAN_CHOICES,
        default='basic'
    )
    is_active = models.BooleanField(_('Active'), default=True)
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    payment_method = models.CharField(
        _('Payment Method'),
        max_length=50,
        blank=True
    )
    notes = models.TextField(_('Notes'), blank=True)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self):
        return f"{self.company} - {self.get_plan_display()}"


class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('create', _('Create')),
        ('update', _('Update')),
        ('delete', _('Delete')),
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('password_change', _('Password Change')),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('User')
    )
    action = models.CharField(
        _('Action'),
        max_length=20,
        choices=ACTION_CHOICES
    )
    model = models.CharField(_('Model'), max_length=50)
    object_id = models.CharField(_('Object ID'), max_length=50, blank=True)
    details = models.JSONField(_('Details'), default=dict)
    ip_address = models.GenericIPAddressField(_('IP Address'), null=True, blank=True)
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)

    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.model}"
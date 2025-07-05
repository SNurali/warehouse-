from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.tenants.models import Company


class ReportTemplate(models.Model):
    REPORT_TYPES = (
        ('inventory', _('Inventory')),
        ('sales', _('Sales')),
        ('purchases', _('Purchases')),
        ('movements', _('Stock Movements')),
        ('custom', _('Custom')),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='report_templates',
        verbose_name=_('Company')
    )
    name = models.CharField(_('Name'), max_length=100)
    report_type = models.CharField(
        _('Report Type'),
        max_length=20,
        choices=REPORT_TYPES
    )
    template = models.TextField(_('Template'))
    is_default = models.BooleanField(_('Default'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Report Template')
        verbose_name_plural = _('Report Templates')
        ordering = ['name']

    def __str__(self):
        return self.name


class ScheduledReport(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('quarterly', _('Quarterly')),
        ('yearly', _('Yearly')),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='scheduled_reports',
        verbose_name=_('Company')
    )
    name = models.CharField(_('Name'), max_length=100)
    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.CASCADE,
        verbose_name=_('Template')
    )
    frequency = models.CharField(
        _('Frequency'),
        max_length=20,
        choices=FREQUENCY_CHOICES
    )
    recipients = models.TextField(_('Recipients'))
    last_run = models.DateTimeField(
        _('Last Run'),
        null=True,
        blank=True
    )
    next_run = models.DateTimeField(_('Next Run'))
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Scheduled Report')
        verbose_name_plural = _('Scheduled Reports')
        ordering = ['next_run']

    def __str__(self):
        return self.name
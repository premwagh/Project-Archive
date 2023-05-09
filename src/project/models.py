from datetime import timedelta
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager

from core.db.models.mixins import TimeStampModelMixin
from core.db.fields import PercentField
from core.ml_functions import uniqueness_percentile_against_data_list
from user.models import User

from .settings import project_settings


def get_invite_expiry():
    return timezone.now() + timedelta(seconds=project_settings.PROJECT_GROUP_INVITE_TTL)


class ProjectGroup(TimeStampModelMixin):
    class StatusChoices(models.TextChoices):
        FORMATION = "formation", _("Formation")
        CONFORMED = "conformed", _("Conformed")

    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name='project_groups',
        limit_choices_to={"role": User.RoleChoices.FACULTY},
    )
    status = models.CharField(
        _('Status'), choices=StatusChoices.choices, default=StatusChoices.FORMATION)
    conformed_on = models.DateField(_('Conformed On'), null=True, blank=True)
    conformed_by = models.ForeignKey(
        "user.User",
        on_delete=models.PROTECT,
        related_name='conformed_student_groups',
        null=True,
        blank=True,
    )
    created_by = models.OneToOneField(
        "user.User",
        on_delete=models.PROTECT,
        related_name='created_student_groups',
    )


class ProjectGroupInvite(TimeStampModelMixin):

    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("Pending")
        ACCEPTED = "accepted", _("Accepted")
        REJECTED = "rejected", _("Rejected")

    project_group = models.ForeignKey(
        ProjectGroup,
        on_delete=models.PROTECT,
        related_name='invites',
    )
    status = models.CharField(
        _('Status'), choices=StatusChoices.choices, default=StatusChoices.PENDING)
    student = models.ForeignKey(
        "user.Student",
        on_delete=models.PROTECT,
        related_name='invites',
    )
    expires_on = models.DateTimeField(
        _('Expires On'), default=get_invite_expiry)
    created_by = models.ForeignKey(
        "user.User",
        on_delete=models.PROTECT,
        related_name='created_invites',
    )

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_on

    def accept_invite(self):
        if not self.is_expired:
            with transaction.atomic():
                self.status = self.StatusChoices.ACCEPTED
                self.student.project_group = self.project_group
                self.student.save(update_fields=['project_group'])
                self.save(update_fields=['status'])

    def reject_invite(self):
        if not self.is_expired:
            with transaction.atomic():
                self.status = self.StatusChoices.REJECTED
                self.save(update_fields=['status'])

    class Meta():
        verbose_name = _('Project Group Invite')
        verbose_name_plural = _('Project Group Invites')
        unique_together = (("project_group", "student"),)


class ProjectIdea(TimeStampModelMixin, models.Model):

    class StatusChoices(models.TextChoices):
        NEW = "new", _("New")
        PENDING = "pending", _("Pending")
        APPROVED = "approved", _("Approved")
        COMPLETED = "completed", _("Completed")
        REJECTED = "rejected", _("Rejected")

    title = models.CharField(_('Title'), max_length=255)
    project_group = models.ForeignKey(
        'project.ProjectGroup',
        verbose_name=_('Project Group'),
        on_delete=models.PROTECT,
        related_name='ideas',
    )
    report_content = models.TextField(_('Report Content'))
    abstract_content = models.TextField(_('Abstract Content'))
    uniqueness = PercentField(_('Uniqueness'), default=0)
    tags = TaggableManager()
    status = models.CharField(
        _('Status'), choices=StatusChoices.choices, default=StatusChoices.NEW)
    approved_on = models.DateField(_('Approved On'), null=True, blank=True)
    completed_on = models.DateField(_('Completed On'), null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def calculate_uniqueness(self, force=False, save=False):
        if self.status not in (
            self.StatusChoices.APPROVED,
            self.StatusChoices.COMPLETED,
        ) or force:
            qs = self._meta.default_manager.get_queryset().filter(
                status__in=(
                    self.StatusChoices.APPROVED,
                    self.StatusChoices.COMPLETED,
                ),
            )
            if self.id:
                qs = qs.objects.exclude(id=self.id)
            self.uniqueness = uniqueness_percentile_against_data_list(
                self.report_content,
                qs.values_list('report_content', flat=True),
            )
            if save:
                self.save(update_fields=['uniqueness'])

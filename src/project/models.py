from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from core.db.models.mixins import TimeStampModelMixin
from core.db.fields import PercentField
from user.models import User



class ProjectGroup(TimeStampModelMixin):
    class StatusChoices(models.TextChoices):
        FORMATION = "formation", _("Formation")
        CONFORMED = "conformed", _("Conformed")

    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(
        'user.Faculty',
        on_delete=models.PROTECT,
        related_name='project_groups',
    )
    status=models.CharField(_('Status'), choices=StatusChoices.choices, default=StatusChoices.FORMATION)
    conformed_on = models.DateField(_('Conformed On'), null=True, blank=True)
    conformed_by = models.ForeignKey(
        "user.Student",
        on_delete=models.PROTECT,
        related_name='conformed_student_groups',
        null=True,
        blank=True,
    )
    created_by = models.OneToOneField(
        "user.Student",
        on_delete=models.PROTECT,
        related_name='created_student_groups',
    )

class ProjectGroupInvites(TimeStampModelMixin):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("Pending")
        ACCEPTED = "accepted", _("Accepted")
        REJECTED = "rejected", _("Rejected")

    project_group = models.ForeignKey(
        ProjectGroup,
        on_delete=models.PROTECT,
        related_name='invites',
    )
    status=models.CharField(_('Status'), choices=StatusChoices.choices, default=StatusChoices.PENDING)
    student = models.OneToOneField(
        "user.Student",
        on_delete=models.PROTECT,
        related_name='invites',
    )
    expires_on = models.DateTimeField(_('Expires On'), blank=True)
    created_by = models.OneToOneField(
        "user.Student",
        on_delete=models.PROTECT,
        related_name='created_invites',
    )

    @property
    def is_expired(self):
        return timezone.now() <= self.expires_on

    def accept_invite(self):
        if not self.is_expired:
            with transaction.atomic():
                self.status = self.StatusChoices.ACCEPTED
                self.student.project_group = self
                self.student.save()
                self.save()

    def reject_invite(self):
        if not self.is_expired:
            with transaction.atomic():
                self.status = self.StatusChoices.REJECTED
                self.student.project_group = self
                self.student.save()
                self.save()

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
    report_content = models.TextField(_('Report Content'))
    abstract_content = models.TextField(_('Abstract Content'))
    status = models.CharField(_('Status'), choices=StatusChoices.choices, default=StatusChoices.NEW)
    approved_on = models.DateField(_('Approved On'), null=True, blank=True)
    completed_on = models.DateField(_('Completed On'), null=True, blank=True)
    uniqueness = PercentField(_('uniqueness'), default=0)
    project_group = models.ForeignKey(
        'project.ProjectGroup',
        verbose_name=_('Project Idea'),
        on_delete=models.PROTECT,
        related_name='ideas',
        limit_choices_to={"role": User.RoleChoices.FACULTY},
    )
    tags = TaggableManager()

    def __str__(self) -> str:
        return self.title



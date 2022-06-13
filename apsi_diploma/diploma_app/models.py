from django.db import models
from viewflow.models import Process
from django.conf import settings
import datetime


BACHELOR_OF_SCIENCE = "BS"
MASTERS = "M"
DOCTORAL = "D"
SCIENTIFIC = "S"
PAPER_TYPE_CHOICES = [
    (BACHELOR_OF_SCIENCE, "Bachelor of Science dissertation"),
    (MASTERS, "Master's dissertation"),
    (DOCTORAL, "Doctoral dissertation"),
    (SCIENTIFIC, "Scientific paper"),
]


class ScientificPublishingProcess(Process):

    title = models.TextField(max_length=500)
    description = models.TextField(max_length=5000)
    file = models.FileField()
    paper_type = models.CharField(max_length=2, choices=PAPER_TYPE_CHOICES)
    organizational_unit = models.CharField(max_length=255)


class DissertationProcess(Process):

    UNSATISFACTORY = 2.0
    SATISFACTORY = 3.0
    SATISFACTORY_PLUS = 3.5
    GOOD = 4.0
    GOOD_PLUS = 4.5
    VERY_GOOD = 5.0
    GRADE_CHOICES = (
        (UNSATISFACTORY, "Unsatisfactory"),
        (SATISFACTORY, "Satisfactory"),
        (SATISFACTORY_PLUS, "Satisfactory plus"),
        (GOOD, "Good"),
        (GOOD_PLUS, "Good plus"),
        (VERY_GOOD, "Very good"),
    )

    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="supervisor",
        blank=True,
        null=True,
    )
    topic_title = models.TextField(max_length=500)
    topic_description = models.TextField(max_length=5000)
    topic_approved = models.BooleanField(default=False)
    decision_explanation = models.TextField(
        max_length=5000, default="Nie ma nic do poprawki"
    )
    dissertation_file = models.FileField()
    dissertation_accepted = models.BooleanField(default=False)
    antiplagiat_report = models.TextField(max_length=5000, default="Pusty raport")
    antiplagiat_report_summary = models.TextField(
        max_length=5000, default="Nie ma nic do poprawki."
    )
    paper_type = models.CharField(max_length=2, choices=PAPER_TYPE_CHOICES)
    keywords = models.TextField(max_length=5000, default="")
    supervisor_review = models.TextField()
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviewer",
        blank=True,
        null=True,
    )
    reviewer_review = models.TextField()
    exam_date = models.DateField(default=datetime.date.today)
    comitee_chair = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comitee_chair",
        blank=True,
        null=True,
    )
    comitee_member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comitee_member",
        blank=True,
        null=True,
    )
    exam_grade = models.FloatField(default=UNSATISFACTORY, choices=GRADE_CHOICES)

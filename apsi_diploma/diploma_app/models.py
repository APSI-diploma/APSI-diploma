from django.db import models
from viewflow.models import Process
import datetime


class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class PaperType(models.Model):
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
    paper_type = models.CharField(
        max_length=2,
        choices=PAPER_TYPE_CHOICES,
    )


class ScientificPublishingProcess(Process):

    title = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    file = models.FileField()
    paper_type = models.ForeignKey(
        PaperType, on_delete=models.CASCADE, blank=True, null=True
    )
    organizational_unit = models.CharField(max_length=256)


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
        Employee,
        on_delete=models.CASCADE,
        related_name="supervisor",
        blank=True,
        null=True,
    )
    topic_title = models.CharField(max_length=500)
    topic_description = models.CharField(max_length=5000)
    topic_approved = models.BooleanField(default=False)
    dissertation_file = models.FileField()
    dissertation_accepted = models.BooleanField(default=False)
    paper_type = models.ForeignKey(PaperType, on_delete=models.CASCADE)
    supervisor_review = models.FileField()
    reviewer = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="reviewer",
        blank=True,
        null=True,
    )
    reviewer_review = models.FileField()
    exam_date = models.DateField(default=datetime.date.today)
    comitee_chair = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="comitee_chair",
        blank=True,
        null=True,
    )
    comitee_member = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="comitee_member",
        blank=True,
        null=True,
    )
    exam_grade = models.FloatField(default=UNSATISFACTORY, choices=GRADE_CHOICES)

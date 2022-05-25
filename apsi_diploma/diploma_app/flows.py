from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from .models import ScientificPublishingProcess, DissertationProcess


@frontend.register
class ScientificPublishingFlow(Flow):
    process_class = ScientificPublishingProcess

    start = (
        flow.Start(CreateProcessView)
        .Permission(
            auto_create=True  # tworzy permission diploma_app.can_start_scientificpublishingprocess
        )
        .Next(this.upload)
    )

    upload = (
        flow.View(UpdateProcessView, fields=["title", "description", "file"])
        .Permission(
            auto_create=True  # tworzy permission diploma_app.can_start_scientificpublishingprocess
        )
        .Next(this.categorize)
    )

    categorize = (
        flow.View(UpdateProcessView, fields=["paper_type"])
        .Permission(
            auto_create=True  # tworzy permission diploma_app.can_categorize_scientificpublishingprocess
        )
        .Next(this.end)
    )

    end = flow.End()


@frontend.register
class DissertationFlow(Flow):

    process_class = DissertationProcess

    start = (
        flow.Start(CreateProcessView)
        .Permission(auto_create=True)
        .Next(this.choose_supervisor)
    )

    choose_supervisor = (
        flow.View(UpdateProcessView, fields=["supervisor"])
        .Permission(auto_create=True)
        .Next(this.upload_topic)
    )

    upload_topic = (
        flow.View(UpdateProcessView, fields=["topic_title", "topic_description"])
        .Permission(auto_create=True)
        .Next(this.topic_approve)
    )

    topic_approve = (
        flow.View(UpdateProcessView, fields=["topic_approved"])
        .Permission(auto_create=True)
        .Next(this.check_acceptance)
    )

    check_acceptance = (
        flow.If(lambda activation: activation.process.topic_approved)
        .Then(this.upload_dissertation)
        .Else(this.choose_supervisor)
    )

    upload_dissertation = (
        flow.View(UpdateProcessView, fields=["dissertation_file"])
        .Permission(auto_create=True)
        .Next(this.antiplagiat_control)
    )

    antiplagiat_control = (
        flow.View(UpdateProcessView, fields=["dissertation_accepted"])
        .Permission(auto_create=True)
        .Next(this.check_antiplagiat)
    )

    check_antiplagiat = (
        flow.If(lambda activation: activation.process.dissertation_accepted)
        .Then(this.categorize)
        .Else(this.upload_dissertation)
    )

    categorize = (
        flow.View(UpdateProcessView, fields=["paper_type"])
        .Permission(auto_create=True)
        .Next(this.supervisor_review)
    )

    supervisor_review = (
        flow.View(UpdateProcessView, fields=["supervisor_review"])
        .Permission(auto_create=True)
        .Next(this.reviewer_review)
    )

    reviewer_review = (
        flow.View(UpdateProcessView, fields=["reviewer", "reviewer_revier"])
        .Permission(auto_create=True)
        .Next(this.add_exam_details)
    )

    add_exam_details = (
        flow.View(
            UpdateProcessView, fields=["exam_date", "comitee_chair", "comitee_member"]
        )
        .Permission(auto_create=True)
        .Next(this.add_exam_results)
    )

    add_exam_results = (
        flow.View(UpdateProcessView, fields=["exam_grade"])
        .Permission(auto_create=True)
        .Next(this.end)
    )

    end = flow.End()

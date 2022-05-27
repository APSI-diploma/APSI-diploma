from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from .models import ScientificPublishingProcess, DissertationProcess


@frontend.register
class ScientificPublishingFlow(Flow):
    process_class = ScientificPublishingProcess

    start = (
        flow.Start(CreateProcessView, task_title="Add scientific paper")
        .Permission(
            auto_create=True        # uzytkownik musi miec can_start_scientificpublishingprocess, view_scientificpublishingprocess
        )
        .Next(this.upload)
    )

    upload = (
        flow.View(UpdateProcessView, fields=["title", "description", "file"], task_title="Upload scientific paper")
        .Assign(this.start.owner)
        .Next(this.categorize)
    )

    categorize = (
        flow.View(UpdateProcessView, fields=["paper_type"], task_title="Categorize scientific paper")
        .Assign(this.start.owner)
        .Next(this.end)
    )

    end = flow.End()


@frontend.register
class DissertationFlow(Flow):

    process_class = DissertationProcess

    start = (
        flow.Start(CreateProcessView, task_title="Start dissertation process")
        .Permission(auto_create=True)
        .Next(this.choose_supervisor_and_topic)
    )

    choose_supervisor_and_topic = (
        flow.View(UpdateProcessView, fields=["supervisor", "topic_title", "topic_description"], task_title="Choose topic of dissertation and supervisor")
        .Assign(this.start.owner)
        .Next(this.topic_approve)
    )

    topic_approve = (
        flow.View(UpdateProcessView, fields=["topic_approved"])
        .Assign(lambda act: act.process.supervisor)
        .Next(this.check_acceptance)
    )

    check_acceptance = (
        flow.If(lambda activation: activation.process.topic_approved)
        .Then(this.upload_dissertation)
        .Else(this.choose_supervisor_and_topic)
    )

    upload_dissertation = (
        flow.View(UpdateProcessView, fields=["dissertation_file"])
        .Assign(this.start.owner)
        .Next(this.antiplagiat_control)
    )

    antiplagiat_control = (
        flow.View(UpdateProcessView, fields=["dissertation_accepted"])
        .Assign(lambda act: act.process.supervisor)
        .Next(this.check_antiplagiat)
    )

    check_antiplagiat = (
        flow.If(lambda activation: activation.process.dissertation_accepted)
        .Then(this.categorize)
        .Else(this.upload_dissertation)
    )

    categorize = (
        flow.View(UpdateProcessView, fields=["paper_type"])
        .Assign(this.start.owner)
        .Next(this.choose_reviewer)
    )

    choose_reviewer = (
        flow.View(UpdateProcessView, fields=["reviewer"])
        .Permission(auto_create=True)
        .Next(this.supervisor_review)
    )

    supervisor_review = (
        flow.View(UpdateProcessView, fields=["supervisor_review"])
        .Assign(lambda act: act.process.supervisor)
        .Next(this.reviewer_review)
    )

    reviewer_review = (
        flow.View(UpdateProcessView, fields=["reviewer", "reviewer_review"])
        .Assign(lambda act: act.process.reviewer)
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

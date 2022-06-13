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
            auto_create=True  # uzytkownik musi miec can_start_scientificpublishingprocess, view_scientificpublishingprocess
        )
        .Next(this.upload)
    )

    upload = (
        flow.View(
            UpdateProcessView,
            fields=["title", "description", "file"],
            task_title="Upload scientific paper",
        )
        .Assign(this.start.owner)
        .Next(this.categorize)
    )

    categorize = (
        flow.View(
            UpdateProcessView,
            fields=["paper_type"],
            task_title="Categorize scientific paper",
        )
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
        flow.View(
            UpdateProcessView,
            fields=["supervisor", "topic_title", "topic_description"],
            task_title="Choose topic of dissertation and supervisor",
        )
        .Assign(this.start.owner)
        .Next(this.can_be_supervisor)
    )

    can_be_supervisor = (
        flow.If(lambda act: (act.process.supervisor == act.process.created_by))
        .Then(this.choose_supervisor_and_topic_again)
        .Else(this.topic_approve)
    )

    choose_supervisor_and_topic_again = (
        flow.View(
            UpdateProcessView,
            fields=["supervisor", "topic_title", "topic_description"],
            task_title="Choose topic of dissertation and supervisor",
            task_description="Chosen supervisor cannot supervise the dissertation process. Please choose again.",
        )
        .Assign(this.start.owner)
        .Next(this.can_be_supervisor)
    )

    topic_approve = (
        flow.View(UpdateProcessView, fields=["topic_approved", "decision_explanation"])
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
        flow.View(
            UpdateProcessView,
            fields=[
                "dissertation_accepted",
                "antiplagiat_report",
                "antiplagiat_report_summary",
            ],
        )
        .Assign(lambda act: act.process.supervisor)
        .Next(this.check_antiplagiat)
    )

    check_antiplagiat = (
        flow.If(lambda activation: activation.process.dissertation_accepted)
        .Then(this.categorize)
        .Else(this.upload_dissertation)
    )

    categorize = (
        flow.View(UpdateProcessView, fields=["paper_type", "keywords"])
        .Assign(this.start.owner)
        .Next(this.choose_reviewer)
    )

    choose_reviewer = (
        flow.View(UpdateProcessView, fields=["reviewer"])
        .Permission(auto_create=True)
        .Next(this.supervisor_review)
    )

    can_be_reviewer = (
        flow.If(
            lambda act: (
                act.process.reviewer == act.process.created_by
                or act.process.supervisor == act.process.reviewer
            )
        )
        .Then(this.choose_reviewer_again)
        .Else(this.supervisor_review)
    )

    choose_reviewer_again = (
        flow.View(
            UpdateProcessView,
            fields=["reviewer"],
            task_description="Chosen reviewer cannot review the dissertation process. Please choose again.",
        )
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
        .Next(this.check_exam_details)
    )

    check_exam_details = (
        flow.If(
            lambda act: (
                act.process.comitee_chair == act.process.created_by
                or act.process.comitee_chair == act.process.reviewer
                or act.process.comitee_chair == act.process.supervisor
                or act.process.comitee_chair == act.process.comitee_member
                or act.process.comitee_member == act.process.created_by
                or act.process.comitee_member == act.process.supervisor
                or act.process.comitee_member == act.process.reviewer
            )
        )
        .Then(this.add_exam_details_again)
        .Else(this.add_exam_results)
    )

    add_exam_details_again = (
        flow.View(
            UpdateProcessView,
            fields=["exam_date", "comitee_chair", "comitee_member"],
            task_description="Chosen comitee is not allowed in dissertation process. Please choose again.",
        )
        .Permission(auto_create=True)
        .Next(this.check_exam_details)
    )

    add_exam_results = (
        flow.View(UpdateProcessView, fields=["exam_grade"])
        .Permission(auto_create=True)
        .Next(this.end)
    )

    end = flow.End()

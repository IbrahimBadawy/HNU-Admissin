from rest_framework import serializers
from .models import Form, Tab, Section, Question, Option, FormSubmission, Answer
from apps.users.models import AcademicYear

from rest_framework.exceptions import ValidationError


class OptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    is_archived = serializers.BooleanField(required=False)

    meta_data = serializers.JSONField(required=False)

    class Meta:
        model = Option
        fields = ["id", "title", "order", "meta_data", "is_archived"]


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    meta_data = serializers.JSONField(required=False)

    is_archived = serializers.BooleanField(required=False)
    options = OptionSerializer(many=True, required=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "title",
            "question_type",
            "is_required",
            "configs",
            "order",
            "options",
            "is_archived",
            "meta_data",
        ]


class SectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    questions = QuestionSerializer(many=True)
    meta_data = serializers.JSONField(required=False)
    is_archived = serializers.BooleanField(required=False)

    class Meta:
        model = Section
        fields = ["id", "title", "order", "questions", "meta_data", "is_archived"]


class TabSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    meta_data = serializers.JSONField(required=False)
    is_archived = serializers.BooleanField(required=False)
    sections = SectionSerializer(many=True)

    class Meta:
        model = Tab
        fields = ["id", "title", "order", "sections", "meta_data", "is_archived"]


class FormListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    is_archived = serializers.BooleanField(required=False)
    meta_data = serializers.JSONField(required=False)

    submissions_count = serializers.IntegerField(read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    academic_year = serializers.PrimaryKeyRelatedField(
        queryset=AcademicYear.objects.all(),
        required=False,
        allow_null=True
    )
    class Meta:
        model = Form
        fields = [
            "id",
            "title",
            "is_active",
            "created_at",
            "modified_at",
            "is_archived",
            "meta_data",
            "submissions_count",
            "academic_year"
        ]


class FormSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    is_archived = serializers.BooleanField(required=False)

    meta_data = serializers.JSONField(required=False)

    tabs = TabSerializer(many=True, required=True)
    submissions_count = serializers.IntegerField(read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    academic_year = serializers.PrimaryKeyRelatedField(
    queryset=AcademicYear.objects.all(), required=False, allow_null=True
)


    class Meta:
        model = Form
        fields = [
            "id",
            "title",
            "is_active",
            "created_at",
            "modified_at",
            "tabs",
            "is_archived",
            "meta_data",
            "submissions_count",
            "academic_year"
        ]

    def create(self, validated_data):
        tabs_data = validated_data.pop("tabs", [])
        form = Form.objects.create(**validated_data)
        for tab_data in tabs_data:
            sections_data = tab_data.pop("sections", [])
            tab = Tab.objects.create(form=form, **tab_data)
            for section_data in sections_data:
                questions_data = section_data.pop("questions", [])
                section = Section.objects.create(tab=tab, **section_data)
                for question_data in questions_data:
                    options_data = question_data.pop("options", [])
                    question = Question.objects.create(section=section, **question_data)
                    for option_data in options_data:
                        Option.objects.create(question=question, **option_data)
        return form

    def update(self, instance, validated_data):
        partial = self.context.get("request").method == "PATCH"
        if not partial:
            validated_data.pop("created_at", None)
            validated_data.pop("modified_at", None)

            instance.title = validated_data.get("title", instance.title)
            instance.is_active = validated_data.get("is_active", instance.is_active)
            instance.save()

            tabs_data = validated_data.pop("tabs", [])
            incoming_tab_ids = [tab.get("id") for tab in tabs_data if tab.get("id")]
            existing_tabs = {
                tab.id: tab
                for tab in Tab.objects.filter(form=instance, id__in=incoming_tab_ids)
            }
            kept_tab_ids = []

            for tab_data in tabs_data:
                sections_data = tab_data.pop("sections", [])
                tab_id = tab_data.get("id")

                if tab_id:
                    tab = existing_tabs.get(tab_id)
                    if not tab:
                        raise ValidationError(
                            f"❌ Tab ID {tab_id} not found in Form {instance.id}"
                        )
                    for attr, value in tab_data.items():
                        setattr(tab, attr, value)
                    tab.is_archived = False
                    tab.save()
                else:
                    tab = Tab.objects.create(form=instance, **tab_data)

                kept_tab_ids.append(tab.id)
                incoming_section_ids = [
                    s.get("id") for s in sections_data if s.get("id")
                ]
                existing_sections = {
                    s.id: s
                    for s in Section.objects.filter(
                        tab=tab, id__in=incoming_section_ids
                    )
                }
                kept_section_ids = []

                for section_data in sections_data:
                    questions_data = section_data.pop("questions", [])
                    section_id = section_data.get("id")

                    if section_id:
                        section = existing_sections.get(section_id)
                        if not section:
                            raise ValidationError(
                                f"❌ Section ID {section_id} not found in Tab {tab.id}"
                            )
                        for attr, value in section_data.items():
                            setattr(section, attr, value)
                        section.is_archived = False
                        section.save()
                    else:
                        section = Section.objects.create(tab=tab, **section_data)

                    kept_section_ids.append(section.id)
                    incoming_question_ids = [
                        q.get("id") for q in questions_data if q.get("id")
                    ]
                    existing_questions = {
                        q.id: q
                        for q in Question.objects.filter(
                            section=section, id__in=incoming_question_ids
                        )
                    }
                    kept_question_ids = []

                    for question_data in questions_data:
                        options_data = question_data.pop("options", [])
                        question_id = question_data.get("id")

                        if question_id:
                            question = existing_questions.get(question_id)
                            if not question:
                                raise ValidationError(
                                    f"❌ Question ID {question_id} not found in Section {section.id}"
                                )
                            for attr, value in question_data.items():
                                setattr(question, attr, value)
                            question.is_archived = False
                            question.save()
                        else:
                            question = Question.objects.create(
                                section=section, **question_data
                            )

                        kept_question_ids.append(question.id)
                        incoming_option_ids = [
                            o.get("id") for o in options_data if o.get("id")
                        ]
                        existing_options = {
                            o.id: o
                            for o in Option.objects.filter(
                                question=question, id__in=incoming_option_ids
                            )
                        }
                        kept_option_ids = []

                        for option_data in options_data:
                            option_id = option_data.get("id")

                            if option_id:
                                option = existing_options.get(option_id)
                                if not option:
                                    raise ValidationError(
                                        f"❌ Option ID {option_id} not found in Question {question.id}"
                                    )
                                for attr, value in option_data.items():
                                    setattr(option, attr, value)
                                option.is_archived = False
                                option.save()
                            else:
                                option = Option.objects.create(
                                    question=question, **option_data
                                )

                            kept_option_ids.append(option.id)

                        for opt in Option.objects.filter(question=question).exclude(
                            id__in=kept_option_ids
                        ):
                            opt.is_archived = True
                            opt.save()

                    for ques in Question.objects.filter(section=section).exclude(
                        id__in=kept_question_ids
                    ):
                        ques.is_archived = True
                        ques.save()

                for sec in Section.objects.filter(tab=tab).exclude(
                    id__in=kept_section_ids
                ):
                    sec.is_archived = True
                    sec.save()

            for t in Tab.objects.filter(form=instance).exclude(id__in=kept_tab_ids):
                t.is_archived = True
                t.save()

            return instance
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    is_archived = serializers.BooleanField(required=False)

    meta_data = serializers.JSONField(required=False)

    class Meta:
        model = Answer
        fields = ["id", "question", "answer_text", "meta_data", "is_archived"]


class FormSubmissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    is_archived = serializers.BooleanField(required=False)

    meta_data = serializers.JSONField(required=False)
    answers = AnswerSerializer(many=True, required=False)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = FormSubmission
        fields = "__all__"

    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        submission = FormSubmission.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(submission=submission, **answer_data)
        return submission

    def update(self, instance, validated_data):
        partial = self.context.get("request").method == "PATCH"
        answers_data = validated_data.pop("answers", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if not partial and answers_data is not None:
            instance.answers.all().delete()
            for answer_data in answers_data:
                Answer.objects.create(submission=instance, **answer_data)

        return instance

class AnswerWithQuestionTitleSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source="question.title", read_only=True)

    class Meta:
        model = Answer
        fields = ["question_title", "answer_text"]

class SubmissionListSerializer(serializers.ModelSerializer):
    is_archived = serializers.BooleanField(required=False)
    meta_data = serializers.JSONField(required=False)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    answers = serializers.SerializerMethodField()

    def get_answers(self, obj):
        return AnswerWithQuestionTitleSerializer(
            obj.answers.filter(answer_text__isnull=False).exclude(answer_text=""),
            many=True
        ).data
    class Meta:
        model = FormSubmission
        fields = [
            "id",
            "form",
            "status",
            "is_paied",
            "is_paied_collage",
            "notes",
            "user_identifier",
            "submitted_at",
            "is_locked",
            "modified_at",
            "meta_data",
            "is_archived",
            "answers",
            "program",
        ]

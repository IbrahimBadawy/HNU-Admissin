
from rest_framework import serializers
from .models import Form, Tab, Section, Question, Option, FormSubmission, Answer


class OptionSerializer(serializers.ModelSerializer):
    meta_data = serializers.JSONField(required=False)
    class Meta:
        model = Option
        fields = ["id", "title", "order","meta_data"]


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)
    is_archived=serializers.BooleanField(required=False)

    class Meta:
        model = Question
        fields = ["id", "title", "question_type", "is_required",'configs', "order", "options"]


class SectionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)
    meta_data = serializers.JSONField(required=False)
    is_archived=serializers.BooleanField(required=False)

    class Meta:
        model = Section
        fields = ["id", "title", "order", "questions","meta_data"]
        
    def get_questions(self, obj):
        qs = obj.questions.filter(is_archived=False).order_by("order")
        return QuestionSerializer(qs, many=True).data
        
class TabSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, required=False)
    meta_data = serializers.JSONField(required=False)
    is_archived=serializers.BooleanField(required=False)

    class Meta:
        model = Tab
        fields = ["id", "title", "order", "sections","meta_data"]
        
    def get_sections(self, obj):
        qs = obj.sections.filter(is_archived=False).order_by("order")
        return SectionSerializer(qs, many=True).data

class FormSerializer(serializers.ModelSerializer):
    tabs = TabSerializer(many=True, required=False)
    meta_data = serializers.JSONField(required=False)
    submissions_count = serializers.SerializerMethodField()
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    


    class Meta:
        model = Form
        fields = [
            "id",
            "title",
            "is_active",
            "created_at",
            "modified_at",
            "tabs",
            "meta_data",
            "submissions_count",
        ]
        read_only_fields = ["created_at", "modified_at", "submissions_count"]  # ✅ هنا

    def get_submissions_count(self, obj):
        return obj.submissions.count()
    def get_tabs(self, obj):
        qs = obj.tabs.filter(is_archived=False).order_by("order")
        return TabSerializer(qs, many=True).data
    
    
    def create(self, validated_data):
        validated_data.pop("created_at", None)
        tabs_data = validated_data.pop("tabs", [])
        form = Form.objects.create(**validated_data)
        self._create_or_update_tabs(tabs_data, form=form)
        return form

    def update(self, instance, validated_data):
        validated_data.pop("created_at", None)
        validated_data.pop("modified_at", None)
        tabs_data = validated_data.pop("tabs", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        self._sync_tabs(instance, tabs_data)
        return instance

    def _sync_tabs(self, form, tabs_data):
        existing_tabs = {tab.id: tab for tab in form.tabs.all()}
        incoming_tab_ids = []

        for tab_data in tabs_data:
            sections_data = tab_data.pop("sections", [])
            tab_id = tab_data.get("id")
            if tab_id and tab_id in existing_tabs:
                tab = existing_tabs[tab_id]
                for attr, value in tab_data.items():
                    setattr(tab, attr, value)
                tab.is_archived = False 
                tab.save()
                self._sync_sections(tab, sections_data)
                incoming_tab_ids.append(tab.id)
            else:
                tab = Tab.objects.create(form=form, **tab_data)
                self._create_or_update_sections(sections_data, tab)
                incoming_tab_ids.append(tab.id)

        for tab in form.tabs.exclude(id__in=incoming_tab_ids):
            tab.is_archived = True  # ✅ أرشف السؤال بدلاً من حذفه
            tab.save()

    def _sync_sections(self, tab, sections_data):
        existing_sections = {s.id: s for s in tab.sections.all()}
        incoming_ids = []

        for section_data in sections_data:
            questions_data = section_data.pop("questions", [])
            section_id = section_data.get("id")
            if section_id and section_id in existing_sections:
                section = existing_sections[section_id]
                for attr, value in section_data.items():
                    setattr(section, attr, value)
                section.is_archived = False  # ✅ أرجعه مرئي لو كان متأرشف

                section.save()
                self._sync_questions(section, questions_data)
                incoming_ids.append(section.id)
            else:
                section = Section.objects.create(tab=tab, **section_data)
                self._create_or_update_questions(questions_data, section)
                incoming_ids.append(section.id)

        for s in tab.sections.exclude(id__in=incoming_ids):
            s.is_archived = True  # ✅ أرشف السؤال بدلاً من حذفه
            s.save()

    def _sync_questions(self, section, questions_data):
        existing = {q.id: q for q in section.questions.all()}
        incoming_ids = []

        for question_data in questions_data:
            options_data = question_data.pop("options", [])
            q_id = question_data.get("id")
            if q_id and q_id in existing:
                question = existing[q_id]
                for attr, value in question_data.items():
                    setattr(question, attr, value)
                question.is_archived = False  # ✅ أرجعه مرئي لو كان متأرشف
                question.save()
                self._sync_options(question, options_data)
                incoming_ids.append(question.id)
            else:
                question = Question.objects.create(section=section, **question_data)
                self._create_or_update_options(options_data, question)
                incoming_ids.append(question.id)

        for q in section.questions.exclude(id__in=incoming_ids):
            q.is_archived = True  # ✅ أرشف السؤال بدلاً من حذفه
            q.save()


    def _sync_options(self, question, options_data):
        existing = {o.id: o for o in question.options.all()}
        incoming_ids = []

        for opt_data in options_data:
            o_id = opt_data.get("id")
            if o_id and o_id in existing:
                opt = existing[o_id]
                for attr, value in opt_data.items():
                    setattr(opt, attr, value)
                opt.save()
                incoming_ids.append(opt.id)
            else:
                opt = Option.objects.create(question=question, **opt_data)
                incoming_ids.append(opt.id)

        for o in question.options.exclude(id__in=incoming_ids):
            if not question.answer_set.exists():
                o.delete()

    def _create_or_update_tabs(self, tabs_data, form):
        for tab_data in tabs_data:
            sections_data = tab_data.pop("sections", [])
            tab = Tab.objects.create(form=form, **tab_data)
            self._create_or_update_sections(sections_data, tab)

    def _create_or_update_sections(self, sections_data, tab):
        for section_data in sections_data:
            questions_data = section_data.pop("questions", [])
            section = Section.objects.create(tab=tab, **section_data)
            self._create_or_update_questions(questions_data, section)

    def _create_or_update_questions(self, questions_data, section):
        for question_data in questions_data:
            options_data = question_data.pop("options", [])
            question = Question.objects.create(section=section, **question_data)
            self._create_or_update_options(options_data, question)

    def _create_or_update_options(self, options_data, question):
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
            
class AnswerSerializer(serializers.ModelSerializer):
    meta_data = serializers.JSONField(required=False)
    class Meta:
        model = Answer
        fields = ["id","question_id", "answer_text","meta_data"]


class FormSubmissionSerializer(serializers.ModelSerializer):
    meta_data = serializers.JSONField(required=False)
    answers = AnswerSerializer(many=True, required=False)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = FormSubmission
        fields = ["id","form","is_locked","user_identifier","modified_at","submitted_at","meta_data","answers"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        submission = FormSubmission.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(submission=submission, **answer_data)
        return submission

    def update(self, instance, validated_data):
        answers_data = validated_data.pop("answers",  [])  # 👈 خليه Optional

        # Update باقي الحقول العادية
        instance.user_identifier = validated_data.get(
            "user_identifier", instance.user_identifier
        )
        instance.is_locked = validated_data.get("is_locked", instance.is_locked)
        instance.save()

        # 🔥 لو فيه تحديث لـ answers، ساعتها فقط امسح القديم واعمل الجديد
        if answers_data is not None:
            instance.answers.all().delete()
            for answer_data in answers_data:
                Answer.objects.create(submission=instance, **answer_data)

        return instance
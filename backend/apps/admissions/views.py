# ✅ optimized_views_serializers.py

from django.db.models import Count, Prefetch
from rest_framework import viewsets, status, filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files.storage import default_storage
from django.db.models import Count,OuterRef, Exists, Q
from django.db.models import OuterRef, Subquery


from .models import Form, FormSubmission, Tab, Section, Question, Option,Answer
from .serializers import (
    FormSerializer,
    FormSubmissionSerializer,
    FormListSerializer,
    SubmissionListSerializer
)


class FormListViewSet(ReadOnlyModelViewSet):
    serializer_class = FormListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Form.objects.prefetch_related(
            Prefetch('tabs', queryset=Tab.objects.filter(is_archived=False).order_by('order')),
            Prefetch('tabs__sections', queryset=Section.objects.filter(is_archived=False).order_by('order')),
            Prefetch('tabs__sections__questions', queryset=Question.objects.filter(is_archived=False).order_by('order')),
            Prefetch('tabs__sections__questions__options', queryset=Option.objects.filter(is_archived=False).order_by('order')),
        ).annotate(
            submissions_count=Count('submissions', filter=Q(submissions__is_archived=False))  # ✅ فقط غير المؤرشفة
        ).order_by('-created_at')


class FormViewSet(viewsets.ModelViewSet):
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Form.objects.prefetch_related(
            Prefetch('tabs', queryset=Tab.objects.filter(is_archived=False).order_by('order')),
            Prefetch('tabs__sections', queryset=Section.objects.filter(is_archived=False).order_by('order')),
            Prefetch('tabs__sections__questions', queryset=Question.objects.filter(is_archived=False).order_by('order')),
            Prefetch('tabs__sections__questions__options', queryset=Option.objects.filter(is_archived=False).order_by('order')),
        ).annotate(
            submissions_count=Count('submissions', filter=Q(submissions__is_archived=False))  # ✅ فقط غير المؤرشفة
        ).order_by('-created_at')

    def check_admin(self):
        if not self.request.user.is_staff:
            raise PermissionDenied("يُسمح فقط للمشرفين بتنفيذ هذا الإجراء.")

    def create(self, request, *args, **kwargs):
        self.check_admin()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        self.check_admin()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.check_admin()
        instance = self.get_object()
        if instance.submissions.exists():
            return Response({"detail": "لا يمكن حذف هذا النموذج لأنه يحتوي على إجابات."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = FormSubmissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["form"]
    search_fields = ["form"]

    def get_queryset(self):
        user = self.request.user
        qs = FormSubmission.objects.select_related('form').prefetch_related(
            Prefetch('form__tabs', queryset=Tab.objects.filter(is_archived=False).order_by('order')),
            Prefetch('form__tabs__sections', queryset=Section.objects.filter(is_archived=False).order_by('order')),
            Prefetch('form__tabs__sections__questions', queryset=Question.objects.filter(is_archived=False).order_by('order')),
            Prefetch('form__tabs__sections__questions__options', queryset=Option.objects.filter(is_archived=False).order_by('order')),
            'answers__question'
        ).filter(is_archived=False)
        if not user.is_staff:
            qs = qs.filter(user_identifier=user.username)
        return qs

    def perform_create(self, serializer):
        username = self.request.user.username if self.request.user.is_authenticated else "guest"
        serializer.save(user_identifier=username)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_locked and not request.user.is_staff:
            raise PermissionDenied("You are not allowed to edit this submission. It is locked.")
        return super().update(request, *args, **kwargs)


class SubmissionListViewSet(ReadOnlyModelViewSet):
    serializer_class = SubmissionListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["form", "status", "is_paied", "is_paied_collage","is_locked", "is_archived","program"]
    search_fields = ["id", "form__title", "status", "notes", "user_identifier"]  # تأكد من وجود form__title


    def get_queryset(self):
        user = self.request.user
        qs = FormSubmission.objects.select_related('form').prefetch_related(
            Prefetch('form__tabs', queryset=Tab.objects.filter(is_archived=False).order_by('order')),
            Prefetch('form__tabs__sections', queryset=Section.objects.filter(is_archived=False).order_by('order')),
            Prefetch('form__tabs__sections__questions', queryset=Question.objects.filter(is_archived=False).order_by('order')),
            Prefetch('form__tabs__sections__questions__options', queryset=Option.objects.filter(is_archived=False).order_by('order')),
            'answers__question'
        ).filter(is_archived=False)
        if not user.is_staff:
            qs = qs.filter(user_identifier=user.username)
 

  
        # ✅ تجميع فلاتر البحث الديناميكية
        params = self.request.query_params
        filters = []

        # دعم السؤال الأساسي بدون suffix
        if params.get("question_title") or params.get("answer_text"):
            filters.append({
                "question_title": params.get("question_title", ""),
                "answer_text": params.get("answer_text", "")
            })

        # دعم أي عدد من الفلاتر باستخدام suffix
        for key in params:
            if key.startswith("question_title_"):
                suffix = key.split("_")[-1]
                q = params.get(f"question_title_{suffix}", "")
                a = params.get(f"answer_text_{suffix}", "")
                if q or a:
                    filters.append({
                        "question_title": q,
                        "answer_text": a
                    })

        # ✅ تطبيق الفلاتر باستخدام Exists
        for idx, f in enumerate(filters):
            subquery = Answer.objects.filter(
                submission=OuterRef('pk'),
                question__title__icontains=f["question_title"],
                answer_text__icontains=f["answer_text"]
            ).exclude(answer_text="").exclude(answer_text__isnull=True)
            alias = f"has_match_{idx}"
            qs = qs.annotate(**{alias: Exists(subquery)}).filter(**{alias: True})

        return qs.distinct()


class FileUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        files = request.FILES.getlist('files')
        file_urls = []
        for file in files:
            path = default_storage.save(f'uploads/{file.name}', file)
            url = default_storage.url(path)
            file_urls.append(url)
        return Response({'urls': file_urls})



class UniqueQuestionAnswersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, form_id):
        # ✅ إجلب كل الأسئلة المرتبطة بـ الفورم (حتى المكررة)
        questions = Question.objects.filter(section__tab__form_id=form_id, is_archived=False)

        # ✅ أنشئ قاموس لتجميع الإجابات حسب عنوان السؤال
        question_answers_map = {}

        for question in questions:
            title = question.title.strip()

            # ✅ اجلب الإجابات غير الفارغة لهذا السؤال
            answers = Answer.objects.filter(
                question=question,
                answer_text__isnull=False
            ).exclude(answer_text="").values_list("answer_text", flat=True)

            # ✅ اجمعهم داخل الـ dict، وأدمج بدون تكرار
            if title in question_answers_map:
                question_answers_map[title].update(set(map(str.strip, answers)))
            else:
                question_answers_map[title] = set(map(str.strip, answers))

        # ✅ تحويل الناتج إلى شكل JSON جاهز للإرجاع
        result = [
            {"question_title": title, "answers": sorted(list(answers))}
            for title, answers in question_answers_map.items()
        ]

        return Response(result)
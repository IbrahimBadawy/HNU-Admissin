import uuid
import requests
from django.apps import apps
from django.shortcuts import get_object_or_404
from requests.auth import HTTPBasicAuth
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from decimal import Decimal
from rest_framework import status as drf_status
from django.utils import timezone
from django.shortcuts import redirect
from django.db.models import Prefetch
from apps.admissions.models import Tab, Section, Question, Option
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError



from .models import Fee, Order, Payment
from .models import FeesTypes,FeesList,ProgramFee
from .serializers import FeeSerializer, OrderSerializer, PaymentSerializer
from .serializers import FeesTypesSerializer,FeesListSerializer,ProgramFeeSerializer
from rest_framework.permissions import IsAuthenticated


# إعدادات بوابة الدفع
# MERCHANT_ID = "merchant.TESTHNU"
# API_PASSWORD = "e136b96b7547e628693242bfccdac09c"
# BASE_URL = (
#     "https://banquemisr.gateway.mastercard.com/api/rest/version/100/merchant/TESTHNU"
# )

# # Production
MERCHANT_ID = "merchant.HNU"
API_PASSWORD = "a5a19446c64c0bcf3dd6f404b0beed80"
BASE_URL = (
    "https://banquemisr.gateway.mastercard.com/api/rest/version/100/merchant/HNU"
)



class FeeViewSet(viewsets.ModelViewSet):
    # queryset = Fee.objects.all()
    permission_classes = [IsAuthenticated]


    serializer_class = FeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["submission_id"]
    search_fields = ["id"]  # تأكد من وجود form__title



    def get_queryset(self):
        return Fee.objects.select_related('submission').prefetch_related(
            Prefetch('submission__form__tabs', queryset=Tab.objects.filter(is_archived=False).order_by('order')),
            Prefetch('submission__form__tabs__sections', queryset=Section.objects.filter(is_archived=False).order_by('order')),
            Prefetch('submission__form__tabs__sections__questions', queryset=Question.objects.filter(is_archived=False).order_by('order')),
            Prefetch('submission__form__tabs__sections__questions__options', queryset=Option.objects.filter(is_archived=False).order_by('order')),
            'submission__answers__question'
        )


    @action(detail=False, methods=["post"], url_path="add-to-submission")
    def add_to_submission(self, request):
        submission_id = request.data.get("submission_id")
        description = request.data.get("description")
        amount = request.data.get("amount")
        fee_list_id = request.data.get("fee_list_id")
        fee_type = request.data.get("fee_type")

        if not (submission_id and description and amount and fee_list_id):
            return Response({"error": "جميع الحقول مطلوبة"}, status=400)

        try:
            FormSubmission = apps.get_model("admissions", "FormSubmission")
            ProgramFee = apps.get_model("payments", "ProgramFee")

            submission = get_object_or_404(FormSubmission, id=submission_id)
            fees_list = get_object_or_404(ProgramFee, id=fee_list_id)

            # ✅ محاولة الإنشاء أو استرجاع الموجود
            fee, created = Fee.objects.get_or_create(
                submission=submission,
                fees_list=fees_list,
                defaults={
                    "description": description,
                    "amount": amount,
                    "fee_type": fee_type,
                }
            )

            return Response(FeeSerializer(fee).data, status=201 if created else 200)

        except Exception as e:
            return Response(
                {"error": f"حدث خطأ غير متوقع: {str(e)}"},
                status=500
            )


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["submission__id"]
    search_fields = ["submission__id"]


    def get_queryset(self):
        return Order.objects.select_related('submission').prefetch_related(
            Prefetch('submission__form__tabs', queryset=Tab.objects.filter(is_archived=False).order_by('order')),
            Prefetch('submission__form__tabs__sections', queryset=Section.objects.filter(is_archived=False).order_by('order')),
            Prefetch('submission__form__tabs__sections__questions', queryset=Question.objects.filter(is_archived=False).order_by('order')),
            Prefetch('submission__form__tabs__sections__questions__options', queryset=Option.objects.filter(is_archived=False).order_by('order')),
            'submission__answers__question'
        )

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Payment.objects.select_related('order__submission').prefetch_related(
            Prefetch('order__submission__form__tabs', queryset=Tab.objects.filter(is_archived=False).order_by('order')),
            Prefetch('order__submission__form__tabs__sections', queryset=Section.objects.filter(is_archived=False).order_by('order')),
            Prefetch('order__submission__form__tabs__sections__questions', queryset=Question.objects.filter(is_archived=False).order_by('order')),
            Prefetch('order__submission__form__tabs__sections__questions__options', queryset=Option.objects.filter(is_archived=False).order_by('order')),
            'order__submission__answers__question'
        )


class InitiatePaymentView(APIView):
    def post(self, request):
        fee_ids = request.data.get("fee_ids", [])
        form_id = request.data.get("form_id")
        order_type = request.data.get("order_type")
        submission_id = request.data.get("submission_id")
        description = ""


        if not fee_ids or not (form_id and order_type and submission_id):
            return Response({"error": "بيانات ناقصة"}, status=400)

        fees = Fee.objects.filter(id__in=fee_ids, is_paid=False)
        if not fees.exists():
            return Response({"error": "لا توجد رسوم صالحة للدفع"}, status=400)

        submission = fees.first().submission
        base_amount = sum(f.amount for f in fees)
        surcharge = round(base_amount * Decimal("0.01") + Decimal("2"), 2)
        total_amount = round(base_amount + surcharge, 2)

        order = Order.objects.create(
            id=uuid.uuid4(), submission=submission, total_amount=total_amount,order_type=order_type
        )
        order.fees.set(fees)  # ⬅️ أضف جميع الرسوم للطلب

        if (order_type=='initial'):
            description = "رسوم تقديم"
        if (order_type=='collage'):
            description = "رسوم الكلية"

        # ✅ يرجع على نفس صفحة الإدخال
        return_url = f"https://admission.hnu.edu.eg/submissions/{form_id}/{submission_id}/?order_id={order.id}"

        payload = {
            "apiOperation": "INITIATE_CHECKOUT",
            "interaction": {
                "operation": "PURCHASE",
                "returnUrl": return_url,
                "redirectMerchantUrl": return_url,
            },
            "order": {
                "currency": "EGP",
                "amount": str(total_amount),
                "id": str(order.id),
                "description": description 
            },
        }

        response = requests.post(
            f"{BASE_URL}/session",
            json=payload,
            auth=HTTPBasicAuth(MERCHANT_ID, API_PASSWORD),
            headers={"Content-Type": "application/json"},
        )

        session_data = response.json()
        order.raw_response = session_data
        order.save()

        session_id = session_data.get("session", {}).get("id")
        session_version = session_data.get("session", {}).get("version")

        checkout_url = (
            f"https://banquemisr.gateway.mastercard.com/checkout/pay/{session_id}"
            f"?checkoutVersion={session_version}"
        )

        return Response({
            "redirect_url": checkout_url,
            "order_id": str(order.id),
            "total": total_amount,
        }, status=200)


class PaymentCheckView(APIView):
    def get(self, request, order_id):
        try:
            url = f"{BASE_URL}/order/{order_id}"
            response = requests.get(
                url,
                auth=HTTPBasicAuth(MERCHANT_ID, API_PASSWORD),
                headers={"Content-Type": "application/json"},
            )
            result = response.json()
            order_status = result.get("status")
            payment_result = result.get("result")

            if order_status in ["CAPTURED"]:
                order = Order.objects.get(id=order_id)

                # تحديث order
                order.status = "paid"
                order.raw_response = result
                order.save()

                if (order.order_type=='initial'):
                    order.submission.is_paied = True
                if (order.order_type=='collage'):
                    order.submission.is_paied_collage = True


                order.submission.save()



                # تعليم الرسوم المدفوعة
                # print("###########################")
                # print("###########################")
                # print("###########################")
                # ✅ تحديث حالة الرسوم المرتبطة
                order.fees.update(is_paid=True)

                # ✅ Debug: التأكد من التحديث
                print("✅ الرسوم المدفوعة:", list(order.fees.filter(is_paid=True).values("id", "description", "amount", "is_paid","fees_list")))

                # print("###########################")
                # print("###########################")
                # print("###########################")
            
                # order.fees.filter(is_paid=False).update(is_paid=True)

                # # إنشاء سجل الدفع
                Payment.objects.update_or_create(
                    order=order,
                    defaults={
                        "status": order_status,
                        "details": result,
                        "paid_at": timezone.now(),
                    },
                )

                return Response({"success": True}, status=drf_status.HTTP_200_OK)

            return Response(
                {"success": False, "message": "لم يتم الدفع بعد"}, status=200
            )

        except Order.DoesNotExist:
            return Response({"success": False, "error": "الطلب غير موجود"}, status=404)

        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500)



class PaymentRedirectView(APIView):
    def get(self, request, order_id):
        try:
            print("++++++++++++++++++++++++++++++++++")
            url = f"{BASE_URL}/order/{order_id}"
            response = requests.get(
                url,
                auth=HTTPBasicAuth(MERCHANT_ID, API_PASSWORD),
                headers={"Content-Type": "application/json"},
            )
            result = response.json()
            status = result.get("status")
            success = status in ["SUCCESS", "CAPTURED"] or result.get("result") == "SUCCESS"

            order = Order.objects.get(id=order_id)
            if success:
                order.status = "paid"
                order.raw_response = result
                order.save()
                order.submission.fees.filter(is_paid=False).update(is_paid=True)
                Payment.objects.update_or_create(
                    order=order,
                    defaults={
                        "status": status,
                        "details": result,
                        "paid_at": timezone.now(),
                    },
                )

            # ✅ رجّع المستخدم على الفرونت
            form_id = request.GET.get("formId")
            submission_id = request.GET.get("id")
            tab_id = request.GET.get("tabId")

            # frontend_url = f"https://c4fb-41-33-164-93.ngrok-free.app/submissions/{form_id}/{submission_id}/edit/{tab_id}"
            frontend_url = f"https://admission.hnu.edu.eg/submissions/{form_id}/{submission_id}/edit/{tab_id}"
            return redirect(f"{frontend_url}?order_id={order_id}")

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        


class FeesTypesViewSet(viewsets.ModelViewSet):
    queryset = FeesTypes.objects.all()
    serializer_class = FeesTypesSerializer
    # permission_classes = [IsAuthenticated]
class FeesListViewSet(viewsets.ModelViewSet):
    queryset = FeesList.objects.all()
    serializer_class = FeesListSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['fees_types']
    search_fields = ['title']


class ProgramFeeViewSet(viewsets.ModelViewSet):
    queryset = ProgramFee.objects.all()
    serializer_class = ProgramFeeSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]  # ← فعل الفلترة هنا
    filterset_fields = ['academic_year', 'program']  # ← دول الفلاتر المسموح بيها

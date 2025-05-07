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

from .models import Fee, Order, Payment
from .serializers import FeeSerializer, OrderSerializer, PaymentSerializer

# إعدادات بوابة الدفع
MERCHANT_ID = "merchant.TESTHNU"
API_PASSWORD = "e136b96b7547e628693242bfccdac09c"
BASE_URL = (
    "https://banquemisr.gateway.mastercard.com/api/rest/version/100/merchant/TESTHNU"
)


class FeeViewSet(viewsets.ModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer

    @action(detail=False, methods=["post"], url_path="add-to-submission")
    def add_to_submission(self, request):
        submission_id = request.data.get("submission_id")
        description = request.data.get("description")
        amount = request.data.get("amount")
        print(f'######{amount}### {submission_id}### {description}##')
        if not (submission_id and description and amount):
            return Response({"error": "جميع الحقول مطلوبة"}, status=400)

        FormSubmission = apps.get_model("admissions", "FormSubmission")
        submission = get_object_or_404(FormSubmission, id=submission_id)

        fee = Fee.objects.create(
            submission=submission, description=description, amount=amount
        )
        return Response(FeeSerializer(fee).data, status=201)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class InitiatePaymentView(APIView):
    def post(self, request):
        fee_ids = request.data.get("fee_ids", [])
        form_id = request.data.get("form_id")
        tab_id = request.data.get("tab_id")
        submission_id = request.data.get("submission_id")

        if not fee_ids or not (form_id and tab_id and submission_id):
            return Response({"error": "بيانات ناقصة"}, status=400)

        fees = Fee.objects.filter(id__in=fee_ids, is_paid=False)
        if not fees.exists():
            return Response({"error": "لا توجد رسوم صالحة للدفع"}, status=400)

        submission = fees.first().submission
        base_amount = sum(f.amount for f in fees)
        surcharge = round(base_amount * Decimal("0.01") + Decimal("2"), 2)
        total_amount = round(base_amount + surcharge, 2)

        order = Order.objects.create(
            id=uuid.uuid4(), submission=submission, total_amount=total_amount
        )

        # ✅ يرجع على نفس صفحة الإدخال
        # return_url = f"https://c4fb-41-33-164-93.ngrok-free.app/submissions/{form_id}/{submission_id}/edit/{tab_id}?order_id={order.id}"
        # return_url = f"http://admission.hnu.edu.eg:83/submissions/{form_id}/{submission_id}/edit/{tab_id}?order_id={order.id}"
        # return_url = f"http://193.227.34.93/submissions/{form_id}/{submission_id}/edit/{tab_id}?order_id={order.id}"
        # return_url = f"http://pay.hnu.edu.eg/submissions/{form_id}/{submission_id}/edit/{tab_id}?order_id={order.id}"
        # return_url = f"https://admission.hnu.edu.eg/submissions/{form_id}/{submission_id}/edit/{tab_id}?order_id={order.id}"
        return_url = f"http://admission.hnu.edu.eg/submissions/{form_id}/{submission_id}/edit/{tab_id}?order_id={order.id}"
        # return_url = f"https://www.google.com/"

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
                "description": "رسوم تقديم"
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

            if order_status in ["SUCCESS", "CAPTURED"] or payment_result == "SUCCESS":
                order = Order.objects.get(id=order_id)

                # تحديث order
                order.status = "paid"
                order.raw_response = result
                order.save()

                # تعليم الرسوم المدفوعة
                order.submission.fees.filter(is_paid=False).update(is_paid=True)

                # إنشاء سجل الدفع
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

            frontend_url = f"http://c4fb-41-33-164-93.ngrok-free.app/submissions/{form_id}/{submission_id}/edit/{tab_id}"
            # frontend_url = f"https://admission.hnu.edu.eg/submissions/{form_id}/{submission_id}/edit/{tab_id}"
            return redirect(f"{frontend_url}?order_id={order_id}")

        except Exception as e:
            return Response({"error": str(e)}, status=500)
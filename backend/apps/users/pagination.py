from rest_framework.pagination import PageNumberPagination

class ProgramPagination(PageNumberPagination):
    page_size = 2000  # default
    page_size_query_param = 'page_size'
    max_page_size = 100000  # ← أعلى قيمة مسموح بيها من العميل

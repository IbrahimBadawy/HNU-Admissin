from .models import Form 
Form.objects.all().delete()
from .models import FormSubmission 
FormSubmission.objects.all().delete()

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

onMounted(async () => {
  const token = localStorage.getItem('access');
  const is_staff_raw = localStorage.getItem('user_is_staff');
  const is_staff = is_staff_raw === 'true'; // ✅ تأكيد إنه boolean حقيقي

  if (token) {
    try {
      const res = await axios.get('/api/admissions/submissions-list/');
      const submissions = res.data || [];
    //   console.log(res.data)

      if (is_staff) {
        router.push('/forms');
      } else {
        if (submissions.length > 0) {
          router.push('/submissions');
        } else {
          router.push('/forms');
        }
      }
    } catch (error) {
      console.error('Redirect failed:', error);
      // fallback in case of error
      router.push('/forms');
    }
  } else {
    router.push('/welcome');
  }
});
</script>

<template>
  <div class="relative min-h-screen flex items-center justify-center">
    <!-- 🌄 Background Image -->
    <img src="/assets/images/hnu-campus.jpg" alt="HNU Background"
      class="absolute inset-0 w-full h-full object-cover z-0" />

    <!-- 🌑 Overlay -->
    <div class="absolute inset-0 bg-black bg-opacity-70 z-10"></div>

    <!-- 📦 Content -->
    <div class="relative z-20 text-center px-6 max-w-3xl space-y-8">
      <!-- 🔰 Logo Image -->
      <img src="/assets/images/logo.png" alt="Logo" class="mx-auto w-28 h-28 mb-6" />

      <!-- 🏷️ Title -->
      <h1 class="text-3xl sm:text-5xl font-bold text-white mb-2">
        منصة التقديم
      </h1>
      <h1 class="text-3xl sm:text-5xl font-bold text-blue-200 mb-2">
        لجامعة حلوان الأهلية
      </h1>
      <h3 class="text-xl sm:text-3xl font-semibold text-yellow-300 mb-6">
        للعام الجامعي 2025-2026
      </h3>

      <!-- 📝 Subtitle -->
      <p class="text-lg sm:text-xl text-blue-100 mb-8">
        سجل الآن وابدأ رحلتك التعليمية ✨
      </p>
      <!-- 📝 Subtitle -->

      <!-- 🔐 Actions -->
      <div class="flex flex-col sm:flex-row justify-center gap-4">
        <button @click="signin_go"
          class="px-6 py-3 bg-blue-600 text-white font-semibold rounded shadow hover:bg-blue-700">
          تسجيل الدخول
        </button>
        <button @click="visible = true"
          class="px-6 py-3 bg-yellow-300 text-black font-semibold rounded shadow hover:bg-yellow-400">
          إنشاء حساب جديد
        </button>
      </div>

      <Dialog v-model:visible="visible" modal header="شروط وأحكام خاصة بالقبول في الجامعة" :style="{ width: '25rem' }">
        <!-- <span class="text-surface-500 dark:text-surface-400 block mb-8">شروط وأحكام خاصة بالقبول في الجامعة</span> -->
        <div class="flex flex-col items-center gap-4 mb-4">
          <p>* يجب التأكد من أن جميع بياناتك وشهاداتك، ودرجاتك، المسجلة علي رابط التقديم صحيحة ودقيقة، وفي حالة إكتشاف
            خلاف ذلك، سيتم إلغاء قبولك وأي أثر يكون قد ترتب عليه، وتحتفظ الجامعة بحقها في إتخاذ الإجراءات القانونية
            المناسبة بهذا الشأن.</p>
          <p>* يجب أن يكون الطالب لائقا صحياً وبدنياً الالتحاق بالكلية التي يرغبها، حيث أنه في حالة قبول الطالب ثم يكتشف
            عدم لياقته البدنية والصحية والطبية، سيتم إلغاء قبوله فوراً وتقع مسئولية ذلك عليه، وعلي ولي الأمر.</p>
          <p>* الجامعة ليس لها أي وسطاء أو مكاتب أو جهات تمثلها، والتقديم يتم إلكترونياً فقط عن طريق هذا الرابط.</p>
          <p>* يجب أن يقوم الطالب بسداد مبلغ 1500 جنيه، رسوم تسجيل، ويتم سدادها من خلال أخر خطوة من هذا البرنامج، مع العلم أنه في حالة عدم السداد لن يتم مراجعة أوراق وشهادات الطالب، ولن يتم قبوله.</p>
          <p>* وإدارة الجامعة تتمني لجميع الطلاب التوفيق والنجاح.</p>

        </div>

        <div class="flex justify-end gap-2">
          <Button type="button" label="لا اوافق" severity="secondary" @click="visible = false"></Button>
          <Button type="button" label="أوافق" @click="signup_go"></Button>
        </div>
      </Dialog>
      
      <p class="text-md sm:text-md text-blue-100 mb-8">
        © 2025. جميع الحقوق محفوظة - مركز الاتصالات وتكنلوجيا المعلومات - جامعة حلوان. </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();

const visible = ref(false);
const visible2 = ref(false);

const signin_go = () => {
  // visible.value = false
  router.push('/auth/signin/')
}
const signup_go = () => {
  visible.value = false
  router.push('/auth/signup/')
}


</script>
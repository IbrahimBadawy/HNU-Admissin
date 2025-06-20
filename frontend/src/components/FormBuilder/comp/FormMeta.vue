<template>
  <div class="space-y-6">
    <!-- عنوان النموذج -->
    <div>
      <label class="font-semibold block mb-1">عنوان النموذج</label>
      <input v-model="form.title" class="input w-full" placeholder="ادخل عنوان النموذج" />
    </div>

    <!-- وصف النموذج -->
    <div>
      <label class="font-semibold block mb-1">وصف النموذج</label>
      <textarea v-model="form.meta_data.description" class="input w-full" placeholder="ادخل وصف النموذج"></textarea>
    </div>

    <!-- تفعيل النموذج -->
    <div class="flex flex-col sm:flex-row gap-2 sm:gap-4 items-start sm:items-center">
      <label class="font-semibold">تفعيل النموذج</label>
      <input type="checkbox" v-model="form.is_active" />
    </div>

    <!-- أعدادات العدد -->
    <div class="flex flex-col sm:flex-row gap-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2">
        <label class="font-semibold">اقصى عدد للمتقدمين</label>
        <input type="number" v-model.number="form.meta_data.submissonsCount" class="input w-full sm:w-24" min="0" />
      </div>
      <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2">
        <label class="font-semibold">اقصى عدد للمستخدم</label>
        <input type="number" v-model.number="form.meta_data.userSubmitCount" class="input w-full sm:w-24" min="0" />
      </div>
    </div>

    <!-- التواريخ -->
    <div class="flex flex-col sm:flex-row gap-4">
      <div class="w-full sm:w-auto">
        <label class="font-semibold block mb-1">تاريخ البداية</label>
        <flat-pickr v-model="form.meta_data.date_start" class="input w-full" :config="dateTime" />
      </div>
      <div class="w-full sm:w-auto">
        <label class="font-semibold block mb-1">تاريخ النهاية</label>
        <flat-pickr v-model="form.meta_data.date_end" class="input w-full" :config="dateTime" />
      </div>
      <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2">
        <label class="font-semibold">تجاهل التوقيت</label>
        <input type="checkbox" v-model="form.meta_data.ignore_date" />
      </div>
    </div>
  </div>
</template>
  
  <script setup>
  import flatPickr from 'vue-flatpickr-component'
  import 'flatpickr/dist/flatpickr.css'
  
  const props = defineProps({
    form: Object
  })
  
  const dateTime = {
    enableTime: true,
    dateFormat: 'Y-m-d H:i',
    position: 'auto right'
  }
  </script>
  
  <style scoped>
  .input {
    @apply border border-gray-300 rounded px-3 py-2 w-full;
  }
  </style>
  
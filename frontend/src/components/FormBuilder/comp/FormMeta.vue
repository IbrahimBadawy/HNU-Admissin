<template>
    <div class="space-y-4">
      <div>
        <label class="font-semibold block mb-1">عنوان النموذج</label>
        <input v-model="form.title" class="input" placeholder="ادخل عنوان النموذج" />
      </div>
  
      <div>
        <label class="font-semibold block mb-1">وصف النموذج</label>
        <textarea v-model="form.meta_data.description" class="input" placeholder="ادخل وصف النموذج"></textarea>
      </div>
  
      <div class="flex gap-4 items-center">
        <label class="font-semibold">تفعيل النموذج</label>
        <input type="checkbox" v-model="form.is_active" />
      </div>
  
      <div class="flex gap-4">
        <div class="flex items-center">
          <label class="font-semibold mr-2">اقصى عدد للمتقدمين</label>
          <input type="number" v-model.number="form.meta_data.submissonsCount" class="input w-24" min="0" />
        </div>
        <div class="flex items-center">
          <label class="font-semibold mr-2">اقصى عدد للمستخدم</label>
          <input type="number" v-model.number="form.meta_data.userSubmitCount" class="input w-24" min="0" />
        </div>
      </div>
  
      <div class="flex gap-4">
        <div>
          <label class="font-semibold block mb-1">تاريخ البداية</label>
          <flat-pickr v-model="form.meta_data.date_start" class="input" :config="dateTime" />
        </div>
        <div>
          <label class="font-semibold block mb-1">تاريخ النهاية</label>
          <flat-pickr v-model="form.meta_data.date_end" class="input" :config="dateTime" />
        </div>
        <div class="flex gap-4 items-center">
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
  
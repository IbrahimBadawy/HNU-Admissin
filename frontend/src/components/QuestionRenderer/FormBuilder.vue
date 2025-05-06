<template>
  <div class="p-4 space-y-6">
    <!-- أزرار تغيير الوضع -->
    <div class="flex gap-4 mb-6">
      <button
        v-for="m in ['create', 'edit', 'view']"
        :key="m"
        class="btn"
        :class="{ 'bg-gray-500': mode === m }"
        @click="mode = m"
      >
        {{ m.toUpperCase() }} Mode
      </button>
    </div>

    <!-- عرض الأسئلة -->
    <div
      v-for="(question, index) in questions"
      :key="question.id"
      class="border p-4 rounded shadow"
    >
      <h3 class="font-semibold mb-2">{{ question.label }}</h3>
      <QuestionRenderer
        :type="question.type"
        :mode="mode"
        v-model="answers[question.id]"
        :configs="question.configs || {}"
        v-model:errorState="errors[question.id]"
      />
    </div>

    <!-- زر الإرسال في وضع edit -->
    <div v-if="mode === 'edit'" class="mt-6">
      <button class="btn" @click="submit"   :disabled="hasErrors" >Submit</button>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref,computed  } from 'vue'
import QuestionRenderer from './QuestionRenderer.vue'

// وضع الفورم: 'create' لتهيئة الأسئلة، 'edit' لتعبئة البيانات، 'view' للعرض فقط
const mode = ref('edit')

const questions = ref([
  {
    id: 'q1',
    label: 'Your Name',
    type: 'text',
    configs: { placeholder: 'Enter your name',answer:'aaaaaaa' },
  },
  {
    id: 'q2',
    label: 'Tell us about yourself',
    type: 'textarea',
    configs: { placeholder: 'Short bio' },
  },
  {
    id: 'q3',
    label: 'Select your city',
    type: 'select',
    configs: {
      options: [
        { value: 'cairo', label: 'Cairo' },
        { value: 'alex', label: 'Alexandria' },
      ],
    },
  },
  {
    id: 'q4',
    label: 'Choose your interests',
    type: 'checkbox',
    configs: {
      options: [
        { value: 'design', label: 'Design' },
        { value: 'coding', label: 'Coding' },
        { value: 'marketing', label: 'Marketing' },
      ],
    },
  },
  {
    id: 'q5',
    label: 'Upload your CV',
    type: 'file-upload',
    configs: {
      maxSize: 2,
      fileTypes: 'application/pdf',
    },
  },
  {
    id: 'q6',
    label: 'Rate your experience order',
    type: 'draggable',
    configs: {},
  },
  {
    id: 'q7',
    label: 'Make a payment',
    type: 'payment',
    configs: {},
  },
  {
  id: 'q8',
  label: 'Date of Birth',
  type: 'date',
  configs: {}, // ممكن تضيف خصائص في المستقبل لو حبيت
},
])

const answers = reactive({
  q1: '',
  q2: '',
  q3: '',
  q4: [],
  q5: null,
  q6: ['UX', 'UI', 'Motion'],
  q7: '',
  q8: '',
})
const errors = reactive({
  q1: false,
  q2: false,
  q3: false,
  q4: false,
  q5: false,
  q6: false,
  q7: false,
  q8: false,

})

const hasErrors = computed(() => Object.values(errors).includes(true))


function submit() {
  console.log('Submitted answers:', answers)
  alert('Form submitted successfully 🎉')
}
</script>

<style scoped>
.btn {
  padding: 10px 20px;
  background: #2c7be5;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  transition: 0.3s;
}
.btn.bg-gray-500 {
  background: #6b7280;
}
</style>

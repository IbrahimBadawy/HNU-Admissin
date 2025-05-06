<template>
  <div class="space-y-2">
    <!-- 📝 وضع view -->
    <div v-if="mode === 'view'">
      {{ modelValue }}
    </div>

    <!-- ✅ وضع edit مع التحقق من الشروط -->
    <div v-else-if="mode === 'edit'">
      <input
        type="number"
        class="input"
        :value="modelValue"
        @input="handleInput"
      />
      <p v-if="error" class="text-red-600 text-sm mt-1">{{ error }}</p>
    </div>

    <!-- ⚙️ وضع create -->
    <div v-else>
      <label class="block font-semibold mb-1">Placeholder</label>
      <input
        type="number"
        v-model="configs.placeholder"
        class="input"
      />

      <Validator
        :rules="configs.rules || []"
        :questionType="'number'"
        @update:rules="(val) => (configs.rules = val)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Validator from '../Validator.vue'
import { validateValue } from '../utils/validation'

const props = defineProps(['modelValue', 'mode', 'configs','errorState'])
const emit = defineEmits(['update:modelValue','update:errorState'])

const error = ref(null)

function handleInput(e) {
  const val = e.target.value
  emit('update:modelValue', val)

  error.value = validateValue(val, props.configs?.rules || [],'number')
  emit('update:errorState', !!error.value)
  
}
</script>

<style scoped>
.input {
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 6px 10px;
  width: 100%;
}
</style>

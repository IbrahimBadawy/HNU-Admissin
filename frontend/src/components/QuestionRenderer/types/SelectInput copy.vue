<template>
    <div v-if="mode === 'edit'">
      <Dropdown
        class="w-full"
        :options="filteredOptions"
        optionLabel="title"
        optionValue="title"
        :modelValue="modelValue"
        @update:modelValue="handleInput"
        placeholder="اختر من القائمة"
      />
      <p v-if="error" class="text-red-600 text-sm mt-1">{{ error }}</p>
    </div>
  
    <div v-else-if="mode === 'view'">
      {{ displayLabel }}
    </div>
  
    <div v-else>
      <Validator
        :rules="configs.rules || []"
        :questionType="'select'"
        @update:rules="(val) => (configs.rules = val)"
      />
    </div>
  </template>
  
  <script setup>
  import { computed, ref } from 'vue';
  import Dropdown from 'primevue/dropdown';
  import Validator from '../Validator.vue';
  import { validateValue } from '../utils/validation';
  
  const props = defineProps(['modelValue', 'mode', 'configs', 'options', 'errorState']);
  const emit = defineEmits(['update:modelValue', 'update:errorState']);
  
  const error = ref(null);
  
  // ✅ الفلترة: استبعاد العناصر المقفولة
  const filteredOptions = computed(() => {
    return props.options?.filter((opt) => !opt.meta_data?.is_locked) || [];
  });
  
  // ✅ التغيير
  function handleInput(value) {
    emit('update:modelValue', value);
    error.value = validateValue(value, props.configs?.rules || [], 'select');
    emit('update:errorState', !!error.value);
  }
  
  // ✅ عرض قيمة العرض فقط
  const displayLabel = computed(() => {
    const match = props.options?.find((o) => o.title === props.modelValue);
    return match?.title || props.modelValue;
  });
  </script>
  
  <style scoped>
  /* ممكن تزود تعديلات ستايل هنا لو حبيت */
  </style>
  
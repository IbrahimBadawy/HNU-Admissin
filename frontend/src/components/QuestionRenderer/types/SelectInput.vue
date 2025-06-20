<template>
    <div v-if="mode === 'edit'">
        <Dropdown
  class="w-full"
  :options="groupedOptions"
  optionGroupLabel="faculty"
  optionGroupChildren="programs"
  optionLabel="title"
  optionValue="full"
  :modelValue="modelValue"
  @update:modelValue="handleInput"
  placeholder="اختر "
/>
        <p v-if="error" class="text-red-600 text-sm mt-1">{{ error }}</p>
    </div>

    <div v-else-if="mode === 'view'">
        {{ displayLabel }}
    </div>

    <div v-else>
        <Validator :rules="configs.rules || []" :questionType="'select'"
            @update:rules="(val) => (configs.rules = val)" />
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

// ✅ فلترة وترتيب الخيارات
const groupedOptions = computed(() => {
  const map = {};
  // console.log(props.options)
  props.options?.forEach((opt) => {
    if (opt.meta_data?.is_locked) return;

    let faculty = '';
    let program = opt.title;

    if (opt.title.includes(' - ')) {
      const parts = opt.title.split(' - ');
      faculty = parts[0].trim();
      program = parts.slice(1).join(' - ').trim(); // في حالة وجود أكثر من "-"
    }

    if (!map[faculty]) {
      map[faculty] = {
        faculty: faculty,
        programs: [],
      };
    }

    map[faculty].programs.push({
      title: program,
      full: opt.title, // ← القيمة اللي هترجع
    });
  });

  return Object.values(map);
});
// ✅ الحدث
function handleInput(val) {
  emit('update:modelValue', val);
  error.value = validateValue(val, props.configs?.rules || [], 'select');
  emit('update:errorState', !!error.value);
}

// ✅ عرض label في حالة view
const displayLabel = computed(() => props.modelValue);

</script>

<style scoped>
/* ممكن تزود تعديلات ستايل هنا لو حبيت */
</style>
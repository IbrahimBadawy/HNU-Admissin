<template>
  <div v-if="options.length > 0">
      <div v-if="mode === 'edit'">
          <label v-for="opt in options" :key="opt.title" class="block">
              <div v-if="!opt.meta_data.is_locked">
                  <input type="checkbox" :value="opt.title" :checked="Array.isArray(parsedArray) && parsedArray.includes(opt.title)" @change="handleInput" />
                  {{ opt.title }}
              </div>
              <div v-else>
                  {{ `${opt.title} ( ${question.meta_data.depend_question.name.split('|')[2]} لا يسمح)` }}
              </div>
          </label>


          <draggable :list="options" handle=".handle" :animate="200" group="options-drag" @end="handleInput">
                <div v-for="(option, index) in options" :key="option.order" class="flex gap-2 items-center border rounded px-2 py-1 bg-gray-50">


                        <div  class="flex w-full border p-3 rounded mt-2 bg-white">
                            <input v-model="option.title" class="input w-full" placeholder="عنوان الاختيار" @change="emitOptions" />
                            <button @click="copyOption(index)" class="w-15">📄</button>
                            <button @click="removeOption(index)" class="w-15">🗑</button>
                            <span class="handle cursor-move w-15">↕️</span>
                        </div>
    
                        <QuestionRenderer :type="'optionsComp'" :mode="'create'" :configs="props.configs || {}" :option="option || {}" :q_type="local_q_type" />
                </div>
            </draggable>

          <p v-if="error" class="text-red-600 text-sm mt-1">{{ error }}</p>
      </div>

      <div v-else-if="mode === 'view'">
          <div v-if="Array.isArray(parsedArray) && options">
              <label v-for="opt in options" :key="opt.title" class="block">
                  <div v-if="!opt.meta_data.is_locked">
                      <input type="checkbox" :value="opt.title" :checked="Array.isArray(parsedArray) && parsedArray.includes(opt.title)" disabled />
                      {{ opt.title }}
                  </div>
                  <div v-else>
                      {{ `${opt.title} ( ${question.meta_data.depend_question.name.split('|')[2]} لا يسمح)` }}
                  </div>
              </label>
          </div>
          <div v-else class="text-gray-400 italic">No options selected</div>
      </div>

      <div v-else>
          <Validator :rules="configs.rules || []" :questionType="'checkbox'" @update:rules="(val) => (configs.rules = val)" />
      </div>
  </div>
</template>

<script setup>
  import { ref, watch, computed } from 'vue';
  import Validator from '../Validator.vue';
  import { validateValue } from '../utils/validation';
  import { VueDraggableNext as draggable } from 'vue-draggable-next';


  const props = defineProps(['modelValue', 'mode', 'configs', 'options', 'errorState', 'question']);
  const emit = defineEmits(['update:modelValue', 'update:errorState']);

  const error = ref(null);
  const parsedArray = computed(() => {
      try {
          return JSON.parse(props.modelValue || '[]');
      } catch (e) {
          // console.error('Invalid JSON in modelValue', e);
          return [];
      }
  });
  function toggleArrayValue(arr, val) {
      if (arr.includes(val)) return arr.filter((v) => v !== val);
      else return [...arr, val];
  }

  function handleInput(e) {
      const val = e.target.value;
      toggleValue(val);

      // بعد التعديل، تحقق من القيم الجديدة
      const updated = Array.isArray(props.modelValue) ? toggleArrayValue([...props.modelValue], val) : [val];

      error.value = validateValue(updated, props.configs?.rules || [], 'checkbox');
      emit('update:errorState', !!error.value);
  }

  function toggleValue(value) {
      let updated = Array.isArray(props.modelValue) ? [...props.modelValue] : [];

      if (updated.includes(value)) {
          updated = updated.filter((v) => v !== value);
      } else {
          updated.push(value);
      }

      emit('update:modelValue', updated);
  }
</script>

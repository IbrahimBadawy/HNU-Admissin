<template>
  <ul v-if="mode === 'edit'">
    <li
      v-for="(item, index) in options"
      :key="item"
      draggable="true"
      @dragstart="startDrag(index)"
      @dragover.prevent
      @drop="onDrop(index)"
      class="border p-2 my-1 bg-white shadow-sm cursor-move"
    >
      {{ item.title }}
    </li>
  </ul>

  <div v-else-if="mode === 'view'">
    <div v-for="item in options" :key="item">{{ item.title }}</div>
  </div>

  <div v-else>
    <!-- <label>Initial Items (comma-separated)</label>
    <input
      class="input"
      v-model="rawItems"
      @blur="updateconfigs"
    /> -->
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
const props = defineProps(['modelValue', 'mode', 'configs', 'options','question'])
const emit = defineEmits(['update:modelValue'])

const rawItems = ref((props.configs.items || []).join(','))
const items = ref([...props.modelValue])
let draggedIndex = null

const startDrag = (index) => {
  draggedIndex = index
}

const onDrop = (index) => {
  const temp = [...items.value]
  const moved = temp.splice(draggedIndex, 1)[0]
  temp.splice(index, 0, moved)
  items.value = temp
  emit('update:modelValue', temp)
}

function updateconfigs() {
  const arr = rawItems.value.split(',').map((v) => v.trim())
  props.configs.items = arr
  emit('update:modelValue', [...arr])
}
</script>

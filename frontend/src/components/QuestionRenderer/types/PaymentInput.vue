<template>
  <input
    v-if="mode === 'edit'"
    type="number"
    class="input"
    :value="modelValue"
    placeholder="EGP"
    @input="$emit('update:modelValue', $event.target.value)"
  />

  <div v-else-if="mode === 'view'">{{ modelValue }} EGP</div>

  <div v-else>
    <p>No configs needed for payment.</p>
  </div>
</template>

<script setup>
defineProps(['modelValue', 'mode'])
defineEmits(['update:modelValue'])
</script>

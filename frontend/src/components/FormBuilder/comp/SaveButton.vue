<template>

    <div class="text-center mt-6">
        <button v-if="!props.formID" class="btn btn-primary" @click="handleSave">💾انشاء نموذج جديد </button>
        <button v-else class="btn btn-primary" @click="handleEdit">💾 حفظ النموذج</button>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';


    const emit = defineEmits(['save','edit']);
    const props = defineProps(['formID','data']);

    onMounted(() => {
        // console.log('Form ID:', props.formID);
    });

    function handleSave() {
        emit('save');
    }
    function handleEdit() {
        emit('edit');
    }


</script>

<style scoped>
    .btn {
        @apply bg-blue-600 text-white font-bold px-6 py-2 rounded shadow hover:bg-blue-700 transition;
    }
</style>

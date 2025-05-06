<template>
    <div class="mt-3 space-y-2">
        <div class="flex justify-between items-center">
            <h4 class="font-semibold">الاختيارات</h4>
            <button class="btn btn-sm btn-primary" @click="addOption">+ إضافة اختيار</button>
        </div>
        <div class="flex items-center space-x-4">
            <label class="block font-semibold mb-1">نوع حقل الشرط</label>
            <label class="flex items-center space-x-1">
                <input type="radio" value="text" v-model="local_q_type" :name="`questionType`" />
                <span>نص</span>
            </label>

            <label class="flex items-center space-x-1">
                <input type="radio" value="number" v-model="local_q_type" :name="`questionType`" />
                <span>رقم</span>
            </label>

            <label class="flex items-center space-x-1">
                <input type="radio" value="date" v-model="local_q_type" :name="`questionType`" />
                <span>تاريخ</span>
            </label>
        </div>
        <draggable :list="localOptions" handle=".handle" :animate="200" group="options" @end="emitOptions">
            <div v-for="(option, index) in localOptions" :key="option.order" class="flex gap-2 items-center border rounded px-2 py-1 bg-gray-50">
                <div class=" flex w-full border p-3 rounded mt-2 bg-white">
                    <input v-model="option.title" class="input w-full " placeholder="عنوان الاختيار" @change="emitOptions" />
                    <button @click="copyOption(index)" class="w-15 " >📄</button>
                    <button @click="removeOption(index)"class="w-15 ">🗑</button>
                    <span class="handle cursor-move w-15 ">↕️</span>
                </div>
                <QuestionRenderer :type="'optionsComp'" :mode="'create'" :configs="props.configs || {}" :option="option || {}"  :q_type="local_q_type" />
            </div>
        </draggable>
    </div>
</template>

<script setup>
    import { ref, watch,onMounted } from 'vue';
    import { VueDraggableNext as draggable } from 'vue-draggable-next';
    import QuestionRenderer from '@/components/QuestionRenderer/QuestionRenderer.vue';

    const props = defineProps({
        options: {
            type: Array,
            required: true,
        },
        configs: {
            type: Object,
        },
        q_type: {
            type: String,
        },
    });
    const emit = defineEmits(['update:options']);
    const localOptions = ref([]);
    const local_q_type = ref(props.q_type);
    
    
    // تحديث localOptions مع الحفاظ على جميع الخصائص
    watch(
        () => props.options,
        (val) => {
            if (!Array.isArray(val)) return;
            localOptions.value = val.map((opt, index) => ({
                ...opt, // احتفظ بجميع الخصائص الأصلية
                order: index + 1, // أضف/حدث الحقل order
            }));
        },
        { immediate: true, deep: true }
    );


    function emitOptions() {
        // تحديث الـ order حسب الترتيب الحالي
        localOptions.value.forEach((opt, index) => {
            opt.order = index + 1;
        });
        // إرسال جميع الخصائص دون إزالة أي منها
        emit(
            'update:options',
            localOptions.value.map((opt) => ({ ...opt }))
        );
    }

    function addOption() {
        localOptions.value.push({
            title: '',
            order: localOptions.value.length + 1,
            meta_data: {
                rules:[]
            }
        });
        emitOptions();
    }

    function copyOption(index) {
        const clone = { ...localOptions.value[index] };
        localOptions.value.splice(index + 1, 0, clone);
        emitOptions();
    }

    function removeOption(index) {
        localOptions.value.splice(index, 1);
        emitOptions();
    }
</script>

<style scoped>
    .input {
        @apply border border-gray-300 rounded px-2 py-1;
    }
    .btn {
        @apply bg-blue-600 text-white px-3 py-1 rounded;
    }
</style>

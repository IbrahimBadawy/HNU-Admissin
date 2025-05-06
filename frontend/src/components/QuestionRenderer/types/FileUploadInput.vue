<template>
    <!-- 🛠 إعدادات في وضع create -->
    <div v-if="mode === 'create'" class="space-y-2">
        <label class="block font-semibold">Max File Size (MB):</label>
        <input type="number" v-model="configsLocal.maxSize" class="input" />

        <label class="block font-semibold">Max Files Count:</label>
        <input type="number" v-model="configsLocal.maxFiles" class="input" />

        <label class="block font-semibold">Allowed File Types:</label>
        <div class="flex flex-wrap gap-2">
            <label v-for="type in fileTypeOptions" :key="type.value" class="flex items-center gap-1">
                <input type="checkbox" v-model="selectedTypes" :value="type.value" />
                {{ type.label }}
            </label>
        </div>
    </div>

    <!-- 📄 في وضع edit -->
    <div v-else-if="mode === 'edit'" class="space-y-4">
        <div class="relative w-full">
            <input
                id="file-upload"
                type="file"
                :accept="acceptedTypes"
                multiple
                @change="handleFileChange"
                class="absolute inset-0 opacity-0 w-full h-full cursor-pointer z-20"
            />
            <label
                for="file-upload"
                class="inline-block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded cursor-pointer z-10 relative"
            >
                📁 اختر الملفات
            </label>
            <p class="mt-1 text-sm text-gray-500">
                {{ selectedFileNames.length ? selectedFileNames.join(', ') : 'لم يتم اختيار ملفات بعد' }}
            </p>
        </div>

        <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>

        <!-- ✅ عرض الملفات القديمة -->
        <div v-if="Array.isArray(oldLinks) && oldLinks.length" class="flex flex-wrap gap-4 mt-4">
            <div
                v-for="(link, idx) in oldLinks"
                :key="idx"
                class="flex flex-col items-center w-[200px] border rounded p-2 shadow-sm bg-white dark:bg-[#1b2e4b]"
            >
                <template v-if="isImage(link)">
                    <a :href="baseURL + link" target="_blank">
                        <img :src="baseURL + link" alt="uploaded" class="max-w-[180px] max-h-[160px] object-contain" />
                    </a>
                </template>
                <template v-else>
                    <a :href="baseURL + link" target="_blank" class="text-center">
                        <img src="/assets/images/file-placeholder.jpg" class="max-w-[100px] opacity-50 mx-auto" />
                    </a>
                </template>
                <p class="text-gray-400 italic mt-2 text-xs text-center truncate w-full" :title="getFileName(link)">
                    {{ truncateText(getFileName(link), 50) }}
                </p>
                <button @click="removeFile(idx)" class="text-red-600 text-sm mt-1">🗑 حذف</button>
            </div>
        </div>
    </div>

    <!-- 🔍 في وضع view -->
    <div v-else-if="mode === 'view'" class="text-sm space-y-2">
        <div v-if="Array.isArray(oldLinks) && oldLinks.length" class="flex flex-wrap gap-4 mt-2">
            <div
                v-for="(link, idx) in oldLinks"
                :key="idx"
                class="flex flex-col items-center w-[200px] border rounded p-2 shadow-sm bg-white dark:bg-[#1b2e4b]"
            >
                <template v-if="isImage(link)">
                    <a :href="baseURL + link" target="_blank">
                        <img :src="baseURL + link" alt="uploaded" class="max-w-[180px] max-h-[160px] object-contain" />
                    </a>
                </template>
                <template v-else>
                    <a :href="baseURL + link" target="_blank" class="text-center">
                        <img src="/assets/images/file-placeholder.jpg" class="max-w-[100px] opacity-50 mx-auto" />
                    </a>
                </template>
                <p class="text-gray-400 italic mt-2 text-xs text-center truncate w-full" :title="getFileName(link)">
                    {{ truncateText(getFileName(link), 50) }}
                </p>
            </div>
        </div>

        <div v-else class="text-center">
            <img src="/assets/images/file-placeholder.jpg" alt="لا يوجد ملفات" class="mx-auto max-w-[150px] opacity-50" />
            <p class="text-gray-400 italic mt-2">لا يوجد ملفات مرفوعة</p>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, watch } from 'vue';
    import axios from '@/services/axios';

    const props = defineProps({
        mode: { type: String, required: true },
        modelValue: [String],
        configs: Object,
    });

    const emit = defineEmits(['update:modelValue', 'update:configs']);
    const baseURL = axios.defaults.baseURL;

    const error = ref(null);
    const selectedTypes = ref([]);
    const oldLinks = ref([]);
    const selectedFileNames = ref([]);
    const truncateText = (text, max = 25) => {
        return text.length > max ? text.slice(0, max) + '...' : text;
    };

    watch(
        () => props.modelValue,
        (val) => {
            if (typeof val === 'string') {
                oldLinks.value = val
                    .split('#-#')
                    .map((link) => link.replace(/^https?:\/\/[^/]+/, ''))
                    .filter(Boolean);
            }
        },
        { immediate: true }
    );

    const configsLocal = computed({
        get: () => props.configs,
        set: (val) => emit('update:configs', val),
    });

    const fileTypeOptions = [
        { label: 'صور', value: 'images' },
        { label: 'PDF', value: 'pdf' },
        { label: 'فيديو', value: 'video' },
        { label: 'ملف مضغوط', value: 'zip' },
    ];

    const typeMap = {
        images: ['image/png', 'image/jpeg', 'image/jpg', 'image/webp', 'image/gif'],
        pdf: ['application/pdf'],
        video: ['video/mp4', 'video/webm', 'video/ogg'],
        zip: ['application/zip', 'application/x-zip-compressed'],
    };

    watch(
        () => props.configs?.fileTypes,
        (val) => {
            const typesFromProps = (val || '').split(',');
            selectedTypes.value = Object.entries(typeMap)
                .filter(([_, mimes]) => mimes.some((type) => typesFromProps.includes(type)))
                .map(([key]) => key);
        },
        { immediate: true }
    );

    watch(
        selectedTypes,
        () => {
            const types = selectedTypes.value.flatMap((type) => typeMap[type] || []);
            configsLocal.value.fileTypes = types.join(',');
        },
        { deep: true }
    );

    const acceptedTypes = computed(() => {
        return (props.mode === 'create' ? configsLocal.value : props.configs)?.fileTypes || '*/*';
    });

    const isImage = (link) => /\.(png|jpe?g|webp|gif)$/i.test(link);
    const getFileName = (link) => link.split('/').pop();

    const removeFile = (index) => {
        oldLinks.value.splice(index, 1);
        emit('update:modelValue', oldLinks.value.join('#-#'));
    };

    const handleFileChange = async (e) => {
        error.value = null;
        const uploadedFiles = Array.from(e.target.files);
        selectedFileNames.value = uploadedFiles.map((f) => f.name); // ← عرض أسماء الملفات

        const maxFiles = Number(configsLocal.value.maxFiles || 5); // عدد الملفات المسموح

        // ✅ التحقق من عدد الملفات
        if (oldLinks.value.length + uploadedFiles.length > maxFiles) {
            error.value = `الحد الأقصى لعدد الملفات هو ${maxFiles}`;
            return;
        }
        const formData = new FormData();
        uploadedFiles.forEach((file) => formData.append('files', file));

        try {
            const res = await axios.post('/api/admissions/upload/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            const newUrls = (res.data.urls || []).map((link) => link.replace(/^https?:\/\/[^/]+/, ''));
            oldLinks.value.push(...newUrls);
            emit('update:modelValue', oldLinks.value.join('#-#'));
        } catch (err) {
            error.value = 'فشل في رفع الملفات';
            console.error(err);
        }
    };
</script>

<style scoped>
    .input {
        padding: 6px 10px;
        border: 1px solid #ccc;
        border-radius: 6px;
        width: 100%;
    }
</style>

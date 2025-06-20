<template>
    <div class="space-y-8">
        <!-- بيانات النموذج الأساسية -->
        <FormMeta :form="form" />

        <!-- أقسام النموذج وتفاصيله -->
        <DynamicSections v-model:tabs="form.tabs" />

        <!-- زر الحفظ -->
        <SaveButton :formID="route.params.formId" :data="form" @save="saveForm" @edit="editForm" />
    </div>
</template>

<script setup>
    import { ref, onMounted, onBeforeMount, watch } from 'vue';
    import FormMeta from './comp/FormMeta.vue';
    import DynamicSections from './comp/DynamicSections.vue';
    import SaveButton from './comp/SaveButton.vue';
    import axios from '@/services/axios';
    import { useRoute, useRouter } from 'vue-router';

    const route = useRoute();
    const router = useRouter();
    const formId = ref(route.params.formId);
    const defaultForm = () => ({
        title: '',
        is_active: false,
        meta_data: { description: '', date_start: '', date_end: '', submissonsCount: 100000, userSubmitCount: 1,ignore_date:false },
        tabs: [],
    });

    const form = ref(defaultForm());

    const saveForm = async () => {
        try {
            const response = await axios.post('api/admissions/forms/', form.value);
            alert('تم حفظ النموذج بنجاح!');
            // console.log(response.data);
            router.push('/forms');
        } catch (error) {
            // console.error(error);
            alert('توجد مشكلة في حفظ النموذج!');
        }
    };

    watch(
        () => route.params.formId, // 🟡 راقب القيمة من route مباشرة
        async (id) => {
            if (id) {
                try {
                    const response = await axios.get(`api/admissions/forms/${id}/`);
                    form.value = response.data;
                    // console.log('✅ Loaded form:', form.value);
                    
                } catch (error) {
                    console.error('❌ Error loading form:', error);
                    // alert('فشل تحميل النموذج');
                }
            } else {
                form.value = defaultForm();
                console.log('🆕 No formId, using default values');
            }
        },
        { immediate: true }
    );
    const editForm = async () => {
        try {
            const response = await axios.put(`api/admissions/forms/${route.params.formId}/`, form.value);
            alert('تم حفظ النموذج بنجاح!');
            router.push(`/forms/`);
            // console.log(response.data);
        } catch (error) {
            console.error(error);
            alert('توجد مشكلة في حفظ النموذج!');        }
    };
</script>

<style scoped></style>

import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from '@/services/axios'; // استيراد axios الجاهز

export const useMenuStore = defineStore('menu', () => {
    const menuTree = ref<any[]>([]);

    const loadMenu = async () => {
        try {
            // const { data } = await axios.get('/api/menu'); // ← عدّل الرابط حسب API فعلي
            const { data } = await axios.get('/media/menu.json');
            menuTree.value = data;
            console.log(data)
        } catch (error) {
            console.error('فشل تحميل القائمة:', error);
        }
    };

    return { menuTree, loadMenu };
});

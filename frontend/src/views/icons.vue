<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Icon Gallery</h1>

    <!-- 🔍 حقل البحث -->
    <input
      v-model="search"
      type="text"
      placeholder="ابحث باسم الأيقونة"
      class="mb-6 px-4 py-2 border border-gray-300 rounded w-full"
    />

    <div class="grid grid-cols-4 gap-6">
      <div
        v-for="(component, name) in filteredIcons"
        :key="name"
        class="flex flex-col items-center text-center text-sm text-gray-600"
      >
        <component :is="component" class="w-8 h-8 text-primary mb-2" />
        <span>{{ extractName(name) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// 🧠 البحث
const search = ref('');

// 🧩 تحميل الأيقونات تلقائيًا
const modules = import.meta.glob('@/components/icon/**/*.vue', { eager: true });

const icons: Record<string, any> = {};
for (const path in modules) {
  icons[path] = (modules[path] as any).default;
}

// ✅ استخلاص الاسم فقط من المسار
const extractName = (path: string) => {
  return path.split('/').pop()?.replace('.vue', '') || '';
};

// ✅ تصفية حسب البحث
const filteredIcons = computed(() => {
  if (!search.value) return icons;

  const result: Record<string, any> = {};
  for (const path in icons) {
    if (extractName(path).toLowerCase().includes(search.value.toLowerCase())) {
      result[path] = icons[path];
    }
  }
  return result;
});
</script>

<style scoped>
/* optional styling */
</style>

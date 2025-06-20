<template>
    <div class="p-6 space-y-6">
        <h2 class="text-2xl font-bold">الكليات والبرامج</h2>
        <form @submit.prevent="createFaculty" class="flex gap-2">
            <input v-model="newFacultyName" class="form-input flex-1" placeholder="اسم الكلية" />
            <button type="submit" class="btn btn-primary">إضافة كلية</button>
        </form>

        <div v-for="faculty in faculties" :key="faculty.id" class="border rounded p-4 space-y-2">
            <div class="flex justify-between items-center">
                <div v-if="!faculty.editing" class="font-semibold">{{ faculty.name }}</div>
                <input v-else v-model="faculty.editName" class="form-input flex-1" />
                <div class="flex gap-1">
                    <button v-if="!faculty.editing" class="btn btn-sm" @click="startFacultyEdit(faculty)">  <Edit class="w-4 h-4" />
                    </button>
                    <button v-if="faculty.editing" class="btn btn-sm btn-primary"
                        @click="updateFaculty(faculty)">  <Save class="w-4 h-4" />
                    </button>
                    <button v-if="faculty.editing" class="btn btn-sm" @click="cancelFacultyEdit(faculty)"><X class="w-4 h-4" /></button>
                    <button class="btn btn-sm text-red-500" @click="deleteFaculty(faculty.id)"><Trash2 class="w-4 h-4" /></button>
                </div>
            </div>
            <ul class="space-y-1">
                <li v-for="prog in faculty.programs" :key="prog.id" class="flex justify-between items-center">
                    <div v-if="!prog.editing">{{ prog.sis_code }} - {{ prog.name }}</div>
                    <div v-else class="flex gap-2 w-full">
                        <input v-model="prog.editSisCode" class="form-input flex-1" placeholder="SIS Code" />
                        <input v-model="prog.editName" class="form-input flex-1" placeholder="اسم البرنامج" />
                    </div>
                    <div class="flex gap-1">
                        <button v-if="!prog.editing" class="" @click="startProgramEdit(prog)">  <Edit class="w-4 h-4" />
                        </button>
                        <button v-if="prog.editing" class=""
                            @click="updateProgram(faculty, prog)">  <Save class="w-4 h-4" />
                        </button>
                        <button v-if="prog.editing" class="" @click="cancelProgramEdit(prog)"><X class="w-4 h-4" /></button>
                        <button class="text-red-500" @click="deleteProgram(prog.id)"><Trash2 class="w-4 h-4" /></button>
                    </div>
                </li>
            </ul>
            <form @submit.prevent="createProgram(faculty)" class="flex gap-2">
                <input v-model="faculty.newProgram_code" class="form-input flex-1" placeholder="SIS Code" />
                <input v-model="faculty.newProgram" class="form-input flex-1" placeholder="اسم البرنامج" />
                <button type="submit" class="btn btn-secondary">إضافة برنامج</button>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/services/axios';

const faculties = ref([]);
const newFacultyName = ref('');
const fetchFaculties = async () => {
    const resFac = await axios.get('/api/users/faculties/');
    const resProg = await axios.get('/api/users/programs/');
    const facs = resFac.data.results || resFac.data;
    const progs = resProg.data.results || resProg.data;

    let facultyList = facs.map(f => {
        const programs = progs
            .filter(p => p.faculty === f.id || p.faculty?.id === f.id)
            .map(p => ({
                ...p,
                editName: p.name,
                editSisCode: p.sis_code || '',
                editing: false,
            }));

        return {
            ...f,
            editName: f.name,
            editing: false,
            newProgram: '',
            newProgram_code: '',
            programs,
            // أضف أول sis_code (أو أصغر)
            firstSisCode: programs.length > 0
                ? programs.map(p => p.sis_code || '').sort()[0]
                : '', // لو مفيش برامج
        };
    });

    // ✳️ الترتيب حسب sis_code
    facultyList.sort((a, b) => {
        if (!a.firstSisCode) return 1;
        if (!b.firstSisCode) return -1;
        return a.firstSisCode.localeCompare(b.firstSisCode);
    });

    faculties.value = facultyList;
};

const createFaculty = async () => {
    if (!newFacultyName.value) return;
    await axios.post('/api/users/faculties/', { name: newFacultyName.value });
    newFacultyName.value = '';
    fetchFaculties();
};

const createProgram = async (faculty) => {
    if (!faculty.newProgram) return;
    await axios.post('/api/users/programs/', { name: faculty.newProgram,sis_code: faculty.newProgram_code, faculty: faculty.id });
    faculty.newProgram = '';
    faculty.newProgram_code = '';
    fetchFaculties();
};

const startFacultyEdit = (faculty) => {
    faculty.editName = faculty.name;
    faculty.editing = true;
};

const cancelFacultyEdit = (faculty) => {
    faculty.editing = false;
};

const updateFaculty = async (faculty) => {
    await axios.patch(`/api/users/faculties/${faculty.id}/`, { name: faculty.editName });
    faculty.editing = false;
    fetchFaculties();
};

const deleteFaculty = async (id) => {
    await axios.delete(`/api/users/faculties/${id}/`);
    fetchFaculties();
};

const startProgramEdit = (program) => {
    program.editName = program.name;
    program.editing = true;
};

const cancelProgramEdit = (program) => {
    program.editing = false;
};

const updateProgram = async (faculty, program) => {
    await axios.patch(`/api/users/programs/${program.id}/`, { name: program.editName, sis_code: program.editSisCode, faculty: faculty.id });
    program.editing = false;
    fetchFaculties();
};

const deleteProgram = async (id) => {
    await axios.delete(`/api/users/programs/${id}/`);
    fetchFaculties();
};

onMounted(fetchFaculties);
</script>
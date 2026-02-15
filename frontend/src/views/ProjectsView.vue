<template>
  <div class="space-y-6 animate-fade-in-up">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">项目管理</h1>
        <p class="text-gray-500 mt-1">组织和管理你的项目</p>
      </div>
      <BaseButton @click="showCreateModal = true">
        <Plus class="w-4 h-4" />
        新建项目
      </BaseButton>
    </div>
    
    <!-- Projects Grid -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="w-8 h-8 text-primary-500 animate-spin" />
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProjectCard
        v-for="project in projects"
        :key="project.id"
        :project="project"
        @edit="editProject"
        @delete="deleteProject"
      />
      
      <!-- Empty State -->
      <div v-if="projects.length === 0" class="col-span-full text-center py-12 text-gray-500">
        <FolderKanban class="w-12 h-12 mx-auto mb-3 text-gray-300" />
        <p>暂无项目</p>
        <p class="text-sm mt-1">点击右上角按钮创建第一个项目</p>
      </div>
    </div>
    
    <!-- Create/Edit Modal -->
    <ProjectModal
      v-model="showCreateModal"
      :project="editingProject"
      @save="saveProject"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useProjectStore } from '@/stores/projectStore'
import { Plus, FolderKanban, Loader2 } from 'lucide-vue-next'
import BaseButton from '@/components/common/BaseButton.vue'
import ProjectCard from '@/components/projects/ProjectCard.vue'
import ProjectModal from '@/components/projects/ProjectModal.vue'
import type { Project, ProjectCreate } from '@/types'

const projectStore = useProjectStore()

// State
const showCreateModal = ref(false)
const editingProject = ref<Project | null>(null)

// Computed
const loading = computed(() => projectStore.loading)
const projects = computed(() => projectStore.activeProjects)

// Methods
onMounted(() => {
  projectStore.fetchProjects()
})

const editProject = (project: Project) => {
  editingProject.value = project
  showCreateModal.value = true
}

const deleteProject = async (id: number) => {
  if (confirm('确定要删除这个项目吗？')) {
    await projectStore.deleteProject(id)
  }
}

const saveProject = async (data: ProjectCreate) => {
  if (editingProject.value) {
    await projectStore.updateProject(editingProject.value.id, data)
  } else {
    await projectStore.createProject(data)
  }
  showCreateModal.value = false
  editingProject.value = null
}
</script>

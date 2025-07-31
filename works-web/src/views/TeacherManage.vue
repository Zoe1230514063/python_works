<template>
  <div class="layout">
    <TeacherNav current="manage" />
    <main class="main">
      <h2>作业详情</h2>

      <el-card shadow="always">
        <el-table :data="assignments" stripe style="width: 100%">
          <el-table-column prop="assignment_id" label="作业ID" width="120" />
          <el-table-column prop="assignment_title" label="作业标题" />
          <el-table-column prop="description" label="作业内容" show-overflow-tooltip />
          <el-table-column prop="publish_time" label="发布时间" width="160" />
          <el-table-column prop="class_name" label="班级" />
          <el-table-column label="操作" width="100">
            <template #default="scope">
              <el-button size="small" type="primary" @click="goDetail(scope.row)">
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/api/request'
import TeacherNav from '@/components/TeacherNav.vue'

const router = useRouter()
const assignments = ref([])

const load = async () => {
  const { data } = await axios.get('/api/assignments/my/', {
    params: { tno: JSON.parse(localStorage.getItem('user') || {}).tno }
  })
  assignments.value = data
}

const goDetail = (row) => {
  router.push(`/teacher/manage/${row.assignment_id}`)
}

onMounted(load)
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}
.main {
  flex: 1;
  padding: 40px;
}
</style>

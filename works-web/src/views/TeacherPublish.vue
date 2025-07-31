<template>
  <div class="layout">
    <TeacherNav current="publish" />
    <main class="main">
      <h2>发布作业</h2>

      <!-- 发布表单 -->
      <el-card style="margin-bottom: 24px">
        <el-form :model="form" label-width="100" @submit.prevent="publish">
          <el-form-item label="作业ID" required>
            <el-input v-model="form.assignment_id" placeholder="请输入作业ID" />
          </el-form-item>
          <el-form-item label="作业标题" required>
            <el-input v-model="form.title" />
          </el-form-item>
          <el-form-item label="作业内容" required>
            <el-input v-model="form.description" type="textarea" :rows="4" />
          </el-form-item>
          <el-form-item label="班级ID" required>
            <el-input v-model="form.class_id" placeholder="请输入班级ID" />
          </el-form-item>
          <el-button type="primary" native-type="submit">发布</el-button>
        </el-form>
      </el-card>

      <!-- 已发布作业列表 -->
      <h3>已发布作业</h3>
      <el-card>
        <el-table :data="assignments" stripe>
          <el-table-column prop="assignment_id" label="作业ID" width="100" />
          <el-table-column prop="assignment_title" label="作业标题" />
          <el-table-column prop="description" label="作业内容" show-overflow-tooltip />
          <el-table-column prop="publish_time" label="发布时间" width="160" />
          <el-table-column prop="class_name" label="班级" />
          <el-table-column label="操作" width="80">
            <template #default="scope">
              <el-popconfirm
                title="确定删除该作业？"
                @confirm="del(scope.row.assignment_id)"
              >
                <template #reference>
                  <el-button type="danger" link>删除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
        <el-empty v-if="!assignments.length" description="暂无作业" />
      </el-card>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from '@/api/request'
import TeacherNav from '@/components/TeacherNav.vue'
import { ElMessage } from 'element-plus'

const teacher = JSON.parse(localStorage.getItem('user') || '{}')
const assignments = ref([])

const form = reactive({
  assignment_id: '',
  title: '',
  description: '',
  class_id: ''
})

const load = async () => {
  const { data } = await axios.get('/api/assignments/my/', {
    params: { tno: teacher.tno }
  })
  assignments.value = data
}

const publish = async () => {
  if (!form.assignment_id || !form.title || !form.description || !form.class_id) {
    ElMessage.warning('请完整填写')
    return
  }
  try {
    await axios.post('/api/assignments/publish/', { ...form, tno: teacher.tno })
    ElMessage.success('发布成功')
    Object.assign(form, { assignment_id: '', title: '', description: '', class_id: '' })
    load()
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '发布失败')
  }
}

const del = async (id) => {
  try {
    await axios.delete(`/api/assignments/${id}/delete/`)
    ElMessage.success('已删除')
    load()
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '删除失败')
  }
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

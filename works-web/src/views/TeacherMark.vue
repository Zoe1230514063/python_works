<template>
  <div class="layout">
    <TeacherNav current="mark" />
    <main class="main">
      <h2>批改作业</h2>

      <el-card>
        <el-table :data="submissions" stripe style="width: 100%">
          <el-table-column prop="assignments_title" label="作业标题" />
          <el-table-column prop="sname" label="学生姓名" />
          <el-table-column prop="answer" label="答案" show-overflow-tooltip />
          <el-table-column prop="submit_time" label="提交时间" />
          <el-table-column label="状态" width="100">
            <template #default="scope">
              <el-tag v-if="scope.row.score !== null" type="success">已批改</el-tag>
              <el-tag v-else type="info">未批改</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="分数" width="80">
            <template #default="scope">
              <span v-if="scope.row.score !== null">{{ scope.row.score }}</span>
              <span v-else style="color:#909399">—</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="scope">
              <el-button size="small" type="primary" @click="openMarkModal(scope.row)">
                {{ scope.row.score !== null ? '修改' : '批改' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 弹窗批改 -->
      <el-dialog
        v-model="showModal"
        title="作业批改"
        width="700"
        :style="{ minHeight: '600px' }"
      >
        <el-form label-width="100">
          <el-form-item label="作业标题">
            <el-input :value="current.assignments_title" disabled />
          </el-form-item>
          <el-form-item label="学生姓名">
            <el-input :value="current.sname" disabled />
          </el-form-item>
          <el-form-item label="答案">
            <el-input
              :value="current.answer"
              type="textarea"
              :rows="8"
              disabled
              style="resize: none"
            />
          </el-form-item>
          <el-form-item label="分数/评语" required>
            <el-input
              v-model="score"
              placeholder="请输入分数或评语，如：优秀、89.5"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showModal = false">取消</el-button>
          <el-button type="primary" @click="saveScore">确认</el-button>
        </template>
      </el-dialog>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/api/request'
import TeacherNav from '@/components/TeacherNav.vue'
import { ElMessage } from 'element-plus'

const submissions = ref([])
const showModal = ref(false)
const current = ref({})
const score = ref('')

const load = async () => {
  const teacher = JSON.parse(localStorage.getItem('user') || '{}')
  const { data } = await axios.get('/api/submissions/to-mark/', {
    params: { tno: teacher.tno }
  })
  submissions.value = data
}

const openMarkModal = (row) => {
  current.value = row
  score.value = row.score ?? ''
  showModal.value = true
}

const saveScore = async () => {
  const sid = String(current.value.submissions_id).trim()
  if (!score.value.trim()) {
    ElMessage.warning('请输入分数或评语')
    return
  }
  try {
    await axios.put(`/api/submissions/${encodeURIComponent(sid)}/score/`, {
      score: score.value.trim()
    })
    ElMessage.success('已保存')
    showModal.value = false
    load()
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '保存失败')
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

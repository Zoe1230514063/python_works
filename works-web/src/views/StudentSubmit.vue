<template>
  <div class="layout">
    <StudentNav current="submit" />
    <main class="main">
      <h2>作业列表</h2>

      <el-card shadow="always" style="border-radius: 8px; overflow: hidden; margin-top: 16px;" >
        <el-table :data="assignments" stripe style="width: 100%">
          <el-table-column prop="assignments_title" label="作业标题" width="160" />
          <el-table-column prop="description" label="作业内容" width="280" show-overflow-tooltip />
          <el-table-column prop="publish_time" label="发布时间" width="180" />
          <el-table-column prop="teacher" label="发布老师" width="140" />

          <el-table-column label="状态" width="160">
            <template #default="scope">
              <div style="display: flex; align-items: center; gap: 4px;">
                <el-tag v-if="scope.row.submitted === 1" type="success">已提交</el-tag>
                <el-tag v-else type="info">未提交</el-tag>
                <span
                  v-if="scope.row.score && scope.row.score.trim()"
                  style="color:#409eff;font-weight:bold;white-space:nowrap"
                >
                  {{ scope.row.score.trim() }}
                </span>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="110">
            <template #default="scope">
              <!-- 未提交，可提交 -->
              <el-button
                v-if="scope.row.submitted === 0"
                type="primary"
                size="small"
                @click="openModal(scope.row, false)"
              >
                提交
              </el-button>
              <!-- 已提交且已批改，不可修改 -->
              <el-button
                v-else-if="scope.row.score !== null"
                type="info"
                size="small"
                disabled
              >
                不可修改
              </el-button>
              <!-- 已提交但未批改，可修改 -->
              <el-button
                v-else
                type="warning"
                size="small"
                @click="openModal(scope.row, true)"
              >
                修改
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 弹窗 -->
      <el-dialog
        v-model="showModal"
        :title="isEdit ? '修改答案' : '提交作业'"
        width="500"
      >
        <el-form>
          <el-form-item label="作业标题">
            <el-input v-model="current.assignments_title" disabled />
          </el-form-item>
          <el-form-item label="作业内容">
            <el-input v-model="current.description" type="textarea" disabled />
          </el-form-item>
          <el-form-item label="我的答案" required>
            <el-input
              v-model="answer"
              type="textarea"
              :rows="5"
              placeholder="请输入答案"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showModal = false">取消</el-button>
          <el-button type="primary" @click="submitAnswer">{{ isEdit ? '更新' : '提交' }}</el-button>
        </template>
      </el-dialog>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/api/request'
import StudentNav from '@/components/StudentNav.vue'
import { ElMessage } from 'element-plus'

const user = JSON.parse(localStorage.getItem('user') || {})
const assignments = ref([])
const showModal = ref(false)
const current = ref({})
const answer = ref('')
const isEdit = ref(false)

const loadAssignments = async () => {
  const { data } = await axios.get('/api/assignments/', {
    params: { sno: user.sno.trim() }
  })
  assignments.value = data
}

const openModal = (row, edit = false) => {
  current.value = row
  isEdit.value = edit
  answer.value = ''
  showModal.value = true
}

const submitAnswer = async () => {
  if (!answer.value.trim()) {
    ElMessage.warning('请输入答案')
    return
  }
  try {
    await axios.post('/api/submissions/submit/', {
      assignments_id: current.value.assignments_id,
      sno: user.sno,
      answer: answer.value
    })
    ElMessage.success(isEdit.value ? '修改成功' : '提交成功')
    showModal.value = false
    loadAssignments()
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '提交失败')
  }
}

onMounted(loadAssignments)
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}
.main {
  flex: 1;
  padding: 20px;
}
</style>

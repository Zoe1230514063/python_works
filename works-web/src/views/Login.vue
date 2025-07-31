<template>
  <el-card style="width:400px;margin:100px auto;text-align:center">
    <h2>作业管理系统登录</h2>

    <el-form @submit.prevent="login">
      <!-- 身份 -->
      <el-form-item label="身份">
        <el-radio-group v-model="form.role">
          <el-radio value="student">学生</el-radio>
          <el-radio value="teacher">教师</el-radio>
        </el-radio-group>
      </el-form-item>

      <!-- 账号 -->
      <el-form-item label="账号">
        <el-input v-model="form.uid" placeholder="学号/工号" />
      </el-form-item>

      <!-- 姓名 -->
      <el-form-item label="姓名">
        <el-input v-model="form.name" placeholder="真实姓名" />
      </el-form-item>

      <!-- 登录按钮 -->
      <el-button type="primary" native-type="submit" :loading="loading">
        {{ loading ? '登录中…' : '登录' }}
      </el-button>
    </el-form>
  </el-card>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from '@/api/request'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const form = reactive({
  role: 'student',
  uid: '',
  name: ''
})

const loading = ref(false)
const router = useRouter()

// 防抖 + 登录
const login = () => {
  // 防止空格触发
  if (!form.uid.trim() || !form.name.trim()) {
    ElMessage.warning('请完整填写')
    return
  }

  if (loading.value) return // 防抖：防止连点
  loading.value = true

  axios.post('/api/login/', {
    role: form.role,
    uid: Number(form.uid.trim()),
    name: form.name.trim()
  })
  .then(({ data }) => {
    if (data.error) {
      ElMessage.error(data.error)
    } else {
      localStorage.setItem('user', JSON.stringify(data.data))
      localStorage.setItem('role', form.role)
      router.push(`/${form.role}/home`)
    }
  })
  .catch(() => {
    ElMessage.error('网络异常')
  })
  .finally(() => {
    loading.value = false
  })
}
</script>

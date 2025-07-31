<template>
  <aside class="sidebar">
    <div class="head">
      <div class="title">学生 作业管理系统</div>
      <div class="info">
        学号信息：{{ user.sno }}
        <el-button
          link
          type="primary"
          class="logout-btn"
          @click="logout"
        >
          退出
        </el-button>
      </div>
    </div>

    <!-- 一级导航 -->
    <ul class="nav">
      <li
        :class="{ active: current === 'home' }"
        @click="$router.push('/student/home')"
      >
        个人中心
      </li>
      <li
        :class="{ active: current === 'submit' }"
        @click="$router.push('/student/submit')"
      >
        作业提交
      </li>
    </ul>
  </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  current: {
    type: String,
    required: true
  }
})

const router = useRouter()
const user = JSON.parse(localStorage.getItem('user') || {})
const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: #f5f7fa;
  height: 100vh;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}
.head {
  padding: 20px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}
.title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 16px;
}
.info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 15px;
  color: #606266;
}
.logout-btn {
  margin-left: auto;
  margin-right: 1px;
}
.nav {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
}
.nav li {
  font-weight: bold;
  padding: 16px 20px;
  cursor: pointer;
  transition: background 0.2s;
}
.nav li:hover {
  background: #e6f1ff;
}
.nav li.active {
  background: #409eff;
  color: #fff;
}
</style>

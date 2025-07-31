<template>
  <div class="layout">
    <StudentNav current="home" />
    <main class="main">

      <div class="info-text">
        <p class="welcome">
          学&nbsp;生&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {{ user.sname }} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;欢&nbsp;迎&nbsp;您&nbsp;!
        </p>
        <p>班&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;级：{{ user.class_name || '暂无' }}</p>
        <p>学&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;号：{{ user.sno }}</p>
        <p>联&nbsp;系&nbsp;方&nbsp;式&nbsp;：{{ user.scontact || '暂无' }}</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import StudentNav from '@/components/StudentNav.vue'
const user = JSON.parse(localStorage.getItem('user') || {})
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}
.main {
  flex: 1;
  padding: 40px 60px;
}
h2 {
  margin: 0 0 16px 0;
  font-size: 24px;
}
.info-text .welcome {
  font-weight: bold;
  font-size: 24px;
  margin-bottom: 48px;
}
.info-text p {
  font-size: 18px;
  line-height: 30px;
}
</style>

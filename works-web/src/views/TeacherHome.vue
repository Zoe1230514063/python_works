<template>
  <div class="layout">
    <TeacherNav current="home" />
    <main class="main">

      <div class="info-text">
        <p class="welcome">
          教&nbsp;师&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {{ user.tname }} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;欢&nbsp;迎&nbsp;您&nbsp;!
        </p>
        <p>工&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;号：{{ user.tno }}</p>
        <p>联&nbsp;系&nbsp;方&nbsp;式&nbsp;：{{ user.tcontact || '暂无' }}</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import TeacherNav from '@/components/TeacherNav.vue'
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

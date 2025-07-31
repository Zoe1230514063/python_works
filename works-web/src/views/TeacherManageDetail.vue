<template>
  <div class="layout">
    <TeacherNav current="manage" />
    <main class="main">
      <h2>作业详情 > {{ assignment_title }}</h2>

      <!-- 表格区域 -->
      <el-card shadow="always" style="border-radius: 8px; overflow: hidden;">
        <el-table :data="students" stripe style="width: 100%">
          <el-table-column prop="sname" label="学生姓名" width="120" />
          <el-table-column label="答案" min-width="260">
            <template #default="scope">
              <span
                class="answer-link"
                @click="openAnswerModal(scope.row)"
              >
                {{ scope.row.answer || '该学生未提交' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="submit_time" label="提交时间" width="180" />
          <el-table-column label="分数" width="100">
            <template #default="scope">
              <span style="color:#409eff;font-weight:bold;">
                {{ scope.row.score || '—' }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 图表区域 -->
      <el-card style="margin-top: 24px;">
        <h3 style="margin-top: 0;">作业完成情况统计</h3>
        <div ref="chartRef" style="width: 100%; height: 160px;"></div>
      </el-card>

      <!-- 答案弹窗 -->
      <el-dialog
        v-model="showModal"
        title="完整答案"
        width="700"
        :style="{ minHeight: '400px' }"
      >
        <el-input
          :value="fullAnswer"
          type="textarea"
          :rows="10"
          readonly
          style="resize: none"
        />
        <template #footer>
          <el-button @click="showModal = false">关闭</el-button>
        </template>
      </el-dialog>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/api/request'
import TeacherNav from '@/components/TeacherNav.vue'
import * as echarts from 'echarts'

const route = useRoute()
const assignment_id = route.params.assignment_id
const assignment_title = ref('')
const students = ref([])
const showModal = ref(false)
const fullAnswer = ref('')
const chartRef = ref(null)

const load = async () => {
  const teacher = JSON.parse(localStorage.getItem('user') || {})
  const { data: asg } = await axios.get('/api/assignments/detail/', {
    params: { assignment_id: assignment_id }
  })
  assignment_title.value = asg.title

  const { data: list } = await axios.get('/api/assignments/student-list/', {
    params: {
      assignment_id: assignment_id,
      tno: teacher.tno
    }
  })
  students.value = list

  await nextTick()
  renderChart()
}

const renderChart = () => {
  const submitted = students.value.filter(s => s.answer && s.answer.trim() !== '').length
  const notSubmitted = students.value.length - submitted

  const chart = echarts.init(chartRef.value)
  chart.setOption({
    tooltip: {},
    grid: {
      left: 60,
      right: 20,
      top: 10,
      bottom: 20
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: ['已完成', '未完成']
    },
    series: [
      {
        type: 'bar',
        data: [submitted, notSubmitted],
        label: {
          show: true,
          position: 'right'
        },
        itemStyle: {
          color: function (params) {
            return params.dataIndex === 0 ? '#67C23A' : '#F56C6C'
          }
        }
      }
    ]
  })
}

const openAnswerModal = (row) => {
  fullAnswer.value = row.answer || '该学生未提交'
  showModal.value = true
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
.answer-link {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
  font-weight: 500;
}
</style>

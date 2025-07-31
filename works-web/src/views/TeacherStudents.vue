<template>
  <div class="layout">
    <TeacherNav current="students" />
    <main class="main">
      <h2>学生管理</h2>

      <el-card>
        <div style="margin-bottom: 12px; text-align: right">
          <el-button type="primary" @click="showAdd = true">新增</el-button>
        </div>

        <el-table :data="students" stripe style="width: 100%">
          <el-table-column prop="sno" label="学号" />
          <el-table-column prop="sname" label="姓名" />
          <el-table-column prop="ssex" label="性别" />
          <el-table-column prop="class_name" label="班级" />
          <el-table-column label="联系方式">
            <template #default="scope">{{ scope.row.scontact || '暂无' }}</template>
          </el-table-column>
          <el-table-column label="操作" width="80">
            <template #default="scope">
              <el-popconfirm
                title="确定删除该学生？"
                @confirm="remove(scope.row.sno)"
              >
                <template #reference>
                  <el-button type="danger" link>删除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>

        <el-empty v-if="!students.length" description="暂无学生数据" />
      </el-card>

      <!-- 新增学生弹窗 -->
      <el-dialog v-model="showAdd" title="新增学生" width="420">
        <el-form :model="addForm" label-width="80">
          <el-form-item label="学号" required>
            <el-input v-model="addForm.sno" placeholder="请输入学号" />
          </el-form-item>
          <el-form-item label="姓名" required>
            <el-input v-model="addForm.sname" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="性别" required>
            <el-select v-model="addForm.ssex" placeholder="请选择性别">
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>
          <el-form-item label="班级" required>
            <el-input v-model="addForm.class_id" placeholder="请输入班级id">
              <el-option
                v-for="c in classes"
                :key="c.class_id"
                :label="c.class_name"
                :value="c.class_id"
              />
            </el-input>
          </el-form-item>
          <el-form-item label="联系方式">
            <el-input v-model="addForm.scontact" placeholder="选填" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showAdd = false">取消</el-button>
          <el-button type="primary" @click="confirmAdd">确认</el-button>
        </template>
      </el-dialog>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from '@/api/request'
import TeacherNav from '@/components/TeacherNav.vue'
import { ElMessage } from 'element-plus'

const students = ref([])
const classes = ref([])
const teacher = JSON.parse(localStorage.getItem('user') || '{}')

const showAdd = ref(false)
const addForm = reactive({
  sno: '',
  sname: '',
  ssex: '',
  class_id: '',
  scontact: ''
})
onMounted(async () => {
  if (!teacher.tno) return
  const [sRes, cRes] = await Promise.all([
    axios.get('/api/students/', { params: { tno: teacher.tno } }),
    axios.get('/api/classes/')
  ])
  students.value = sRes.data
  classes.value = cRes.data
})

const confirmAdd = async () => {
  if (!addForm.sno || !addForm.sname || !addForm.ssex || !addForm.class_id) {
    ElMessage.warning('请完整填写必填项')
    return
  }
  try {
    await axios.post('/api/students/add/', addForm)
    ElMessage.success('新增成功')
    showAdd.value = false
    const { data } = await axios.get('/api/students/', { params: { tno: teacher.tno } })
    students.value = data
    Object.assign(addForm, { sno: '', sname: '', ssex: '', class_id: '', scontact: '' })
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '新增失败')
  }
}

const remove = async (rawSno) => {
  const sno = String(rawSno).trim() // 去除空格
  try {
    await axios.delete(`/api/students/${sno}/delete/`)
    ElMessage.success('已删除')
    students.value = students.value.filter(stu => String(stu.sno).trim() !== sno)
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '删除失败')
  }
}
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

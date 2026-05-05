<template>
  <div>
    <el-card>
      <h2>错题本</h2>

      <el-table :data="list">
        <el-table-column prop="question_content" label="题目"/>
        <el-table-column prop="knowledge_point" label="知识点"/>

        <el-table-column label="操作">
          <template #default="scope">
            <el-button @click="goPractice(scope.row)">
              重新练习
            </el-button>
          </template>
        </el-table-column>

      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { wrongApi } from '../api/wrong'

const router = useRouter()
const list = ref([])

onMounted(async () => {
  const res = await wrongApi.getWrongList("1")
  list.value = res.data.list
})

const goPractice = (row) => {
  router.push({
    path: '/exam',
    query: {
      mode: 'wrong'
    }
  })
}
</script>
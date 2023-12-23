<template>
  <el-row>
    <el-space wrap>
      <el-card class="home-box-card" v-for="item in moduleCount" :key="item.name">
        <template #header>
          <div class="card-header">
            <span>{{ item.name }}</span>
          </div>
        </template>
        <div class="big-num">{{ item.count }}</div>
      </el-card>
    </el-space>
  </el-row>
  <br>
  <el-row>
    <el-col :span="12">
      <el-card class="info-box-card">
        <template #header>
          <div class="card-header">
            <span>测试环境</span>
          </div>
        </template>
        <h4>主站点</h4>
        <ul>
          <li v-for="prim in primEnvList">
            <a :href=prim.url target="_blank">{{prim.url}}</a>
          </li>
        </ul>
        <h4>管理后台</h4>
        <ul>
          <li v-for="admin in adminEnvList">
            <a :href=admin.url target="_blank">{{admin.url}}</a>
            <el-button type="success" size='small' round @click="openNew(admin)">创建账号</el-button>
          </li>
        </ul>
      </el-card>
    </el-col>
    <el-col :span="12">
      <el-card class="info-box-card">
        <template #header>
          <div class="card-header">
            <span>工具文档</span>
          </div>
        </template>
        <ul>
          <li>
            <a href="https://www.baidu.com" target="_blank">常见问题汇总</a>
          </li>
          <li>
            <a href="https://www.weibo.com" target="_blank">新闻八卦</a>
          </li>
        </ul>
      </el-card>
    </el-col>
  </el-row>
</template>


<script setup>
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import { ref, onMounted } from 'vue'
import util from "@/libs/utils";

const chartLoading = ref(false)

let moduleCount = ref([{"name":"A", "count": 212}, {"name":"B", "count": 21212}, {"name":"C", "count": 9000}])
let primEnvList = util.primEnvList
let adminEnvList = util.adminEnvList

// onMounted(() => {  todo
//   chartLoading.value = true
//   axios.post("/home/count").then((resp) => {
//     moduleCount.value = resp.data.data;
//   })
// })
const accountCreate = (env, account, adminType) => {
  axios.get("/home/createBossAccount?adminType=" + adminType + "&env=" + env + "&account=" + account).then(resp => {
    if (resp.data === 0) {
      ElMessage({
        type: 'error',
        message: '账户已存在'
      })
    } else {
      ElMessage({
        type: 'success',
        message: '创建成功'
      })
    }

  })
}

const openNew = (env) => {
  ElMessageBox.prompt('请输入账号，密码默认Bg_123456', '账号创建', {
    confirmButtonText: 'OK',
    cancelButtonText: 'Cancel',
  }).then(({ value }) => {
    accountCreate(env, `${value}`, 'new')
  })
}
</script>

<style>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.home-box-card {
  width: 200px;
}

.big-num {
  color: green;
  font-size: 40px;
}

.info-box-card {
  width: 600px;
}
</style>
<template>
  <el-table :data="tableData" height="1200" v-loading="tableLoading">
    <el-table-column label="服务" prop="service"></el-table-column>
    <el-table-column label="环境" prop="env"></el-table-column>
    <el-table-column label="分支" prop="branch"></el-table-column>
    <el-table-column label="占用状态" prop="status">
      <template #default="scope">
        <el-tag :type="scope.row.status === '占用' ? 'danger' : 'success'">{{ scope.row.status }}</el-tag>
      </template>
    </el-table-column>
    <el-table-column label="执行状态" prop="progress">
      <template #default="scope">
        <el-tag :type="scope.row.progress !== 'SUCCESS' ? 'danger' : 'success'">{{ scope.row.progress }}</el-tag>
      </template>
    </el-table-column>
    <el-table-column label="构建者" prop="builder"></el-table-column>
    <el-table-column label="备注" prop="remark"></el-table-column>
    <el-table-column label="开始时间" prop="startTime"></el-table-column>
    <el-table-column align="right" width="200">
      <template #header>
        <el-space direction="vertical">
          <el-select v-model="env_search" size="small" filterable placeholder="环境选择" style="width: 100px;"
                     @change="handleEnvChange">
            <el-option v-for="env in primEnvList" :value="env.url">{{ env.name }}</el-option>
          </el-select>
          <el-input v-model="service_search" size="small" placeholder="服务搜索" style="width: 100px;"
                    @input="handleServiceChange" />
        </el-space>
      </template>
      <template #default="scope">
        <el-button size="small" type="primary" @click="handleBuild(scope.row)">占用</el-button>
        <el-button size="small" type="success" @click="handleRelease(scope.row)">释放</el-button>
        <el-button size="small" type="info" @click="handleHistory(scope.row)">历史</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-pagination background layout="prev, pager, next" :total="dataTotal" :page-size=40
                 @current-change="handelPageChange" />
  <el-dialog v-model="buildDialogShow" width="40%" :title="form.env + '-' + form.service">
    <el-form :model="form" v-loading="branchLoading">
      <el-form-item label="分支">
        <el-select v-model="form.branch" filterable size="large" style="width: 400px;">
          <el-option v-for="item in branchList" :value="item.name" :key="item.name">{{ item.name }}
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Tag">
        <el-select v-model="form.extra1" size="large" style="width:400px">
          <el-option v-for="item in extra1Option" :value="item" :key="item">{{ item }}</el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="JAVA_OPTS_PARAMS">
        <el-input v-model="form.extra2" size="large"></el-input>
      </el-form-item>
      <el-form-item label="备注">
        <el-input type="textarea" :row="4" v-model="remark"></el-input>
      </el-form-item>
      <el-form-item>
        <el-space>
          <el-button type="danger" @click="build" :loading="buildBtnLoading">开始构建</el-button>
          <el-button type="info" @click="openConsole()" :loading="logBtnLoading">控制台日志</el-button>
        </el-space>
      </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog v-model="buildHistoryShow" width="60%" title="构建历史">
    <el-table :data="buildHistoryData">
      <el-table-column label="服务" prop="service"></el-table-column>
      <el-table-column label="分支" prop="branch"></el-table-column>
      <el-table-column label="tag" prop="tag"></el-table-column>
      <el-table-column label="构建者" prop="builder"></el-table-column>
      <el-table-column label="构建时间" prop="updateTime"></el-table-column>
    </el-table>
  </el-dialog>
</template>

<script lang="ts" setup>
import util from '../../libs/utils';
import axios from 'axios';
import { ref, onMounted, computed, h } from 'vue'
import { ElNotification, ElMessage } from 'element-plus';
import {FALSE} from "sass";

interface Build {
  id: number,
  env: string,
  service: string,
  status: string,
  builder: string,
  larkName: string,
  folder: string,
  branch: string,
  remark: string,
  startTime: string,
  version: number,
  extra1: string,
  extra2: string,
  progress: string
}
interface Search {
  env: string,
  service: string,
  page: number
}
interface BuildHistory {
  id: number,
  service: string,
  branch: string,
  builder: string,
  updateTime: string,
  tag: string
}
const tableData = ref<Build[]>([])
const service_search = ref('')
const env_search = ref('')
const dataTotal = ref(0)
// const filterTableData = computed(() => tableData.value.filter(data => (!service_search.value ||
//     data.service.toLocaleLowerCase().includes(service_search.value.toLocaleLowerCase())) && (!env_search.value || data.env === env_search.value)))
const buildDialogShow = ref(false)
const buildHistoryShow = ref(false)
const form = ref<Build>({
  id: 0,
  env: 'test1',
  service: '',
  status: '',
  builder: '',
  larkName: '',
  folder: '',
  branch: '',
  remark: '',
  startTime: '',
  version: 0,
  extra1: '',
  extra2: '',
  progress: ''
})
const searchCondition = ref<Search>({
  env: '',
  service: '',
  page: 1
})
const branchList = ref([]) as any
let primEnvList = util.primEnvList
const remark = ref('')
const branchLoading = ref(false)
const buildBtnLoading = ref(false)
const logBtnLoading = ref(false)
const tableLoading = ref(false)
const extra1Option = ref([]) as any
const buildHistoryData = ref<BuildHistory[]>([])
let lastBuildNum = ''

onMounted(() => {
  // buildType = sessionStorage.getItem('buildType')
  // console.log(buildType)
  dataLoad()
})
const dataLoad = () => {
  tableLoading.value = false
  axios.post('/build/queryBuild', searchCondition.value).then(resp => {
    tableData.value = resp.data.data
    tableLoading.value = false
    dataTotal.value = parseInt(resp.data.message)
  })
}
const handleBuild = (row: Build) => {
  form.value = row
  axios.post('/build/getServiceName', form.value).then(resp => {
    extra1Option.value = resp.data
  })

  buildDialogShow.value = true
  branchLoading.value = true
  form.value.builder = util.getLoginName()
  remark.value = row.remark
  axios.post('/build/getBranch', form.value).then(resp => {
    branchLoading.value = false
    branchList.value = resp.data
  }).catch(error => {
    buildDialogShow.value = false
    ElMessage({
      type: 'error',
      message: '拉取分支失败,请确保Jenkins可访问并且EAA保持登录状态 ╮(￣▽￣)╭',
      duration: 10000
    })
  })
}
const handleHistory = (row: Build) => {
  buildHistoryShow.value = true
  axios.get(`/build/getBuildHistory?buildId=${row.id}`).then(resp => {
    buildHistoryData.value = resp.data.data
  })
}
const build = () => {
  form.value.status = '占用'
  form.value.progress = 'RUNNING'
  form.value.remark = remark.value
  buildBtnLoading.value = true
  logBtnLoading.value = true
  axios.post('/build/build', form.value).then(resp => {
    if (resp.data.code == '0000') {
      form.value.version = form.value.version + 1
      dataLoad()
      ElNotification({
        title: '触发构建',
        message: h('i', { style: 'color:teal' }, resp.data.message)
      })
    } else {
      ElNotification({
        title: '触发构建',
        message: h('i', { style: 'color:red' }, resp.data.message)
      })
    }
  })
  setTimeout(() => {
    logBtnLoading.value = false
    buildBtnLoading.value = false
    axios.post('/build/getLastBuildNum', form.value).then(resp => {
      lastBuildNum = resp.data
    })
  }, 10000)

}
const handleRelease = (row: Build) => {
  row.status = "可用"
  row.progress = ""
  axios.post('/build/release', row).then(resp => {
    ElNotification({
      title: '构建结果',
      message: h('i', { style: 'color:teal' }, resp.data.message)
    })
    dataLoad()
  })
}
const openConsole = () => {
  open('https://dev-test-jenkins02.sniper5.vip/job/' + form.value.folder + '/job/' + form.value.service + '/' + lastBuildNum + '/console', '_blank')
}
const handelPageChange = (val: number) => {
  console.log(`current page: ${val}`)
  searchCondition.value.page = val
  dataLoad()
}
const handleEnvChange = (val: string) => {
  console.log(`current env: ${val}`)
  searchCondition.value.env = val
  dataLoad()
}
const handleServiceChange = (val: string) => {
  console.log(`current service: ${val}`)
  searchCondition.value.service = val
  dataLoad()
}
</script>
<template>
  <el-card show="always" class="main-card">
    <el-form :model="form">
      <el-form-item>
        <el-radio-group v-model="form.kycFlag">
          <el-radio size="large" label="Real" border>个人认证</el-radio>
          <el-radio size="large" label="Enterprise" border>企业认证</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-select placeholder="选择环境" size="large" filterable v-model="form.env" style="width: 500px">
          <el-option v-for="item in primEnvList" :value="item.url">{{ item.name }}</el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-input v-model="form.account" size="large" placeholder="UID"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input v-model="form.userName" size="large" placeholder="名称"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input v-model="form.idCardNo" size="large" placeholder="证件号码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-select placeholder="国家地区" size="large" v-model="form.areaId" style="width: 500px">
          <el-option value="86">大陆</el-option>
          <el-option value="94">韩国</el-option>
          <el-option value="201">美国</el-option>
          <el-option value="88">牙买加</el-option>
          <el-option value="89">日本</el-option>
          <el-option value="26">巴西</el-option>
          <el-option value="76">香港</el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <span style="color:cornflowerblue;">* 姓名身份证同时为空则取消认证</span>
      </el-form-item>
      <el-form-item>
        <el-button class="btn-center" type="primary" size="large" @click="verify">实名认证</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>


<script setup>
import { ElMessage } from 'element-plus'
import utils from '../../libs/utils'
import { ref, onMounted } from 'vue'
import axios from 'axios';



let form = ref({
  env: "test9",
  dbType: "new",
  account: "",
  keyType: "uid",
  userName: "",
  idCardNo: "",
  areaId: "",
  kycFlag: "Real",
  // user:"ira"
})
let primEnvList = utils.primEnvList

const verify = () => {
  axios.post('/account/realNameSubmit', form.value).then(resp => {
    if (resp.data.code === '0000') {
      ElMessage({
        message: resp.data.message,
        type: 'success'
      })
    } else {
      ElMessage({
        message: resp.data.message,
        type: 'error'
      })
    }
  })
}
onMounted(() => {
  // axios.get('/build/queryEnvList').then(resp => {
  //     envList.value = resp.data
  // })
  // envList.value = util.env
})
</script>

<style></style>
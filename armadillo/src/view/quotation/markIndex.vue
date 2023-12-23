<template>
  <el-card show="always" class="main-card">
    <el-form :model="form">
      <el-radio-group v-model="type">
        <el-radio size="large" label="标记价格">标记价格</el-radio>
        <el-radio size="large" label="指数价格">指数价格</el-radio>
      </el-radio-group>
      <el-form-item>
        <el-select placeholder="选择环境" size="large" filterable v-model="form.env" style="width: 450px">
          <el-option v-for="item in primEnvList" :value="item.url">{{ item.name }}</el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select v-model="selectedItem" size="large" style="width: 450px;" filterable allow-create
                   placeholder="选择交易对" @click="symbols" @change="handleSelect">
          <el-option v-for="item in symbolList" :key="item.symbolCode" :value="item.symbolCode">
            {{ item.symbolCode }}</el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-input v-model="form.price" size="large" placeholder="价格" style="width: 450px;"></el-input>
      </el-form-item>
      <el-form-item label="铺单">
        <el-switch v-model="form.isOrder" size="large" placeholder="铺单" style="width: 450px;" active-value="1"
                   inactive-value="0" @change="changevalue"></el-switch>
      </el-form-item>
      <el-form-item v-show="form.inputValue">
        <el-input v-model="form.inputNumber" size="large" placeholder="铺单数量(选填)" style="width: 450px;"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button class="btn-center" type="danger" size="large" @click="price">调整价格</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>
<script setup>
import { ElMessage } from 'element-plus'
import utils from '../../libs/utils'
import { ref, onMounted } from 'vue'
import axios from 'axios';

const type = ref('标记价格')

let form = ref({
  env: "test",
  symbol: "",
  price: "",
  isOrder: "0",
  symbolId: "",
  baseSymbol: "",
  pricedSymbol: "",
  inputValue: false,
  inputNumber: "",
})
let envList = utils.primEnvList
const price = () => {
  let path = ''
  if (type.value === '标记价格') {
    path = '/changeMarkPrice'
  } else if (type.value === '指数价格') {
    path = '/updateIndexPrice'
  }
  axios.post(`/contract${path}`, form.value).then(resp => {
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


let symbolList = ref([])

const symbols = async () => {
  try {
    const resp = await axios.post('/contract/getSymbol', form.value);
    if (resp.data.code === '0000') {
      symbolList.value = resp.data.data;
      console.log(symbolList.value);
    } else {
      ElMessage({
        message: "该环境未配置币对，请确认环境可用" ,
        type: 'error'
      });
    }
  } catch (error) {
    console.error(error);
  }
}
const selectedItem = ref(null);


const handleSelect = (val) => {
  console.log("%--%"+val)
  let tmplist = [...symbolList.value]

  let selectObj = tmplist.find((item) => {
    console.log("---" + item.symbolCode)

    return item.symbolCode === val

  })
  if (!selectObj) {
    // 如果没有匹配项，将新选项添加到列表中
    selectObj = { symbolCode: val };
    symbolList.value.push(selectObj);
  }
  console.log("-"+symbolList.value)
  form.value.symbol = selectObj.symbolCode;
  form.value.symbolId = selectObj.symbolId;
  form.value.baseSymbol = selectObj.baseSymbol;
  form.value.pricedSymbol = selectObj.pricedSymbol;

  console.log("++symbolId值:" + form.value.symbolId)
  selectedItem.value = selectObj.symbolCode;


};

const changevalue=() => {
  if (form.value.isOrder === '1') {
    form.value.inputValue = true
  }else{
    form.value.inputValue = false
  }
}


onMounted(() => {
  // axios.get('/build/queryEnvList').then(resp => {
  //     envList.value = resp.data
  // })
  // envList.value = util.env
  symbols();
})




</script>


<style></style>
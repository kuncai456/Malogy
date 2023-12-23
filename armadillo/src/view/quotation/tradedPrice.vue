<template>
  <el-card show="always" class="main-card" style="width:620px;top: 10%">
    <template #header>
      <span>修改现货最新成交价</span>
    </template>
    <el-form :model="form">
      <el-row>
        <el-form-item label="测试环境">
          <el-select placeholder="选择环境" size="large" filterable v-model="form.env" style="width: 200px"
                     @change="updateSymbolList">
            <el-option v-for="item in primEnvList" :value="item.url">{{ item.name }}</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="交易币对" required style="margin-left: 20px">
          <el-select v-model="selectedItem" size="large" style="width: 200px;" filterable allow-create
                     placeholder="选择交易对" @change="getSymbolSelectValue">
            <el-option v-for="item in symbolList" :key="item.symbolCode" :value="item.symbolCode">{{ item.symbolCode
              }}</el-option>
          </el-select>
        </el-form-item>
      </el-row>

      <el-row>
        <el-form-item label="当前价格">
          <el-input v-model="form.lastPrice" too size="large" placeholder="最新成交价 (双击可刷新)" @dblclick="getLastPrice" style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="目标价格" required style="margin-left: 20px">
          <el-input v-model="form.price" size="large" placeholder="请输入价格" style="width: 100px;"
                    @change="updatePriceRatio(1)"></el-input>
        </el-form-item>
        <el-form-item  style="margin-left: 5px">
          <el-input v-model="form.ratio" size="large" placeholder="涨幅" style="width: 90px;"
                    @change="updatePriceRatio(2)"></el-input>%
        </el-form-item>
      </el-row>
      <el-row>
        <el-form-item label="下单用户">
          <el-input v-model="form.uid" size="large" placeholder="uid(选填)" style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="铺单" style="margin-left: 20px;">
          <el-switch v-model="form.isOrder" size="large" placeholder="" style="width: 50px;" active-value="1"
                     inactive-value="0"></el-switch>
        </el-form-item>
        <el-form-item label="同步指数价格" style="margin-left: 20px;">
          <el-switch v-model="form.isIndexPrice" size="large" placeholder="" style="width: 50px;" active-value="1"
                     inactive-value="0"></el-switch>
        </el-form-item>
      </el-row>
      <el-form-item>
        <el-button class="btn-center" type="danger" size="large" @click="submit" :loading="isLoading">提 交</el-button>
      </el-form-item>
    </el-form>
    <span style="color: gray">
      1. 通过循环下单的方式，将最新成交价格推到目标价格；<br>
      2. 输入"下单用户"则使用该用户下单，不输入则使用默认账户；<br>
      3. 当输入的uid用户资产不足时会<font style="color: red">自动进行充值</font>；<br>
      4. 启动"结束后自动铺单"时，达到目标价格后进行铺单(铺单使用的是量化账户).
    </span>
  </el-card>
</template>
<script setup>
import { ElMessage } from 'element-plus'
import utils from '../../libs/utils'
import { ref, onMounted } from 'vue'
import axios from 'axios';

let form = ref({
  env: "test",
  symbol: "",
  baseCoin: "",
  quoteCoin: "",
  lastPrice: "",
  price: "",
  ratio: "",
  isOrder: "1",
  isIndexPrice: "1",
  uid: "",
  // user: util.getLoginName()
  user: ""
})
let isLoading = ref(false)
let primEnvList = utils.primEnvList
const submit = () => {
  if(form.value.symbol == "" || form.value.price == ""){
    ElMessage({
      message: "必填项不能为空！",
      type: 'error'
    })
    return
  }
  isLoading.value = true
  axios.post('/spot/changeLastPrice', form.value).then(resp => {
    if (resp.data.code === '0000') {
      isLoading.value = false
      ElMessage({
        message: resp.data.message,
        type: 'success'
      })
    } else {
      ElMessage({
        message: resp.data.message,
        type: 'error'
      })
      isLoading.value = false
    }
  })
  // 记录点击事件
  reqRecord();
}

const getLastPrice = async () => {
  if (form.value.symbol == ""){
    return
  }
  try {
    const resp = await axios.get('/spot/getLastPrice?env=' + form.value.env + '&symbol=' + form.value.symbol);
    if (resp.data.code === '0000') {
      form.value.lastPrice = resp.data.data;
      console.log(form.value.lastPrice);
    } else {
      ElMessage({
        message: resp.data.message,
        type: 'error'
      });
    }
  } catch (error) {
    console.error(error);
  }
}

const updatePriceRatio = async (type) => {
  if (form.value.lastPrice == 0 || form.value.lastPrice ==""){
    ElMessage({
      message: "当前价格未获取到，请刷新后重试 或 手动输入当前价格！",
      type: 'error'
    });
    return
  }
  // 根据目标价格计算涨幅
  if (form.value.price > 0 && type == '1'){
    let ratio = String((form.value.price - form.value.lastPrice) / form.value.lastPrice * 100)
    form.value.ratio = ratio.slice(0, ratio.indexOf(".") + 3)
  }
  // 根据涨幅计算目标价格
  if (form.value.ratio != "" && type == '2'){
    let price = String(form.value.lastPrice * (1 + form.value.ratio/100.0))
    form.value.price = price.slice(0, price.indexOf(".") + String(form.value.lastPrice).length - String(form.value.lastPrice).indexOf("."))
  }
}
let selectedItem = ref(null);
let symbolList = ref([])
const updateSymbolList = async () => {
  selectedItem.value = "";
  form.value.symbol = ""
  form.value.baseCoin = ""
  form.value.quoteCoin = ""
  form.value.lastPrice = ""
  form.value.price = ""
  form.value.ratio = ""
  symbolList.value = null
  try {
    const resp = await axios.get('/spot/getSymbol?env='+form.value.env);
    if (resp.data.code === '0000') {
      symbolList.value = resp.data.data;
    } else {
      ElMessage({
        message: "该环境未配置币对，请确认环境可用" + resp.data.message,
        type: 'error'
      });
    }
  } catch (error) {
    console.error(error);
  }
  getLastPrice()
}

const getSymbolSelectValue = async (val) => {
  console.log(val)
  let tmplist = [...symbolList.value]

  const selectObj = tmplist.find((item) => {
    console.log("---" + item.symbolCode)

    return item.symbolCode === val
  })
  form.value.symbol = selectObj.symbolCode;
  form.value.baseCoin = selectObj.baseSymbol
  form.value.quoteCoin = selectObj.pricedSymbol
  selectedItem.value = selectObj.symbolCode;
  console.log("++form:" + form.value)
  getLastPrice()
  form.value.price = ""
  form.value.ratio = ""

};

function reqRecord() {
  let recordData = {
    env: form.value.env,
    module: "现货调价",
    action: JSON.stringify(form.value)
  }
  axios.post('/test/record', recordData)
}


onMounted(() => {
  // axios.get('/build/queryEnvList').then(resp => {
  //     envList.value = resp.data
  // })
  // envList.value = util.env
  updateSymbolList();
})




</script>


<style></style>
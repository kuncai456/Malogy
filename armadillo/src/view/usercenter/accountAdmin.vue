<template>
  <div style="text-align:left;margin-top: -20px">
    <el-select placeholder="请选择环境" v-model="envName" @change="setEnv()">
      <el-option v-for="env in envlist" :key="env.value" :label="env.lable" :value="env.value">
      </el-option>
    </el-select>
  </div>
  <el-form ref="findUserForm" style="text-align: left;background-color: #ffffff;height:100%;margin-top: 1%"
           label-width="80px" class="demo-ruleForm">
    <el-form-item>
      <el-row :gutter="10" style="margin-top: 5%">
        <el-col :span="4">
          <el-input v-model.lazy="findForm.user" clearable placeholder="请输入用户名"></el-input>
        </el-col>
        <el-col :span="4">
          <el-input v-model.lazy="findForm.uid" clearable placeholder="请输入UID"></el-input>
        </el-col>
        <!--        <el-col :span="4">-->
        <!--          <el-input v-model.lazy="findForm.remark" clearable-->
        <!--                    placeholder="请输入备注信息"></el-input>-->
        <!--        </el-col>-->
        <el-button style="margin-left: 1%" type="primary" @click="getUserList(1)" :loading="loading">查询</el-button>
        <el-button style="margin-left: 1%" type="success" @click="showAddUser">邮箱注册</el-button>
        <el-button style="margin-left: 1%" type="success" @click="showAddUsers">批量注册</el-button>
        <el-button style="margin-left: 1%" type="success" @click="showEnterUser">录入账号</el-button>
      </el-row>
    </el-form-item>
    <el-table :data="tableData" size="medium" height="65vh" style="position: sticky">
      <el-table-column prop="user_name" label="登录名" />
      <el-table-column prop="pass_word" label="登录密码" />
      <el-table-column prop="uid" label="UID" />
      <!--      <el-table-column prop="kyc_country" label="认证国籍"/>-->
      <el-table-column prop="kyc_country" label="国籍">
        <template #default="scope">
          <span>{{ getCountryName(scope.row) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="kyc_level" label="认证">
        <template #default="scope">
          <span v-if="scope.row.kyc_level === '0'" style="color:#F56C6C">未认证</span>
          <span v-else style="color:#67C23A">已认证(L{{ scope.row.kyc_level }})</span>
        </template>
      </el-table-column>
      <el-table-column prop="clac_code" label="clc码"/>
      <el-table-column prop="channel_code" label="channel_vip" width="150px">
        <template #default="scope">
          <span>{{scope.row.channel_code}}_{{scope.row.vip_code}}</span>
        </template>
      </el-table-column>
      <!--      <el-table-column prop="channel_vip" label="channel码"/>-->
      <!--      <el-table-column prop="isOperator" label="交易员">-->
      <!--        <template #default="scope">-->
      <!--          <span v-if="scope.row.isOperator==='0'" style="color:#F56C6C">否</span>-->
      <!--          <span v-else style="color:#67C23A">是</span>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
      <el-table-column prop="register_date" label="注册时间"/>
      <el-table-column prop="create_user" label="创建者"/>
      <el-table-column label="操作" width="200px">
        <template #default="scope">
          <el-button size="small" style="margin-left: 5%;" @click="chargeWindow(scope.row)">充值</el-button>
          <el-button size="small" style="margin-left: 5%;" @click="couponWindow(scope.row)">发券</el-button>
          <el-dropdown style="margin-left: 5%;margin-top: 3%">
            <span class="el-dropdown-link">
              更多
              <el-icon class="el-icon--right">
                <arrow-down />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="kycWindow(scope.row)">身份认证</el-dropdown-item>
                <el-dropdown-item @click="operatorWindow(scope.row)">申请交易员</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </el-table-column>
      <!--      <el-table-column prop="remark" label="备注">-->
      <!--        <template #default="scope">-->
      <!--          <textarea class="remarkbody" v-model="scope.row.remark" rows="1" @change="saveRemark(scope.row)"></textarea>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
    </el-table>
    <el-row style="margin-top: 5px">
      <el-pagination :total="total_count" :current-page="cur" layout="prev, pager, next, jumper" :page-size="10"
                     :page-count="totalPage" @current-change="getUserList" placement="top">
      </el-pagination>
    </el-row>
    <el-dialog v-model="add_window" title="邮箱注册" style="text-align: left" customClass="customWidth" class="dialog">
      <el-row :gutter="40" style="width:80%">
        <el-col :span="15">
          <el-form style="text-align: left;" label-width="80px" ref="emailRegisterForm" :model="registerForm"
                   :rules="rules1">
            <el-divider style="margin-top: -2%">用户信息</el-divider>
            <el-row>
              <el-col span="6">
                <el-form-item label="用户名" prop="userName">
                  <el-input v-model.lazy="registerForm.userName" clearable placeholder="请输入用户名" class="a-form"></el-input>
                </el-form-item>
              </el-col>
              <el-col span="6">
                <el-form-item label="用户密码" prop="passWord">
                  <el-input v-model.lazy="registerForm.passWord" clearable placeholder="请输入用户密码"
                            class="width:90%" type="password" show-password></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-divider>邀请信息</el-divider>
            <el-row>
              <el-col span="6">
                <el-form-item label="邀请码" prop="clacCode">
                  <el-input v-model.lazy="registerForm.clacCode" clearable placeholder="请输入clacCode" :disabled="registerForm.registerVipNo != ''"></el-input>
                </el-form-item>
              </el-col>
              <el-col span="6">
                <el-form-item label="vipCode" prop="registerVipNo">
                  <el-input v-model.lazy="registerForm.registerVipNo" clearable placeholder="请输入vipCode" :disabled="registerForm.clacCode != ''"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-divider>认证设置</el-divider>
            <el-row>
              <el-col span="6">
                <el-form-item label="资金密码" prop="tradePass">
                  <el-input v-model.lazy="registerForm.tradePass" clearable placeholder="请输入资金密码"
                            class="a-form" style="width: 80%; margin-left: 2%" type="password" show-password></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row style="margin-top: 1%">
              <el-col>
                <el-checkbox v-model="registerForm.kyc.switch" label="认证"></el-checkbox>
                <el-select placeholder="请选择国家" v-model="registerForm.kyc.area_id" filterable
                           style="width: 25%; margin-left: 2%" :disabled="registerForm.kyc.switch == false">
                  <el-option v-for="(type, index) in authCountrys" :label="type.label" :value="type.value"
                             :key="index"></el-option>
                </el-select>
                <el-select placeholder="请选择级别" v-model="registerForm.kyc.level" filterable
                           style="width: 20%; margin-left: 2%" :disabled="registerForm.kyc.switch == false">
                  <el-option v-for="(type, index) in kycs" :label="type.label" :value="type.value"
                             :key="index"></el-option>
                </el-select>
              </el-col>
            </el-row>
            <el-divider>资产设置</el-divider>
            <el-row :gutter="20" style="margin-top: 1%">
              <el-col span="6">
                <el-checkbox v-model="registerForm.charge.switch" label="现货"></el-checkbox>
                <el-select placeholder="请选择币种" v-model="registerForm.charge.coin_info" filterable
                           style="width: 37%;margin-left: 2%" :disabled="registerForm.charge.switch == false">
                  <el-option v-for="(type, index) in advertiseCoins" :label="type.label" :value="type.value"
                             :key="index"></el-option>
                </el-select>
                <el-input placeholder="数量" v-model="registerForm.charge.amount" clearable
                          style="width: 35%; margin-left: 2%" :disabled="registerForm.charge.switch == false"></el-input>
              </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 1%">
              <el-col span="6">
                <el-checkbox v-model="registerForm.integral.switch" label="积分"></el-checkbox>
                <el-input placeholder="数量" v-model="registerForm.integral.score" clearable
                          style="width: 60%; margin-left: 2%" :disabled="registerForm.integral.switch == false"></el-input>
              </el-col>
            </el-row>
            <!--            <el-divider>身份设置</el-divider>-->
            <!--            <el-row :gutter="20">-->
            <!--              <el-col span="12" style="width: 80%">-->
            <!--                <el-checkbox v-model="registerForm.business.switch" label="申请商家" :disabled="true"></el-checkbox>-->
            <!--              </el-col>-->
            <!--&lt;!&ndash;              <el-col span="12" style="width: 80%">&ndash;&gt;-->
            <!--&lt;!&ndash;                <el-checkbox v-model="registerForm.operator.switch" label="申请交易员"></el-checkbox>&ndash;&gt;-->
            <!--&lt;!&ndash;              </el-col>&ndash;&gt;-->
            <!--            </el-row>-->
          </el-form>
        </el-col>
        <el-col :span="7">
          <div v-if="visible" class="resulta">
            <p style="text-align: left;font-size: medium;">执行结果：</p>
            <el-timeline>
              <el-timeline-item style="text-align: left;" v-for="(item, index) in results" :key="index"
                                :timestamp="item.details" :icon="MoreFilled" :color="item.result ? '#0bbd87' : 'rgb(255 0 0)'"
                                type="primary" size="normal">{{ item.name }}
                <el-timeline v-if="item.name === 'KYC' || item.name === '发布广告'">
                  <el-timeline-item style="text-align: left;" v-for="(item, index) in item.chlid" :key="index"
                                    :timestamp="item.details" :icon="MoreFilled" :color="item.result ? '#0bbd87' : 'rgb(255 0 0)'"
                                    type="primary" size="normal">{{ item.name }}
                  </el-timeline-item>
                </el-timeline>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-col>
      </el-row>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeAdd">取消</el-button>
        <el-button type="primary" @click="register('emailRegisterForm')" :loading="registerLoading">确认</el-button>
      </span>
      </template>
    </el-dialog>
    <el-dialog v-model="adds_window" title="批量注册" style="text-align: left" customClass="customWidth" class="dialog">
      <el-row :gutter="40">
        <el-button v-if="registerList.length === 0" type="success" @click="addParam(0)">添加用户</el-button>
        <el-table :data="registerList" border>
          <el-table-column fixed prop="userName" label="注册邮箱" width="200">
            <template #default="scope">
              <el-input v-model="scope.row.userName" clearable placeholder="请输入登录名" class="a-form"></el-input>
            </template>
          </el-table-column>
          <el-table-column fixed prop="password" label="登录密码">
            <template #default="scope">
              <el-checkbox label="默认密码" v-model="scope.row.defaultPass"></el-checkbox>
              <el-input v-model.lazy="scope.row.passWord" clearable placeholder="请输入登录密码" class="a-form"
                        :disabled="scope.row.defaultPass === true" type="password" show-password></el-input>
            </template>
          </el-table-column>
          <!--          <el-table-column fixed prop="tradePass" label="资金密码">-->
          <!--            <template #default="scope">-->
          <!--              <el-input v-model.lazy="scope.row.tradePass" clearable placeholder="请输入资金密码" class="a-form"></el-input>-->
          <!--            </template>-->
          <!--          </el-table-column>-->
          <el-table-column fixed prop="kyc" label="KYC" width="200">
            <template #default="scope">
              <el-checkbox v-model="scope.row.kyc.switch"></el-checkbox>
              <el-select v-model="scope.row.kyc.area_id" filterable style="margin-left: 3%;width: 45%"
                         :disabled="scope.row.kyc.switch === false">
                <el-option v-for="(type, index) in authCountrys" :label="type.label" :value="type.value"
                           :key="index"></el-option>
              </el-select>
              <el-select v-model="scope.row.kyc.level" filterable style="margin-left: 3%;width: 35%"
                         :disabled="scope.row.kyc.switch === false">
                <el-option v-for="(type, index) in kycs" :label="type.label" :value="type.value" :key="index"></el-option>
              </el-select>
            </template>
          </el-table-column>
          <el-table-column fixed prop="charge" label="资产" width="300">
            <template #default="scope">
              <el-checkbox v-model="scope.row.charge.switch"></el-checkbox>
              <el-select placeholder="请选择币种" v-model="scope.row.charge.coin_info" filterable
                         style="width: 40%;margin-left: 1%" :disabled="scope.row.charge.switch == false">
                <el-option v-for="(type, index) in advertiseCoins" :label="type.label" :value="type.value"
                           :key="index"></el-option>
              </el-select>
              <el-input placeholder="数量" v-model="scope.row.charge.amount" clearable style="margin-left: 3%;width: 45%"
                        :disabled="scope.row.charge.switch == false"></el-input>
            </template>
          </el-table-column>
          <!--        <el-table-column fixed prop="business" label="商家" width="80">-->
          <!--          <template #default="scope">-->
          <!--            <el-checkbox v-model="scope.row.business.switch"></el-checkbox>-->
          <!--          </template>-->
          <!--        </el-table-column>-->
          <el-table-column label="操作" width="140">
            <template #default="scope">
              <el-button type="success" icon="el-icon-plus" @click="addParam(scope.$index)" size="small"
                         circle></el-button>
              <el-button v-if="registerList.length > 1" type="danger" icon="el-icon-minus" @click="delParam(scope.row)"
                         size="small" circle></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="adds_window = false">取消</el-button>
          <el-button type="primary" @click="registerBatch" :loading="registerLoading">提交</el-button>
        </span>
      </template>
    </el-dialog>
    <el-drawer v-model="drawerCheck" direction="rtl">
      <el-card class="box-card" v-for="(nowResults, i) in resultLists" :key="i">
        <template #header>
          <div class="card-header">
            <span>注册账号：</span>
            <span v-if="nowResults != null" text>{{ nowResults[0].details.user }}</span>
          </div>
        </template>
        <el-timeline>
          <el-timeline-item style="text-align: left;" v-for="(item, index) in nowResults" :key="index"
                            :timestamp="item.details" :icon="MoreFilled" :color="item.result ? '#0bbd87' : 'rgb(255 0 0)'" type="primary"
                            size="normal">{{ item.name }}
            <el-timeline v-if="item.name === 'KYC' || item.name === '发布广告'">
              <el-timeline-item style="text-align: left;" v-for="(item, index) in item.chlid" :key="index"
                                :timestamp="item.details" :icon="MoreFilled" :color="item.result ? '#0bbd87' : 'rgb(255 0 0)'"
                                type="primary" size="normal">{{ item.name }}
              </el-timeline-item>
            </el-timeline>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </el-drawer>
    <el-dialog v-model="charge_window" title="快捷充币" width="25%" class="dialog">
      <el-form-item label="UID" prop="UID">
        <el-input placeholder="UID" v-model="chargeForm.uid" clearable style="width: 70%"></el-input>
      </el-form-item>
      <el-form-item label="币种" prop="userName">
        <el-select placeholder="请选择币种" v-model="chargeForm.coin_info" filterable style="width: 70%">
          <el-option v-for="(type, index) in advertiseCoins" :label="type.label" :value="type.value"
                     :key="index"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="数量" prop="userName">
        <el-input placeholder="数量" v-model="chargeForm.amount" clearable style="width: 70%"></el-input>
      </el-form-item>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="charge_window = false">取消</el-button>
        <el-button type="primary" @click="chargeCoin" :loading="chargeLoading">提交</el-button>
      </span>
      </template>
    </el-dialog>
    <el-dialog v-model="coupon_window" title="快捷发券" width="25%" class="dialog">
      <el-form-item label="UID" prop="UID">
        <el-input placeholder="UID" v-model="couponForm.uid" clearable style="width: 70%"></el-input>
      </el-form-item>
      <el-form-item label="类型" prop="userName">
        <el-select placeholder="请选择类型" v-model="couponForm.card_type" filterable style="width: 70%" @change="pickCoupon">
          <el-option v-for="(type, index) in couponTypes" :label="type.card_type"
                     :value="type.card_type"
                     :key="index"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="数量" prop="userName">
        <el-input placeholder="数量" v-model="couponForm.amount" clearable style="width: 70%"></el-input>
      </el-form-item>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="coupon_window = false">取消</el-button>
        <el-button type="primary" @click="grantCoupon" :loading="couponLoading">提交</el-button>
      </span>
      </template>
    </el-dialog>
    <el-dialog v-model="kyc_window" title="快捷认证" width="25%" class="dialog">
      <el-form-item label="UID" prop="UID">
        <el-input placeholder="UID" v-model="kycForm.uid" clearable style="width: 70%"></el-input>
      </el-form-item>
      <el-form-item label="国籍" prop="area_id">
        <el-select placeholder="请选择国家" v-model="kycForm.area_id" filterable style="width: 60%" >
          <el-option v-for="(type, index) in authCountrys" :label="type.label" :value="type.value"
                     :key="index"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="级别" prop="level">
        <el-select placeholder="请选择级别" v-model="kycForm.level" filterable style="width: 60%">
          <el-option v-for="(type, index) in kycs" :label="type.label" :value="type.value"
                     :key="index"></el-option>
        </el-select>
      </el-form-item>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="kyc_window = false">取消</el-button>
        <el-button type="primary" @click="kyc" :loading="kycLoading">提交</el-button>
      </span>
      </template>
    </el-dialog>
    <el-dialog v-model="enter_window" title="录入账号" width="25%" class="dialog">
      <el-form-item prop="user_account" label="账号: ">
        <el-input v-model="enterForm.username" placeholder="请输入账号"></el-input>
      </el-form-item>
      <el-form-item prop="user_pwd" label="密码: ">
        <el-input v-model="enterForm.password" placeholder="请输入密码" type="password" show-password></el-input>
      </el-form-item>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="enter_window = false">取消</el-button>
        <el-button type="primary" @click="enter" :loading="enterLoading">提交</el-button>
      </span>
      </template>
    </el-dialog>
    <el-dialog v-model="operator_window" title="申请交易员" width="25%" class="dialog">
      <el-form-item label="UID" prop="UID">
        <el-input placeholder="UID" v-model="operatorForm.uid" clearable style="width: 70%"></el-input>
      </el-form-item>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="operator_window = false">取消</el-button>
        <el-button type="primary" @click="applyOperator" :loading="operatorLoading">提交</el-button>
      </span>
      </template>
    </el-dialog>
  </el-form>
</template>

<script>
import axios from 'axios'
import ActivityBase from "../../libs/ActivityBase";
import {ArrowDown} from "@element-plus/icons-vue";

export default {
  name: "accountAdmin",
  components: {ArrowDown},
  computed: {
    ActivityBase() {
      return ActivityBase
    }
  },
  data() {
    return {
      envName:ActivityBase.data().envName,
      envlist : ActivityBase.data().envlist,
      qaUser : ActivityBase.data().qaUser,
      authCountrys : ActivityBase.data().authCountrys,
      auth : false,
      findForm: {
        user: '',
        uid: '',
        authType: '',
        maxLevel: '',
        remark: ''
      },
      loading: false,
      registerLoading: false,
      chargeLoading: false,
      couponLoading: false,
      kycLoading: false,
      operatorLoading:false,
      enterLoading: false,
      tableData: [],
      cur: 1,
      total_count: 1,
      totalPage: 1,
      add_window: false,
      adds_window: false,
      enter_window: false,
      charge_window: false,
      coupon_window: false,
      kyc_window: false,
      operator_window : false,
      drawerCheck: false,
      registerForm: {
        qaUser: this.qaUser,
        userName: '',
        defaultPass: true,
        passWord: 'Cs123456@',
        tradePass: 'Cs123456',
        clacCode: '',
        registerChannel: '',
        registerVipNo: '',
        area_id: 201,
        kyc: {
          switch: false,
          area_id: 201,
          level: 1
        },
        business: {
          switch: false,
          level: 1,
        },
        operator: {
          switch: false,
        },
        receiptAccount: {
          switch: false,
          method: "银行卡",
          methodId: 1
        },
        charge: {
          switch: false,
          coin_info: 'USDT',
          amount: '10000',
        },
        integral: {
          switch: false,
          score: '1000',
        },
        advertise: {
          switch: false,
          coin_info: 'RUB',
          coin: '',
        }
      },
      registerList: [],
      newRegisterList: [],
      chargeForm: {
        uid: '',
        coin_info: 'USDT',
        amount: 1000,
        recharge_type: '外链入金'
      },
      couponForm:{
        uid:'',
        card_type: '抵扣券',
        amount: 10,
        token_id: "USDT",
        business_type: "1",
        position_type: 0,
        earn_days: 7,
        earn_rate: 100,
        is_auto: "0",
        env: this.envName
      },
      kycForm:{
        uid:'',
        area_id: 201,
        level: 1
      },
      operatorForm:{
        uid:'',
      },
      enterForm:{
        username:'',
        password: '',
      },
      registerChannels:[
        {"label": "l1", "value": 'v1'},
        {"label": "l2", "value": 'v2'},
      ],
      registerVipNos:[
        {"label": "l1", "value": 'v1'},
        {"label": "l2", "value": 'v2'},
      ],
      kycs: [
        { "label": "L1", "value": 1 },
        { "label": "L2", "value": 2 },
      ],
      advertiseCoins: [
        { "label": "BTC", "value": "BTC" },
        { "label": "USDT", "value": "USDT" },
        { "label": "ETH", "value": "ETH" },
        { "label": "BGB", "value": "BGB" },
      ],
      couponTypes: [
        {"card_type":"抵扣券","business_type":"1","token_id":"USDT","is_auto":"0","earn_rate":100,"earn_days":1},
        {"card_type":"体验金","business_type":"10","token_id":"USDT","is_auto":"0","earn_rate":100,"earn_days":1},
        {"card_type":"现金券","business_type":"1","token_id":"USDT","is_auto":"0","earn_rate":100,"earn_days":1},
        {"card_type":"加息券","business_type":"6","token_id":"USDT","is_auto":"0","earn_rate":100,"earn_days":1},
        {"card_type":"减息券","business_type":"23","token_id":"USDT","is_auto":"0","earn_rate":100,"earn_days":1}
      ],
      businessLevels: [
        { "label": "商家", "value": 1 },
      ],
      receiptAccounts: [
        { "label": "银行卡", "value": 1 },
      ],
      authLevels: [
        { "label": "未认证", "value": 0 },
        { "label": "L1认证", "value": 1 },
        { "label": "L2认证", "value": 2 },
      ],
      rules1: {
        userName: [
          {
            required: true,
            message: '请输入用户名',
            trigger: 'blur',
          }
        ],
        passWord: [
          {
            required: true,
            message: '请输入用户密码',
            trigger: 'blur',
          }
        ],
        tradePass: [
          {
            required: false,
            message: '请输入用户资金密码',
            trigger: 'blur',
          }],
        area_id: [
          {
            required: true,
            message: '请选择国籍',
            trigger: 'blur',
          }],


      },
      results: [],
      registerId: '',
      registerRead: false,
      resultLists: [],
      registerIdList: [],
      visible: false,
      icon: {
        refresh: "https://hx.huobiapps.com/staticFront/assets/vector.c4f35866.svg"
      }
    }
  },
  methods: {
    setEnv() {
      ActivityBase.methods.setEnv(this.envName, this.qaUser)
    },
    record() {
      ActivityBase.methods.recordSend(this.envName, this.qaUser)
    },
    refresh(row) {
      const data = {
        username: row.user_name,
        password: ''
      }
      row.loading = true;
      axios.post("/proxy/flask/check_login", data)
          .then(resp => {
            if(resp.data.code === '0000'){
              this.$message.sucess = "成功";
              this.enter_window = false
            } else {
              this.$message.error("失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("失败：" + error);
          })
          .finally(() => {
            row.loading = false
            this.record()
            this.getUserList()
          });
    },
    saveRemark(row) {
      const data = { "id": row.id, "remark": row.remark }
      axios.post("/set-user-remark", data)
          .then(resp => {
            if(resp.data.code === '0000'){
              this.$message.success("成功")
            }else {
              this.$message.error("失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("失败：" + error);
          })
          .finally(() => {
            this.loading = false;
            this.record()
          });
    },
    showAddUser() {
      this.registerId = ''
      this.registerRead = false
      this.add_window = true
    },
    closeAdd(){
      this.registerId = ''
      this.registerRead = false
      this.add_window = false
      this.getUserList()
    },
    showAddUsers() {
      this.registerList = []
      this.newRegisterList = []
      this.addParam(0)
      this.adds_window = true
    },
    showEnterUser() {
      this.enter_window = true
    },
    getCountryName(val){
      if(val.kyc_country === 0){
        return ''
      }
      for (let key in this.authCountrys) {
        if (this.authCountrys[key].value === val.kyc_country) {
          return this.authCountrys[key].label
        }
      }
      return val.kyc_country
    },
    clearSearch() {
      this.findForm.user = '',
          this.findForm.uid = '',
          this.findForm.authType = '',
          this.findForm.maxLevel = '',
          this.findForm.remark = ''
    },
    getUserList(page) {
      page = arguments[0] ? arguments[0] : 1
      this.cur = page
      this.loading = true;
      const data = {
        userBody: {
          pageSize: 10,
          currPage: this.cur,
          user: this.findForm.user,
          uid: this.findForm.uid,
          authType: this.findForm.authType,
          maxLevel: this.findForm.maxLevel,
          remark: this.findForm.remark
        }
      }
      axios.post("/activity/user/get-register-history", data)
          .then(resp => {
            if(resp.data.code === '0000'){
              this.tableData = resp.data.data.dbData
              this.total_count = resp.data.data.totalCount
              this.totalPage = resp.data.data.totalPage
            } else {
              this.$message.error("读取失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("失败：" + error);
          })
          .finally(() => {
            this.loading = false;
            this.record()
          });
    },
    chargeWindow(val) {
      this.charge_window = true
      this.chargeForm.uid = val.uid
    },
    chargeCoin() {
      this.chargeLoading = true
      const data = this.chargeForm
      axios.post("/proxy/flask/user_fast_recharge", data)
          .then(resp => {
            if(resp.data.code === '0000'){
              this.$message.sucess = "充币成功";
              this.charge_window = false
            } else {
              this.$message.error("充币失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("充币失败：" + error);
          })
          .finally(() => {
            this.chargeLoading = false
            this.record()
          });
    },
    couponWindow(val) {
      this.coupon_window = true
      this.couponForm.uid = val.uid
      // this.$router.push('/CouponsCenter')
      // sessionStorage.setItem('index', '18');
    },
    pickCoupon(){
      console.log("开始赋值")
      for(let key in this.couponTypes){
        if(this.couponTypes[key].card_type === this.couponForm.card_type){
          this.couponForm.token_id = this.couponTypes[key].token_id
          this.couponForm.business_type = this.couponTypes[key].business_type
          this.couponForm.earn_days = this.couponTypes[key].earn_days
          this.couponForm.earn_rate = this.couponTypes[key].earn_rate
          this.couponForm.is_auto = this.couponTypes[key].is_auto
        }
      }
    },
    grantCoupon() {
      this.couponLoading = true
      const data = this.couponForm
      axios.post("/proxy/flask/user_card_receive", data)
          .then(resp => {
            if(resp.data.code === '0000'){
              this.$message.sucess = "成功";
              this.coupon_window = false
            } else {
              this.$message.error("失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("失败：" + error);
          })
          .finally(() => {
            this.couponLoading = false
            this.record()
          });
    },
    kycWindow(val) {
      this.kyc_window = true
      this.kycForm.uid = val.uid
      // this.$router.push('/CouponsCenter')
      // sessionStorage.setItem('index', '18');
    },
    //kyc
    kyc(){
      this.kycLoading = true
      const data = this.kycForm
      axios.post("/activity/user/kyc", data)
          .then(resp => {
            if(resp.data.code === '0000'){
              this.$message.sucess = "成功";
              this.kyc_window = false
            } else {
              this.$message.error("失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("生成失败：" + error);
          })
          .finally(() => {
            this.getUserList()
            this.kycLoading = false
            this.record()
          });
    },
    operatorWindow(val) {
      this.operator_window = true
      this.operatorForm.uid = val.uid
    },
    applyOperator(){
      this.operatorLoading = true
      const data = this.operatorForm
      axios.post("/activity/user/operator", data)
          .then(resp => {
            if(resp.data.code === '0000'){
              this.$message.sucess = "成功";
              this.operator_window = false
            } else {
              this.$message.error("失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("生成失败：" + error);
          })
          .finally(() => {
            this.getUserList()
            this.operatorLoading = false
            this.record()
          });
    },
    //录入
    enter(){
      this.enterLoading = true
      const data = this.enterForm
      axios.post("/proxy/flask/check_login", data)
          .then(resp => {
            if(resp.data.code === '0000'){
              this.$message.sucess = "成功";
              this.enter_window = false
            } else {
              this.$message.error("失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("生成失败：" + error);
          })
          .finally(() => {
            this.enterLoading = false
            this.record()
            this.getUserList()
          });
    },
    //注册
    register(formName) {
      this.results = []
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.registerLoading = true
          const data = this.registerForm
          this.$http.post("/activity/user/register", data)
              .then(resp => {
                if(resp.data.code === '0000'){
                  this.registerId = resp.data.data
                  this.$message.sucess = "提交成功";
                  this.visible = true
                  this.registerRead = true
                } else {
                  this.$message.error("提交失败：" + resp.data.message);
                }
              })
              .catch(error => {
                this.$message.error("生成失败：" + error);
              })
              .finally(() => {
                this.getUserList()
                this.registerLoading = false
                this.record()
              });
        } else {
          return false
        }
      })
    },
    //批量注册
    registerBatch() {
      // this.drawerCheck = true
      this.registerLoading = true
      const data = this.registerList
      axios.post("/activity/user/register-list", data)
          .then(resp => {
            if(resp.data.code === '0000'){
              this.registerIdList = resp.data.data
              this.$message.sucess = "提交成功";
              this.visible = true
              // this.adds_window = false
              this.drawerCheck = true
            } else {
              this.$message.error("提交失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("生成失败：" + error);
          })
          .finally(() => {
            // this.getUserList()
            this.registerLoading = false
            this.record()
          });
    },
    //获取批量注册进度
    getRegisterListSchedule() {
      // this.registerLoading = true
      const data = {
        registerIdList: this.registerIdList
      }
      axios.post("/activity/user/get-register-list-schedule", data)
          .then(resp => {
            if (resp.data.code === '0000') {
              this.resultLists = resp.data.data
              this.$message.sucess = "成功";
            } else {
              this.$message.error("失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("生成失败：" + error);
          })
          .finally(() => {
            // this.getUserList()
            // this.registerLoading = false
          });
    },
    //获取注册进度
    getRegisterSchedule() {
      const data = {
        registerId: this.registerId
      }
      axios.post("/activity/user/get-register-schedule", data)
          .then(resp => {
            if (resp.data.code === '0000') {
              this.results = resp.data.data
              this.$message.sucess = "成功";
            } else {
              this.$message.error("失败：" + resp.data.message);
            }
          })
          .catch(error => {
            this.$message.error("生成失败：" + error);
          })
          .finally(() => {
            // this.getUserList()
            // this.registerLoading = false
          });
    },
    // 新增参数
    addParam(index) {
      this.newRegisterList.splice(index + 1, 0, {
        qaUser: this.qaUser,
        userName: '',
        defaultPass: true,
        passWord: 'Cs123456@',
        tradePass: 'Cs123456',
        area_id: 201,
        kyc: {
          switch: false,
          level: 1,
          area_id: 201
        },
        business: {
          switch: false,
          level: 1
        },
        charge: {
          switch: false,
          coin_info: 'USDT',
          amount: '10000',
        },
      })
      this.registerList = this.newRegisterList
    },
    delParam(item) {
      var index = this.registerList.indexOf(item)
      if (index !== -1) {
        this.registerList.splice(index, 1)
      }
      if (this.newRegisterList.length == 0) {
        this.isActive = false
      }
    },
    round() {
      this.innerTimers = window.setInterval(() => {
        if (this.add_window == true && this.drawerCheck == true) {
          this.getRegisterListSchedule()
        }
        if (this.add_window == true && this.registerRead == true) {
          this.getRegisterSchedule()
        }
      }, 5000);
    },
    round2() {
      this.innerTimers = window.setInterval(() => {
        if(this.add_window == false){
          this.getUserList()
        }
      }, 30000);
    },
  },
  created() {
    this.setEnv()
    this.getUserList()
    this.round()
    // this.round2()
    // if(util.getLoginName() === 'hasaki.huang' || util.getLoginName() === 'hasaki.huang'){
    //   this.auth = true
    // }
  },
  watch: {
    envName: function () {
      this.getUserList()
    }
  }

}
</script>

<style>
.activity-card-1 {
  width: 650px;
  top: 50px;
}

.activity-card-2 {
  width: 350px;
  top: 50px;
  left: 240px;
}

.customWidth {
  width: 70%;
}
</style>
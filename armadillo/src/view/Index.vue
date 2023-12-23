<template>
  <div style="width: 200px;" class="menu">
    <div class="swap">
      <el-row class="tac">
        <el-col>
          <el-menu
              active-text-color="#67C23A"
              background-color="#337ecc"
              class="el-menu-vertical-demo"
              default-active="2"
              text-color="#ecf5ff"
              @open="handleOpen"
              @close="handleClose"
              style="border: none;"
          >
            <el-menu-item index="1">
              <el-icon><HomeFilled /></el-icon>
              <router-link to="/home" custom v-slot="{ navigate }">
                <span @click="navigate" role="link">首页</span>
              </router-link>
            </el-menu-item>
            <el-sub-menu index="2">
              <template #title>
                <el-icon><Box /></el-icon>
                <span>潘多拉盒</span>
              </template>
              <el-menu-item index="2-1">
                <el-icon><Ship /></el-icon>
                <router-link to="/build" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">服务构建</span>
                </router-link>
              </el-menu-item>
              <el-menu-item index="2-2">
                <el-icon><Briefcase /></el-icon>
                <router-link to="/install" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">安装包</span>
                </router-link>
              </el-menu-item>
              <el-menu-item index="2-3">
                <el-icon><ChromeFilled /></el-icon>
                <router-link to="/lang" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">多语言检查</span>
                </router-link>
              </el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="3">
              <template #title>
                <el-icon><UserFilled /></el-icon>
                <span>账户概览</span>
              </template>
              <el-menu-item index="3-1">
                <el-icon><Money /></el-icon>
                <router-link to="/deposit" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">虚拟币充值</span>
                </router-link>
              </el-menu-item>
              <el-menu-item index="3-2">
                <el-icon><Avatar /></el-icon>
                <router-link to="/user" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">用户管理</span>
                </router-link>
              </el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="4">
              <template #title>
                <el-icon><Histogram /></el-icon>
                <span>行情中心</span>
              </template>
              <el-menu-item index="4-1">
                <el-icon><DataLine /></el-icon>
                <router-link to="/book" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">铺单工具</span>
                </router-link>
              </el-menu-item>
              <el-menu-item index="4-2">
                <el-icon><TrendCharts /></el-icon>
                <router-link to="/markIndex" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">标记/指数价</span>
                </router-link>
              </el-menu-item>
              <el-menu-item index="4-3">
                <el-icon><Checked /></el-icon>
                <router-link to="/uprice" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">调整成交价</span>
                </router-link>
              </el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="5">
              <template #title>
                <el-icon><ElemeFilled /></el-icon>
                <span>接口调用</span>
              </template>
              <el-menu-item index="5-1">
                <el-icon><Paperclip /></el-icon>
                <router-link to="/restful" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">Restful</span>
                </router-link>
              </el-menu-item>
              <el-menu-item index="5-2">
                <el-icon><Lightning /></el-icon>
                <router-link to="/websocket" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">webSocket</span>
                </router-link>
              </el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="6">
              <template #title>
                <el-icon><SwitchFilled /></el-icon>
                <span>交易校验器</span>
              </template>
              <el-menu-item index="6-1">
                <el-icon><Bicycle /></el-icon>
                <router-link to="/copy" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">跟单系统</span>
                </router-link>
              </el-menu-item>
              <el-menu-item index="6-2">
                <el-icon><Cpu /></el-icon>
                <router-link to="/bots" custom v-slot="{ navigate }">
                  <span @click="navigate" role="link">策略系统</span>
                </router-link>
              </el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-col>
      </el-row>
    </div>
    <div class="logout">
      <el-menu
          active-text-color="#67C23A"
          background-color="#337ecc"
          class="el-menu-vertical-demo"
          default-active="2"
          text-color="#ecf5ff"
      >
        <el-menu-item>
          <el-icon><Fold /></el-icon>退出系统
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>

<script setup>
import {
  Cpu,
  Box,
  Fold,
  Ship,
  Avatar,
  Money,
  Checked,
  Bicycle,
  DataLine,
  Histogram,
  HomeFilled,
  Briefcase,
  UserFilled,
  TrendCharts,
  ChromeFilled,
  Paperclip,
  Lightning,
  ElemeFilled,
  SwitchFilled,
} from '@element-plus/icons-vue'
const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}
const handleClose = (key, keyPath) => {
  console.log(key, keyPath)
}

</script>

<style scoped>
.menu{
  width: 165px;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  background: #337ecc;
  padding-bottom: 40px;
  display: flex;
  flex-direction: column;
}
.swap{
  flex: 1;
  overflow-y: auto;
}
.logout{
  left: 0;
  bottom: 0;
  height: 25px;
  color: #ecf5ff;
  background: #337ecc;
}

</style>
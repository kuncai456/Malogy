<template>
  <ElConfigProvider :locale="zhCn">
    <div class="swapper">
      <index></index>
      <router-view/>
    </div>
  </ElConfigProvider>
</template>


<script setup>
import { ElConfigProvider } from 'element-plus';
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import index from "@/view/Index.vue";

</script>

<style>

</style>
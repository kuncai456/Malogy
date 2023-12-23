<template>
  <div id="root">
    <!-- 主体内容 -->
    <div class="container mt-3 main-container">
      <div class="row monospace">
        <div class="overall">
          <div class="card">
            <!-- 应用容器 -->
            <div class="card-body">
              <div class="row">
                <!-- 左侧面板 -->
                <div class="lefthand">
                  <!-- 服务设置 -->
                  <div class="col-sm-12">
                    <h5 class="card-title">服务器配置 状态: {{ 1 }}</h5>  <!--ToDo 服务器状态-->
                    <hr class="divider divider-dashed">
                    <!-- 连接地址 -->
                    <div class="card-text">
                      <div class="input-group">
                        <div class="input-group-prepend">
                          <div class="input-group-text">服务地址</div>
                        </div>
                        <input type="text" class="form-control" placeholder="输入 WebSocket 服务器地址" v-model="address">
                        <div class="input-group-append">
                          <button type="button" class="btn btn-block" :class="connected ? 'btn-danger' : 'btn-success'" @click="autoWsConnect">{{ connected ? '关闭连接' : '开启连接' }}</button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- 发包设置 -->
                  <div class="col-sm-12 mt-3">
                    <h5 class="card-title">发包设置</h5>
                    <hr class="divider divider-dashed">
                    <!-- 自动发送 -->
                    <div class="card-text">
                      <div class="input-group">
                        <div class="input-group-prepend">
                          <div class="input-group-text">每隔</div>
                        </div>
                        <input title="" type="text" class="form-control text-center" v-model="heartBeatSecond" :disabled="!connected">
                        <div class="input-group-append input-group-prepend">
                          <span class="input-group-text">秒发送内容</span>
                        </div>
                        <input title="" type="text" class="form-control" v-model="heartBeatContent" :disabled="!connected">
                        <div class="input-group-append">
                          <button type="button" class="btn btn-block" :class="autoSend ? 'btn-danger' : 'btn-success'" @click="autoHeartBeat" :disabled="!connected">{{ autoSend ? '停止发送' : '开始发送' }}</button>
                        </div>
                      </div>
                    </div>
                    <!-- 手动发送 -->
                    <div class="card-text mt-2">
                      <textarea class="form-control mt-1" id="exampleTextarea" rows="2" placeholder="需要发送到服务端的内容" v-model="content" :disabled="!connected"></textarea>
                      <div class="custom-control custom-checkbox inline-flex mt-2">
                        <input type="checkbox" class="custom-control-input" id="sendClean" v-model="sendClean" :disabled="!connected">
                        <label class="custom-control-label" for="sendClean">发包清空输入</label>
                      </div>
                    </div>
                    <div class="card-text mt-2">
                      <button class="btn btn-block btn-success" :disabled="!connected" @click="sendData">发送到服务端</button>
                    </div>
                  </div>
                  <!-- 调试消息 -->
                  <div class="col-sm-12 mt-3">
                    <h5 class="card-title">调试消息</h5>
                    <hr class="divider divider-dashed">
                    <div class="card-text">
                      <div class="card-title console-box" id="console-box">
                        <div class="mb-2" v-for="item in consoleData">
                          <strong :class="'text-'+item.type">{{item.time}} => </strong> <span>{{item.content}}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- 右侧面板 -->
                <div class="righthand">
                  <!-- 消息记录 -->
                  <div class="col-sm-12">
                    <h5 class="card-title" style="display: inline">消息记录</h5>
                    <a href="javascript:void(0);" @click="cleanMessage">清空消息</a>
                    <hr class="divider divider-dashed">
                    <div>
                      <div class="custom-control custom-checkbox inline-flex mt-2">
                        <input type="checkbox" class="custom-control-input" id="recvClean" v-model="recvClean" :disabled="!connected">
                        <label class="custom-control-label" for="recvClean">收包清空记录</label>
                      </div>
                      <div class="custom-control custom-checkbox inline-flex mt-2">
                        <input type="checkbox" class="custom-control-input" id="recvDecode" v-model="recvDecode" :disabled="!connected">
                        <label class="custom-control-label" for="recvDecode">收包JSON解码</label>
                      </div>
                      <div class="custom-control custom-checkbox inline-flex mt-2">
                        <input type="checkbox" class="custom-control-input" id="recvPause" v-model="recvPause" :disabled="!connected">
                        <label class="custom-control-label" for="recvPause">暂停接收</label>
                      </div>
                    </div>
                    <hr class="divider divider-dashed">
                    <div class="card-text message-box" id="message-box">
                      <template v-for="item in messageData">
                        <div class="mb-4" :class="{ 'text-left' : item.direction , 'text-left' : !item.direction }">
                          <strong><span :class="{'text-success' : item.direction , 'text-primary' : !item.direction}">{{item.direction ? '发送' : '收到'}}消息</span> {{item.time}}</strong>
                          <div class="monospace" v-if="!recvDecode"> {{ item.content }}</div>
                          <div class="monospace" v-html='JSON.format(item.content)' v-if="recvDecode"></div>
                        </div>
                      </template>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "websocket"
}

</script>

<style scoped>

</style>
import { createRouter, createWebHashHistory } from 'vue-router'
import home from '@/view/home.vue'
import restful from '@/view/hickycall/restful.vue'
import websocket from '@/view/hickycall/websocket.vue'
import user from '@/view/usercenter/accountAdmin.vue'
import deposit from '@/view/usercenter/deposit.vue'
import kycVerify from '@/view/usercenter/kycVerify.vue'
import build from '@/view/utilitybox/buildService.vue'
import install from '@/view/utilitybox/installer.vue'
import lang from '@/view/utilitybox/langVerify.vue'
import markIndex from '@/view/quotation/markIndex.vue'
import book from '@/view/quotation/orderBook.vue'
import uprice from '@/view/quotation/tradedPrice.vue'
import copy from "@/view/strategy/copyTrade.vue"
import bots from "@/view/strategy/botsTrade.vue"



const routes = [
    {
        path: '/uprice',
        name: 'uprice',
        component: uprice,
    },{
        path: '/markIndex',
        name: 'markIndex',
        component: markIndex,
    },{
        path: '/book',
        name: 'book',
        component: book,
    },{
        path: '/home',
        name: 'home',
        component: home,
    },{
        path: '/',
        redirect: '/home'
    },{
        path: '/',
        redirect: '/home'
    },{
        path: '/restful',
        name: 'restful',
        component: restful,
    },{
        path: '/websocket',
        name: 'websocket',
        component: websocket,
    },{
        path: '/user',
        name: 'user',
        component: user,
    },{
        path: '/deposit',
        name: 'deposit',
        component: deposit,
    },{
        path: '/kyc',
        name: 'kyc',
        component: kycVerify,
    },{
        path: '/build',
        name: 'build',
        component: build,
    },{
        path: '/install',
        name: 'install',
        component: install,
    },{
        path: '/lang',
        name: 'lang',
        component: lang,
    },{
        path: '/copy',
        name: 'copy',
        component: copy,
    },{
        path: '/bots',
        name: 'bots',
        component: bots,
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
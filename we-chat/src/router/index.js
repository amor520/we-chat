import Vue from 'vue'
import Router from 'vue-router'
import WeChat from '@/components/WeChat'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'WeChat',
      component: WeChat
    }
  ]
})

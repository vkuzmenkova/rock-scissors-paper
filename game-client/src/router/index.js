import { createRouter, createWebHistory } from 'vue-router'

import GamePlayView from '../views/GamePlayView.vue'
import LeaderBoardView from '../views/LeaderBoardView.vue'
import AuthFormView from '../views/AuthFormView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: GamePlayView
    },
    {
      path: '/leaderboard',
      component: LeaderBoardView
    },
    {
      path: '/auth',
      component: AuthFormView
    }
  ]
})

export default router

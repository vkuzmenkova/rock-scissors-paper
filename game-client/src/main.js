import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import GamePlay from './components/GamePlay.vue' 
import LeaderBoard from './components/LeaderBoard.vue'
import AuthForm from './components/AuthForm.vue'

const pinia = createPinia()

const app = createApp(App)
app.component('GamePlay', GamePlay)
app.component('LeaderBoard', LeaderBoard)
app.component('AuthForm', AuthForm)

app.use(pinia)
app.use(router)

app.mount('#app')

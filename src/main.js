import './assets/main.css'

import { createApp } from 'vue'
import App from './SurveyApp.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)

const vm = app.mount('#app')

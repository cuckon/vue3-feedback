<script setup>
import EngineerPanel from './components/EngineerPanel.vue'
import Divider from './components/Divider.vue'
import EngineersSelector from './components/EngineersSelector.vue'
import {ref, getCurrentInstance} from 'vue'

const isFetching = ref(false)
const hasSubmitted = ref(false)
const failedToSubmit = ref(false)
const feedbackResults = ref({})
const feedbacker = ref('John')
const engineersSelected = ref([])
const domain = getCurrentInstance().appContext.config.globalProperties.$domain

async function onSubmit() {
    isFetching.value = true
    let feedbacks = []
    engineersSelected.value.forEach((eng, index)=>{
        const feedbackValue = feedbackResults.value[index]

        feedbacks[index] = {
            to: eng,
            rate: feedbackValue.rate,
            good_comment: feedbackValue.goodFeedback,
            bad_comment: feedbackValue.badFeedback,
        }
    })

    try{
        const resp = await fetch(
            domain + '/feedbacks',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body:  JSON.stringify({
                    user: feedbacker.value,
                    timestamp: Date.now(),
                    feedbacks: feedbacks
                })
            })
        const data = await resp.json()
        console.log(data)
        hasSubmitted.value = true
    } catch(error) {
        console.error(error)
        failedToSubmit.value = true
    }

}
</script>

<template>
    <el-container style="width:800px;">
        <el-header>
            <h1>调查问卷</h1>
        </el-header>
        <el-main>
            <p>请添加要评价的人。</p>
            <EngineersSelector :feedbacker="feedbacker"
                v-model:engineersSelected="engineersSelected"/>

            <el-form label-width="300px" label-position="right">
                <div v-for="(engineer, index) in engineersSelected">
                    <Divider/>
                    <EngineerPanel :name="engineer"
                    v-model:result="feedbackResults[index]"/>
                </div>

                <Divider/>

                <el-button @click="onSubmit" :disabled="isFetching">提交</el-button>
                <el-text v-if="hasSubmitted" type="success"> 提交成功</el-text>
                <el-text v-if="failedToSubmit" type="danger"> 提交失败</el-text>
            </el-form>
        </el-main>
    </el-container>
</template>

<style scoped>
.banner {
  display:block;
  margin: 0 auto 2rem;
}
</style>
<script setup>
import EngineerPanel from './components/EngineerPanel.vue'
import Divider from './components/Divider.vue'
import {ref} from 'vue'
import { useFetch } from '@vueuse/core'


const engineers = [
    '苏', '张'
]
const engineersSelected = ref([])

const { isFetching, isFinished, execute } = useFetch('http://127.0.0.1:8000/feedbacks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  immediate: false,
  body:  JSON.stringify({
        user: 'William Ding',
        time: '2021-08-634',
        // feedbacks: [
        //     {
        //         to: 'John',
        //         rate: 5,
        //         good_comment: 'Great',
        //         bad_comment: 'haheh'
        //     },
        //     {
        //         to: 'Mary',
        //         rate: 4,
        //         good_comment: 'Good',
        //         bad_comment: 'h'
        //     },
        // ]
    })
}).post().json()

const onSubmit = () => {
    const feedbackData = {
        user: 'William Ding',
        time: '2021-08-19 16:34',
        // feedbacks: [
        //     {
        //         to: 'John',
        //         rate: 5,
        //         good_comment: 'Great',
        //         bad_comment: 'haheh'
        //     },
        //     {
        //         to: 'Mary',
        //         rate: 4,
        //         good_comment: 'Good',
        //         bad_comment: 'h'
        //     },
        // ]
    }

    execute(feedbackData)
}

const feedbackResults = ref({})

</script>

<template>
    <el-container style="width:800px;">
        <el-header>
            <h1>调查问卷</h1>
        </el-header>
        <el-main>
            <p>请添加要评价的人。</p>
            <el-select multiple v-model="engineersSelected">
                <el-option
                v-for="engineer in engineers"
                :key="engineer"
                :label="engineer"
                :value="engineer"
                />
            </el-select>
            <el-form label-width="300px" label-position="right">
                <div v-for="(engineer, index) in engineersSelected">
                    <Divider/>
                    <EngineerPanel :name="engineer"
                    v-model:result="feedbackResults[index]"/>
                </div>

                <Divider/>
                <el-button @click="onSubmit" :disabled="isFetching">提交</el-button>
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
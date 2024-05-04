<script setup>
import EngineerPanel from './components/EngineerPanel.vue'
import Divider from './components/Divider.vue'
import {ref} from 'vue'

const engineers = [
    '苏', '张'
]
const engineersSelected = ref([])

async function onSubmit() {
    try{
        const resp = await fetch(
            'http://127.0.0.1:8000/feedbacks',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body:  JSON.stringify({
                    user: 'William Ding',
                    timestamp: Date.now(),
                    feedbacks: [
                        {
                            to: 'John',
                            rate: 5,
                            good_comment: 'Great!!!',
                            bad_comment: 'haheh'
                        },
                        {
                            to: 'Mary',
                            rate: 4,
                            good_comment: 'Good',
                            bad_comment: 'h'
                        },
                    ]
                })
            })
        const data = await resp.json()
        console.log(data)
    } catch(error) {
        console.error(error)
    }

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
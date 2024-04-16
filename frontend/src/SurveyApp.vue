<script setup>
import EngineerPanel from './components/EngineerPanel.vue'
import Divider from './components/Divider.vue'
import {ref, reactive} from 'vue'

const engineers = [
    '苏', '张'
]
const engineersSelected = ref([])

const onSubmit = () => {
    console.log(JSON.stringify(feedbackResults.value))
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
                <el-button @click="onSubmit">提交</el-button>
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
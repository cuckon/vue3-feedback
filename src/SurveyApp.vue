<script setup>
import EngineerPanel from './components/EngineerPanel.vue'
import Divider from './components/Divider.vue'
import {ref} from 'vue'

const Engineers = [
    '苏', '张'
]
const EngineersSelected = ref([])
</script>

<template>
    <el-container style="width:800px;">
        <el-header>
            <h1>调查问卷</h1>
        </el-header>
        <el-main>
            <p>请添加要评价的人。</p>
            <el-select multiple v-model="EngineersSelected">
                <el-option
                v-for="Engineer in Engineers"
                :key="Engineer"
                :label="Engineer"
                :value="Engineer"
                />
            </el-select>
            <el-form label-width="300px" label-position="right">
                <div v-for="Engineer in EngineersSelected">
                    <Divider/>
                    <EngineerPanel :name="Engineer" />
                </div>
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
<script setup>
import { ref } from 'vue'
defineProps(['name'])
const result = defineModel(
    'result',
    {
        default:{rate:3, goodFeedback: '', badFeedback: ''}
    }
)
result.value = {rate:3, goodFeedback: '', badFeedback: ''}

</script>

<template>

    <el-form-item :label="`请为 ${name} 同学这个月整体打分`" >
            <el-rate v-model="result.rate" :texts="['不能接受', '有待改进', '一般情况', '不错', '完美!']" show-text />
    </el-form-item>

    <el-form-item label="你认为他这段时间有哪些地方做的可以提升？（最好有具体例子）">
        <el-input v-model="result.goodFeedback" type="textarea" />
    </el-form-item>
    <el-form-item label="你认为他这段时间那些地方做的很好值得表扬？（最好有具体例子）">
        <el-input v-model="result.badFeedback" type="textarea" />
    </el-form-item>

</template>
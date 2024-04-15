<script setup>
import { ref } from 'vue'
const rate = ref(3)

defineProps(['name'])
</script>

<template>

    <el-form-item :label="`请为 ${name} 同学这个月整体打分`" >
            <el-rate v-model="rate" :texts="['不能接受', '有待改进', '一般情况', '不错', '完美!']" show-text />
    </el-form-item>

    <el-form-item label="你认为他这段时间有哪些地方做的可以提升？（最好有具体例子）">
        <el-input type="textarea" />
    </el-form-item>
    <el-form-item label="你认为他这段时间那些地方做的很好值得表扬？（最好有具体例子）">
        <el-input type="textarea" />
    </el-form-item>

</template>
<script setup>
import {ref, onMounted, getCurrentInstance} from 'vue'

const props = defineProps(['feedbacker'])
const engineers = ref([])
const domain = getCurrentInstance().appContext.config.globalProperties.$domain
const engineersSelected = defineModel(
    'engineersSelected', {default: []}
)

onMounted(async () => {
    const params = {
        feedbacker: props.feedbacker,
    }

    const queryString = new URLSearchParams(params).toString()
    const resp = await fetch(domain + '/engineers?' + queryString)
    const json = await resp.json()
    engineers.value = json
})

</script>
<template>
    <el-select multiple v-model="engineersSelected">
        <el-option
        v-for="engineer in engineers"
        :key="engineer"
        :label="engineer"
        :value="engineer"
        />
    </el-select>
</template>
<template>
  <section class="panel">
    <h2>天气</h2>
    <a-table :columns="columns" :data-source="tripPlan.weather_info" row-key="date" :pagination="false" />
  </section>
</template>

<script setup lang="ts">
import type { TripPlan } from '../types'

defineProps<{ tripPlan: TripPlan }>()

const columns = [
  { title: '日期', dataIndex: 'date', key: 'date' },
  { title: '白天天气', dataIndex: 'day_weather', key: 'day_weather' },
  { title: '夜间天气', dataIndex: 'night_weather', key: 'night_weather' },
  { title: '白天气温', dataIndex: 'day_temp', key: 'day_temp', customRender: ({ text }: { text: number }) => `${text}°C` },
  { title: '夜间气温', dataIndex: 'night_temp', key: 'night_temp', customRender: ({ text }: { text: number }) => `${text}°C` },
]
</script>

<style scoped>
.panel {
  margin-bottom: 24px;
}

h2 {
  margin-bottom: 16px;
}
</style>

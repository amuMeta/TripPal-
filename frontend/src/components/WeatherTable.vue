<template>
  <section class="panel glass-panel">
    <div class="panel-head">
      <div class="kicker">Weather</div>
      <h2>天气概览</h2>
    </div>
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
  padding: 24px;
  border-radius: 28px;
}

.panel-head {
  margin-bottom: 18px;
}

.kicker {
  margin-bottom: 10px;
  color: var(--accent);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.14em;
}

h2 {
  margin: 0;
  font-size: 24px;
  letter-spacing: -0.03em;
}

:deep(.ant-table) {
  background: transparent;
}

:deep(.ant-table-container) {
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(148, 163, 184, 0.14);
}

:deep(.ant-table-thead > tr > th) {
  background: rgba(248, 250, 252, 0.92);
}
</style>

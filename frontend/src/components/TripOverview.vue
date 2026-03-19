<template>
  <section class="panel">
    <h2>行程概览</h2>
    <a-descriptions bordered :column="1">
      <a-descriptions-item label="目的地">{{ tripPlan.city }}</a-descriptions-item>
      <a-descriptions-item label="日期">{{ tripPlan.start_date }} 至 {{ tripPlan.end_date }}</a-descriptions-item>
      <a-descriptions-item label="天数">{{ tripPlan.days.length }} 天</a-descriptions-item>
      <a-descriptions-item label="建议">{{ tripPlan.overall_suggestions }}</a-descriptions-item>
    </a-descriptions>
  </section>
</template>

<script setup lang="ts">
import type { TripPlan } from '../types'

defineProps<{ tripPlan: TripPlan }>()
</script>

<style scoped>
.panel {
  margin-bottom: 24px;
}

h2 {
  margin-bottom: 16px;
}
</style>

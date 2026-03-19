<template>
  <section class="panel">
    <h2>预算明细</h2>
    <div class="budget-grid">
      <a-statistic title="景点" :value="tripPlan.budget?.total_attractions || 0" suffix="元" />
      <a-statistic title="酒店" :value="tripPlan.budget?.total_hotels || 0" suffix="元" />
      <a-statistic title="餐饮" :value="tripPlan.budget?.total_meals || 0" suffix="元" />
      <a-statistic title="交通" :value="tripPlan.budget?.total_transportation || 0" suffix="元" />
      <a-statistic class="total" title="合计" :value="tripPlan.budget?.total || 0" suffix="元" />
    </div>
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

.budget-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
}

.total {
  grid-column: 1 / -1;
}
</style>

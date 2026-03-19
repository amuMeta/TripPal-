<template>
  <section class="panel glass-panel">
    <div class="panel-head">
      <div class="kicker">Budget</div>
      <h2>预算分布</h2>
    </div>

    <div class="budget-grid">
      <div class="budget-card">
        <span>景点</span>
        <strong>{{ tripPlan.budget?.total_attractions || 0 }}</strong>
        <em>元</em>
      </div>
      <div class="budget-card">
        <span>酒店</span>
        <strong>{{ tripPlan.budget?.total_hotels || 0 }}</strong>
        <em>元</em>
      </div>
      <div class="budget-card">
        <span>餐饮</span>
        <strong>{{ tripPlan.budget?.total_meals || 0 }}</strong>
        <em>元</em>
      </div>
      <div class="budget-card">
        <span>交通</span>
        <strong>{{ tripPlan.budget?.total_transportation || 0 }}</strong>
        <em>元</em>
      </div>
    </div>

    <div class="total-card">
      <span>总预算</span>
      <strong>{{ tripPlan.budget?.total || 0 }} 元</strong>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { TripPlan } from '../types'

defineProps<{ tripPlan: TripPlan }>()
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

.budget-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.budget-card,
.total-card {
  padding: 18px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(148, 163, 184, 0.14);
}

.budget-card span,
.total-card span {
  display: block;
  margin-bottom: 8px;
  color: var(--text-tertiary);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.budget-card strong,
.total-card strong {
  font-size: 24px;
  letter-spacing: -0.03em;
}

.budget-card em {
  margin-left: 6px;
  color: var(--text-tertiary);
  font-style: normal;
}

.total-card {
  margin-top: 14px;
  background: linear-gradient(135deg, rgba(45, 109, 246, 0.08), rgba(255, 255, 255, 0.88));
}

@media (max-width: 640px) {
  .budget-grid {
    grid-template-columns: 1fr;
  }
}
</style>

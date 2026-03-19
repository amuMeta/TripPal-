<template>
  <section class="panel glass-panel">
    <div class="panel-head">
      <div>
        <div class="kicker">Overview</div>
        <h2>这次行程的整体轮廓</h2>
      </div>
    </div>

    <div class="summary-grid">
      <div class="summary-card">
        <span>目的地</span>
        <strong>{{ tripPlan.city }}</strong>
      </div>
      <div class="summary-card">
        <span>日期</span>
        <strong>{{ tripPlan.start_date }} 至 {{ tripPlan.end_date }}</strong>
      </div>
      <div class="summary-card">
        <span>时长</span>
        <strong>{{ tripPlan.days.length }} 天</strong>
      </div>
    </div>

    <div class="suggestion-box">
      <span>TripPal Suggestion</span>
      <p>{{ tripPlan.overall_suggestions }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { TripPlan } from '../types'

defineProps<{ tripPlan: TripPlan }>()
</script>

<style scoped>
.panel {
  padding: 26px;
  border-radius: 28px;
}

.panel-head {
  margin-bottom: 20px;
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
  font-size: 28px;
  letter-spacing: -0.03em;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.summary-card {
  padding: 18px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.14);
}

.summary-card span,
.suggestion-box span {
  display: block;
  margin-bottom: 8px;
  color: var(--text-tertiary);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.summary-card strong {
  font-size: 18px;
  line-height: 1.5;
}

.suggestion-box {
  padding: 20px 22px;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.82), rgba(240, 248, 255, 0.92));
  border: 1px solid rgba(148, 163, 184, 0.14);
}

.suggestion-box p {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.8;
}

@media (max-width: 760px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>

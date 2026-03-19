<template>
  <section class="panel glass-panel">
    <div class="panel-head">
      <div class="kicker">Itinerary</div>
      <h2>每日行程</h2>
    </div>

    <div v-for="(day, dayIndex) in tripPlan.days" :key="day.day_index" class="day-block">
      <div class="day-shell">
        <div class="day-top">
          <div>
            <span class="day-label">Day {{ day.day_index }}</span>
            <h3>{{ day.date }}</h3>
          </div>
          <a-tag color="blue">{{ day.transportation }}</a-tag>
        </div>

        <p class="day-description">{{ day.description }}</p>

        <div class="meta-row">
          <div class="meta-card">
            <span>住宿</span>
            <strong>{{ day.accommodation }}</strong>
          </div>
          <div v-if="day.hotel" class="meta-card hotel-card">
            <span>推荐酒店</span>
            <strong>{{ day.hotel.name }}</strong>
            <small>{{ day.hotel.address }} · {{ day.hotel.price_range }}</small>
          </div>
        </div>

        <div class="attraction-list">
          <div v-for="(item, index) in day.attractions" :key="`${item.name}-${index}`" class="attraction-card">
            <div class="attraction-copy">
              <strong>{{ item.name }}</strong>
              <span>{{ item.address }}</span>
              <p>{{ item.visit_duration }} 分钟 · {{ item.category || '景点' }}</p>
            </div>

            <div v-if="editMode" class="edit-actions">
              <a-button size="small" @click="$emit('move', dayIndex, index, -1)" :disabled="index === 0">上移</a-button>
              <a-button
                size="small"
                @click="$emit('move', dayIndex, index, 1)"
                :disabled="index === day.attractions.length - 1"
              >
                下移
              </a-button>
              <a-button size="small" danger @click="$emit('delete', dayIndex, index)">删除</a-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { TripPlan } from '../types'

defineProps<{
  tripPlan: TripPlan
  editMode: boolean
}>()

defineEmits<{
  move: [dayIndex: number, attractionIndex: number, direction: number]
  delete: [dayIndex: number, attractionIndex: number]
}>()
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

h2,
h3 {
  margin: 0;
}

h2 {
  font-size: 28px;
  letter-spacing: -0.03em;
}

.day-block + .day-block {
  margin-top: 16px;
}

.day-shell {
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(148, 163, 184, 0.14);
}

.day-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.day-label {
  display: inline-block;
  margin-bottom: 8px;
  color: var(--text-tertiary);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.day-description {
  margin: 14px 0 16px;
  color: var(--text-secondary);
  line-height: 1.8;
}

.meta-row {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 12px;
  margin-bottom: 18px;
}

.meta-card {
  padding: 16px;
  border-radius: 18px;
  background: #f8fbff;
}

.meta-card span {
  display: block;
  margin-bottom: 8px;
  color: var(--text-tertiary);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.hotel-card small {
  display: block;
  margin-top: 8px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.attraction-list {
  display: grid;
  gap: 12px;
}

.attraction-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  padding: 16px 18px;
  border-radius: 18px;
  background: rgba(246, 248, 251, 0.92);
}

.attraction-copy strong {
  display: block;
  margin-bottom: 6px;
}

.attraction-copy span,
.attraction-copy p {
  color: var(--text-secondary);
}

.attraction-copy p {
  margin: 8px 0 0;
}

.edit-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

@media (max-width: 760px) {
  .meta-row {
    grid-template-columns: 1fr;
  }

  .attraction-card {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>

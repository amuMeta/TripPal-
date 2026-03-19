<template>
  <section class="panel">
    <h2>每日行程</h2>
    <div v-for="(day, dayIndex) in tripPlan.days" :key="day.day_index" class="day-block">
      <a-card :title="`第 ${day.day_index} 天 (${day.date})`">
        <p>{{ day.description }}</p>
        <p>交通方式：{{ day.transportation }}</p>
        <p>住宿：{{ day.accommodation }}</p>

        <div v-if="day.hotel" class="hotel-box">
          <strong>{{ day.hotel.name }}</strong>
          <div>{{ day.hotel.address }}</div>
          <div>{{ day.hotel.price_range }} / 评分 {{ day.hotel.rating }}</div>
        </div>

        <a-list item-layout="horizontal" :data-source="day.attractions">
          <template #renderItem="{ item, index }">
            <a-list-item>
              <a-list-item-meta :title="item.name" :description="`${item.address} · ${item.visit_duration} 分钟`" />
              <div v-if="editMode" class="edit-actions">
                <a-button size="small" @click="$emit('move', dayIndex, index, -1)" :disabled="index === 0">上移</a-button>
                <a-button size="small" @click="$emit('move', dayIndex, index, 1)" :disabled="index === day.attractions.length - 1">下移</a-button>
                <a-button size="small" danger @click="$emit('delete', dayIndex, index)">删除</a-button>
              </div>
            </a-list-item>
          </template>
        </a-list>
      </a-card>
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
  margin-bottom: 24px;
}

h2 {
  margin-bottom: 16px;
}

.day-block {
  margin-bottom: 16px;
}

.hotel-box {
  margin: 12px 0;
  padding: 12px;
  background: #f6f8fb;
  border-radius: 10px;
}

.edit-actions {
  display: flex;
  gap: 8px;
}
</style>

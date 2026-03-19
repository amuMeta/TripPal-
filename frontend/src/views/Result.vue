<template>
  <div v-if="tripPlan" class="result-page">
    <a-card class="shell" title="旅行计划结果">
      <div class="action-row">
        <a-button type="primary" @click="toggleEditMode">{{ editMode ? '退出编辑' : '编辑行程' }}</a-button>
        <a-button @click="downloadPng">导出 PNG</a-button>
        <a-button @click="downloadPdf">导出 PDF</a-button>
      </div>

      <TripOverview :trip-plan="tripPlan" />
      <BudgetPanel :trip-plan="tripPlan" />
      <TripMap :trip-plan="tripPlan" />
      <DayPlanEditor
        :trip-plan="tripPlan"
        :edit-mode="editMode"
        @move="moveAttraction"
        @delete="deleteAttraction"
      />
      <WeatherTable :trip-plan="tripPlan" />
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BudgetPanel from '../components/BudgetPanel.vue'
import DayPlanEditor from '../components/DayPlanEditor.vue'
import TripMap from '../components/TripMap.vue'
import TripOverview from '../components/TripOverview.vue'
import WeatherTable from '../components/WeatherTable.vue'
import { useExport } from '../composables/useExport'
import { useTripResult } from '../composables/useTripResult'

const { tripPlan, editMode, toggleEditMode, moveAttraction, deleteAttraction } = useTripResult()
const { exportAsPNG, exportAsPDF } = useExport()

const exportBaseName = computed(() => {
  if (!tripPlan.value) return 'trip-plan'
  return `旅行计划_${tripPlan.value.city}_${tripPlan.value.start_date}`
})

const downloadPng = async () => {
  await exportAsPNG(`${exportBaseName.value}.png`)
}

const downloadPdf = async () => {
  await exportAsPDF(`${exportBaseName.value}.pdf`)
}
</script>

<style scoped>
.result-page {
  min-height: 100vh;
  padding: 24px 16px;
  background: #f3f5f7;
}

.shell {
  max-width: 1180px;
  margin: 0 auto;
  border-radius: 20px;
}

.action-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}
</style>

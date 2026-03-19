<template>
  <div v-if="tripPlan" class="result-page">
    <section class="result-hero glass-panel">
      <div class="hero-copy">
        <div class="eyebrow">TripPal Result</div>
        <h1>{{ tripPlan.city }} · {{ tripPlan.days.length }} 天行程已生成</h1>
        <p>
          保留整体节奏感，同时把预算、天气、行程和地图压缩成一份更适合浏览和调整的明亮视图。
        </p>
      </div>

      <div class="hero-actions">
        <a-button @click="backToPlanner">返回重新输入</a-button>
        <a-button type="primary" @click="toggleEditMode">{{ editMode ? '退出编辑' : '编辑行程' }}</a-button>
        <a-button @click="downloadPng">导出 PNG</a-button>
        <a-button @click="downloadPdf">导出 PDF</a-button>
      </div>
    </section>

    <div class="content-grid">
      <div class="main-column">
        <TripOverview :trip-plan="tripPlan" />
        <DayPlanEditor
          :trip-plan="tripPlan"
          :edit-mode="editMode"
          @move="moveAttraction"
          @delete="deleteAttraction"
        />
      </div>

      <aside class="side-column">
        <BudgetPanel :trip-plan="tripPlan" />
        <TripMap :trip-plan="tripPlan" />
        <WeatherTable :trip-plan="tripPlan" />
      </aside>
    </div>
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

const { tripPlan, editMode, toggleEditMode, moveAttraction, deleteAttraction, backToPlanner } = useTripResult()
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
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 20px 64px;
}

.result-hero {
  display: flex;
  justify-content: space-between;
  gap: 28px;
  padding: 28px 30px;
  border-radius: 32px;
  margin-bottom: 24px;
}

.eyebrow {
  margin-bottom: 12px;
  color: var(--accent);
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.hero-copy h1 {
  margin: 0 0 12px;
  font-size: clamp(30px, 5vw, 52px);
  line-height: 1.06;
  letter-spacing: -0.04em;
}

.hero-copy p {
  max-width: 720px;
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.8;
  font-size: 17px;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-content: flex-start;
  justify-content: flex-end;
  min-width: 280px;
}

.content-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 22px;
  align-items: start;
}

.main-column,
.side-column {
  display: grid;
  gap: 20px;
}

:deep(.ant-btn) {
  height: 46px;
  padding-inline: 18px;
  border-radius: 999px;
  border-color: rgba(148, 163, 184, 0.18);
  box-shadow: none;
}

:deep(.ant-btn-primary) {
  box-shadow: 0 14px 30px rgba(45, 109, 246, 0.2);
}

@media (max-width: 980px) {
  .result-hero,
  .content-grid {
    grid-template-columns: 1fr;
    display: grid;
  }

  .hero-actions {
    justify-content: flex-start;
    min-width: 0;
  }
}

@media (max-width: 640px) {
  .result-page {
    padding: 22px 14px 48px;
  }

  .result-hero {
    padding: 22px 18px;
  }
}
</style>

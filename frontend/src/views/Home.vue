<template>
  <div class="home-page">
    <section class="hero">
      <div class="hero-copy">
        <div class="eyebrow">TripPal</div>
        <h1>用更轻盈的方式，生成一份好看的旅行计划。</h1>
        <p>
          从城市、日期到预算与偏好，TripPal 会把这些信息整理成一份明亮、清晰、可编辑的行程结果。
        </p>
        <div class="hero-meta">
          <div class="meta-pill">城市灵感</div>
          <div class="meta-pill">预算视图</div>
          <div class="meta-pill">路线整理</div>
        </div>
      </div>

      <div class="preview-card glass-panel">
        <div class="preview-top">
          <span>推荐节奏</span>
          <strong>3 天轻旅行</strong>
        </div>
        <div class="preview-list">
          <div class="preview-item">
            <span>Day 1</span>
            <p>城市地标、经典午餐、傍晚夜游</p>
          </div>
          <div class="preview-item">
            <span>Day 2</span>
            <p>博物馆、步行路线、氛围晚餐</p>
          </div>
          <div class="preview-item">
            <span>Day 3</span>
            <p>公园放松、手信采购、返程建议</p>
          </div>
        </div>
      </div>
    </section>

    <section class="planner-shell glass-panel">
      <div class="planner-head">
        <div>
          <div class="section-kicker">Plan Builder</div>
          <h2>开始定制你的下一次出行</h2>
        </div>
        <div class="head-note">明亮、克制、可直接生成</div>
      </div>

      <a-form :model="form" layout="vertical" @submit.prevent="handleSubmit">
        <div class="layout-grid">
          <div class="main-form">
            <a-form-item label="目的地城市" required>
              <a-input v-model:value="form.city" size="large" placeholder="例如：上海、杭州、厦门" />
            </a-form-item>

            <div class="date-grid">
              <a-form-item label="出发日期" required>
                <a-input v-model:value="form.start_date" size="large" type="date" />
              </a-form-item>
              <a-form-item label="结束日期" required>
                <a-input v-model:value="form.end_date" size="large" type="date" />
              </a-form-item>
            </div>

            <a-form-item label="偏好描述">
              <a-textarea
                v-model:value="form.preferences"
                :rows="5"
                placeholder="例如：艺术馆、美食街、海边步行、适合拍照、节奏轻松"
              />
            </a-form-item>
          </div>

          <div class="side-form">
            <a-form-item label="旅行天数">
              <a-input-number v-model:value="form.days" :min="1" :max="14" class="full-width" size="large" />
            </a-form-item>

            <a-form-item label="预算档位">
              <a-select v-model:value="form.budget" size="large">
                <a-select-option value="经济型">经济型</a-select-option>
                <a-select-option value="舒适型">舒适型</a-select-option>
                <a-select-option value="豪华型">豪华型</a-select-option>
              </a-select>
            </a-form-item>

            <a-form-item label="交通方式">
              <a-select v-model:value="form.transportation" size="large">
                <a-select-option value="公共交通">公共交通</a-select-option>
                <a-select-option value="打车">打车</a-select-option>
                <a-select-option value="自驾">自驾</a-select-option>
              </a-select>
            </a-form-item>

            <a-form-item label="住宿类型">
              <a-select v-model:value="form.accommodation" size="large">
                <a-select-option value="经济酒店">经济酒店</a-select-option>
                <a-select-option value="中档酒店">中档酒店</a-select-option>
                <a-select-option value="高档酒店">高档酒店</a-select-option>
              </a-select>
            </a-form-item>
          </div>
        </div>

        <a-alert v-if="errorMessage" type="error" :message="errorMessage" show-icon class="error-alert" />

        <div class="submit-row">
          <div class="submit-copy">
            <strong>生成结果后可继续编辑、导出，并返回重新规划。</strong>
            <span>推荐使用真实高德 Key 获得完整地图体验。</span>
          </div>
          <a-button class="submit-button" type="primary" size="large" :loading="loading" @click="handleSubmit">
            生成旅行计划
          </a-button>
        </div>
      </a-form>

      <div v-if="loading" class="progress-box">
        <div class="progress-head">
          <strong>{{ loadingStatusText }}</strong>
          <span>{{ loadingProgress }}%</span>
        </div>
        <a-progress :percent="loadingProgress" :show-info="false" stroke-linecap="round" />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTripPlanner } from '../composables/useTripPlanner'

const { form, loading, loadingProgress, loadingStatusText, submit } = useTripPlanner()
const errorMessage = ref('')

const handleSubmit = async () => {
  errorMessage.value = ''

  if (!form.city.trim()) {
    errorMessage.value = '请填写目的地城市'
    return
  }

  if (!form.start_date || !form.end_date) {
    errorMessage.value = '请填写出发和结束日期'
    return
  }

  if (form.end_date < form.start_date) {
    errorMessage.value = '结束日期不能早于出发日期'
    return
  }

  try {
    await submit()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '生成行程失败，请稍后重试'
  }
}
</script>

<style scoped>
.home-page {
  position: relative;
  max-width: 1220px;
  margin: 0 auto;
  padding: 48px 20px 72px;
}

.hero {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 24px;
  align-items: stretch;
  margin-bottom: 28px;
}

.hero-copy {
  padding: 18px 4px;
}

.eyebrow,
.section-kicker {
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 12px;
}

.hero h1 {
  max-width: 760px;
  margin: 0 0 16px;
  font-size: clamp(36px, 6vw, 64px);
  line-height: 1.04;
  letter-spacing: -0.04em;
}

.hero p {
  max-width: 620px;
  margin: 0;
  font-size: 18px;
  line-height: 1.75;
  color: var(--text-secondary);
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 22px;
}

.meta-pill {
  padding: 10px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(15, 23, 42, 0.08);
  color: var(--text-secondary);
}

.preview-card {
  padding: 24px;
  border-radius: var(--radius-xl);
}

.preview-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  color: var(--text-secondary);
}

.preview-top strong {
  color: var(--text-primary);
  font-size: 18px;
}

.preview-list {
  display: grid;
  gap: 14px;
}

.preview-item {
  padding: 16px 18px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(148, 163, 184, 0.15);
}

.preview-item span {
  display: inline-block;
  margin-bottom: 8px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-tertiary);
}

.preview-item p {
  margin: 0;
  color: var(--text-primary);
  line-height: 1.6;
}

.planner-shell {
  padding: 28px;
  border-radius: 32px;
}

.planner-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 28px;
}

.planner-head h2 {
  margin: 0;
  font-size: 28px;
  letter-spacing: -0.03em;
}

.head-note {
  color: var(--text-tertiary);
}

.layout-grid {
  display: grid;
  grid-template-columns: 1.35fr 0.85fr;
  gap: 22px;
}

.main-form,
.side-form {
  padding: 4px 0;
}

.date-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.full-width {
  width: 100%;
}

.error-alert {
  margin-top: 12px;
  margin-bottom: 12px;
  border-radius: 16px;
}

.submit-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-top: 12px;
}

.submit-copy {
  display: grid;
  gap: 6px;
}

.submit-copy strong {
  font-size: 15px;
}

.submit-copy span {
  color: var(--text-tertiary);
}

.submit-button {
  min-width: 220px;
  height: 52px;
  border-radius: 999px;
  box-shadow: 0 14px 30px rgba(45, 109, 246, 0.22);
}

.progress-box {
  margin-top: 24px;
  padding: 18px 20px;
  border-radius: 22px;
  background: rgba(248, 250, 252, 0.92);
  border: 1px solid rgba(148, 163, 184, 0.16);
}

.progress-head {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

:deep(.ant-card) {
  border: none;
}

:deep(.ant-card-head) {
  display: none;
}

:deep(.ant-form-item-label > label) {
  color: var(--text-secondary);
  font-weight: 500;
}

:deep(.ant-input),
:deep(.ant-input-number),
:deep(.ant-input-number .ant-input-number-input),
:deep(.ant-select-selector),
:deep(.ant-input-affix-wrapper),
:deep(textarea.ant-input) {
  border-radius: 18px !important;
  border-color: rgba(148, 163, 184, 0.22) !important;
  box-shadow: none !important;
}

:deep(.ant-input),
:deep(.ant-input-number),
:deep(.ant-select-selector),
:deep(textarea.ant-input) {
  min-height: 48px;
  background: rgba(255, 255, 255, 0.86) !important;
}

@media (max-width: 980px) {
  .hero,
  .layout-grid {
    grid-template-columns: 1fr;
  }

  .planner-head,
  .submit-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .submit-button {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .home-page {
    padding: 24px 14px 54px;
  }

  .planner-shell {
    padding: 20px;
  }

  .date-grid {
    grid-template-columns: 1fr;
  }
}
</style>

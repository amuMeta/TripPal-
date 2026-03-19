<template>
  <div class="page">
    <a-card class="card" title="智能旅行助手">
      <a-form :model="form" layout="vertical" @submit.prevent="handleSubmit">
        <a-form-item label="目的地城市" required>
          <a-input v-model:value="form.city" placeholder="例如：北京、上海、杭州" />
        </a-form-item>

        <div class="date-grid">
          <a-form-item label="出发日期" required>
            <a-input v-model:value="form.start_date" type="date" />
          </a-form-item>
          <a-form-item label="结束日期" required>
            <a-input v-model:value="form.end_date" type="date" />
          </a-form-item>
        </div>

        <a-form-item label="旅行天数">
          <a-input-number v-model:value="form.days" :min="1" :max="14" class="full-width" />
        </a-form-item>

        <a-form-item label="偏好">
          <a-textarea v-model:value="form.preferences" :rows="4" placeholder="例如：历史文化、美食、轻松步行、拍照" />
        </a-form-item>

        <div class="triple-grid">
          <a-form-item label="预算档位">
            <a-select v-model:value="form.budget">
              <a-select-option value="经济型">经济型</a-select-option>
              <a-select-option value="舒适型">舒适型</a-select-option>
              <a-select-option value="豪华型">豪华型</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="交通方式">
            <a-select v-model:value="form.transportation">
              <a-select-option value="公共交通">公共交通</a-select-option>
              <a-select-option value="打车">打车</a-select-option>
              <a-select-option value="自驾">自驾</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="住宿类型">
            <a-select v-model:value="form.accommodation">
              <a-select-option value="经济酒店">经济酒店</a-select-option>
              <a-select-option value="中档酒店">中档酒店</a-select-option>
              <a-select-option value="高档酒店">高档酒店</a-select-option>
            </a-select>
          </a-form-item>
        </div>

        <a-alert v-if="errorMessage" type="error" :message="errorMessage" show-icon class="error-alert" />

        <a-button type="primary" :loading="loading" block @click="handleSubmit">
          生成行程
        </a-button>
      </a-form>

      <div v-if="loading" class="progress-box">
        <a-progress :percent="loadingProgress" />
        <div class="status">{{ loadingStatusText }}</div>
      </div>
    </a-card>
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
.page {
  min-height: 100vh;
  padding: 32px 16px;
  background: linear-gradient(160deg, #f4efe6 0%, #e6eef7 100%);
}

.card {
  max-width: 880px;
  margin: 0 auto;
  border-radius: 20px;
}

.date-grid,
.triple-grid {
  display: grid;
  gap: 16px;
}

.date-grid {
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.triple-grid {
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.full-width {
  width: 100%;
}

.progress-box {
  margin-top: 20px;
}

.status {
  margin-top: 8px;
  color: #595959;
}

.error-alert {
  margin-bottom: 16px;
}
</style>

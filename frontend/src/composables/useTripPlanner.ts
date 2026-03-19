import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { generateTripPlan } from '../services/api'
import { saveTripPlan } from '../services/tripStorage'
import type { TripPlanRequest } from '../types'

const statusMessages = [
  '正在检索城市景点',
  '正在整理天气信息',
  '正在匹配住宿方案',
  '正在生成每日行程',
  '正在补充展示素材',
]

export const useTripPlanner = () => {
  const router = useRouter()

  const form = reactive({
    city: '',
    start_date: '',
    end_date: '',
    days: 3,
    preferences: '',
    budget: '舒适型',
    transportation: '公共交通',
    accommodation: '中档酒店',
  })

  const loading = ref(false)
  const loadingProgress = ref(0)
  const loadingStatusText = ref('')
  let timer: ReturnType<typeof setInterval> | null = null

  const stopProgress = () => {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  const startProgress = () => {
    // The loading bar is intentionally simulated because itinerary generation
    // may combine multiple slow backend stages without streaming progress.
    stopProgress()
    loadingProgress.value = 0
    loadingStatusText.value = statusMessages[0]

    let step = 0
    timer = setInterval(() => {
      step += 1
      loadingProgress.value = Math.min(step * 18, 90)
      loadingStatusText.value = statusMessages[Math.min(step, statusMessages.length - 1)]
    }, 800)
  }

  const submit = async () => {
    if (!form.city || !form.start_date || !form.end_date) {
      throw new Error('请填写城市和出发日期')
    }

    const payload: TripPlanRequest = {
      ...form,
      days: Number(form.days),
    }

    loading.value = true
    startProgress()

    try {
      const tripPlan = await generateTripPlan(payload)
      // Persist the latest result so the result page can be a pure route
      // transition instead of carrying a large object in router params.
      saveTripPlan(tripPlan)
      loadingProgress.value = 100
      loadingStatusText.value = '行程生成完成'
      await router.push({ name: 'Result' })
    } finally {
      stopProgress()
      loading.value = false
    }
  }

  return {
    form,
    loading,
    loadingProgress,
    loadingStatusText,
    submit,
  }
}

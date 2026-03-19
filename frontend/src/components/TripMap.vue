<template>
  <section class="panel">
    <h2>地图</h2>
    <div id="map-container" class="map-container"></div>
    <p v-if="!amapKey" class="tip">未配置高德地图 Key，地图功能已降级。</p>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import type { TripPlan } from '../types'

const props = defineProps<{ tripPlan: TripPlan }>()
const amapKey = import.meta.env.VITE_AMAP_WEB_KEY || ''

declare global {
  interface Window {
    AMap?: any
  }
}

const createMap = () => {
  if (!window.AMap) return

  const map = new window.AMap.Map('map-container', {
    center: [116.397428, 39.90923],
    zoom: 11,
  })

  props.tripPlan.days.forEach((day) => {
    day.attractions.forEach((attraction) => {
      const position: [number, number] = [attraction.location.longitude, attraction.location.latitude]
      const marker = new window.AMap.Marker({
        position,
        title: attraction.name,
        map,
      })

      const infoWindow = new window.AMap.InfoWindow({
        content: `
          <div style="padding: 10px;">
            <h3>${attraction.name}</h3>
            <p>${attraction.address}</p>
            <p>游览时长：${attraction.visit_duration} 分钟</p>
            <p>门票：${attraction.ticket_price} 元</p>
          </div>
        `,
        offset: new window.AMap.Pixel(0, -30),
      })

      marker.on('click', () => {
        infoWindow.open(map, marker.getPosition())
      })
    })
  })

  map.setFitView()
}

const initMap = () => {
  if (!amapKey) return

  if (window.AMap) {
    createMap()
    return
  }

  const script = document.createElement('script')
  script.src = `https://webapi.amap.com/maps?v=2.0&key=${amapKey}`
  script.onload = createMap
  document.head.appendChild(script)
}

onMounted(initMap)
</script>

<style scoped>
.panel {
  margin-bottom: 24px;
}

h2 {
  margin-bottom: 16px;
}

.map-container {
  width: 100%;
  height: 420px;
  border-radius: 12px;
  overflow: hidden;
}

.tip {
  margin-top: 12px;
  color: #8c8c8c;
}
</style>

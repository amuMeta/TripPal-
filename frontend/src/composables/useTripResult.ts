import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { clearTripPlan, loadTripPlan } from '../services/tripStorage'
import type { TripPlan } from '../types'

export const useTripResult = () => {
  const router = useRouter()
  const tripPlan = ref<TripPlan | null>(loadTripPlan())
  const editMode = ref(false)

  if (!tripPlan.value) {
    void router.replace({ name: 'Home' })
  }

  const toggleEditMode = () => {
    editMode.value = !editMode.value
  }

  const moveAttraction = (dayIndex: number, attractionIndex: number, direction: number) => {
    const day = tripPlan.value?.days[dayIndex]
    if (!day) return

    const newIndex = attractionIndex + direction
    if (newIndex < 0 || newIndex >= day.attractions.length) return

    const next = [...day.attractions]
    ;[next[attractionIndex], next[newIndex]] = [next[newIndex], next[attractionIndex]]
    day.attractions = next
  }

  const deleteAttraction = (dayIndex: number, attractionIndex: number) => {
    const day = tripPlan.value?.days[dayIndex]
    if (!day) return
    day.attractions = day.attractions.filter((_, index) => index !== attractionIndex)
  }

  const backToPlanner = async () => {
    // Clear stale itinerary data before returning so the home page always
    // starts a fresh planning flow instead of depending on previous state.
    clearTripPlan()
    await router.push({ name: 'Home' })
  }

  return {
    tripPlan,
    editMode,
    toggleEditMode,
    moveAttraction,
    deleteAttraction,
    backToPlanner,
  }
}

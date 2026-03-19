import type { TripPlan } from '../types'

const STORAGE_KEY = 'smart-trip-plan'

export const saveTripPlan = (tripPlan: TripPlan) => {
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(tripPlan))
}

export const loadTripPlan = (): TripPlan | null => {
  const raw = sessionStorage.getItem(STORAGE_KEY)
  if (!raw) {
    return null
  }

  try {
    return JSON.parse(raw) as TripPlan
  } catch {
    sessionStorage.removeItem(STORAGE_KEY)
    return null
  }
}

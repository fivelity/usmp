import { writable, derived } from "svelte/store"

// Core sensor data store
export const sensorData = writable({})

// Derived stores for organized access
export const sensorsByCategory = derived(sensorData, ($sensorData) => {
  const categories = {}

  Object.values($sensorData).forEach((sensor) => {
    if (!categories[sensor.category]) {
      categories[sensor.category] = []
    }
    categories[sensor.category].push(sensor)
  })

  return categories
})

export const activeSensors = derived(sensorData, ($sensorData) => {
  return Object.values($sensorData).filter((sensor) => sensor.value !== null && sensor.value !== undefined)
})

// Utility functions
export const sensorUtils = {
  updateSensorData: (newData) => {
    sensorData.set(newData)
  },

  getSensorById: (id) => {
    let data
    sensorData.subscribe((value) => (data = value))()
    return data[id] || null
  },

  clearSensorData: () => {
    sensorData.set({})
  },
}

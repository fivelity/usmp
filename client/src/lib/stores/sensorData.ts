import type { SensorData, SensorSource, SensorSourceFromAPI, SensorInfo } from '$lib/types'

// Sensor state management using Svelte 5 runes
export let sensorData = $state<Record<string, SensorData>>({})
export let sensorSources = $state<SensorSource[]>([])
export let availableSensors = $state<SensorInfo[]>([])
export let hardwareTree = $state<any[]>([])

// Derived state
export let activeSensors = $derived(() => 
  Object.values(sensorData).filter(sensor => sensor.value !== undefined)
)

export let sensorCategories = $derived(() => {
  const categories = new Set<string>()
  Object.values(sensorData).forEach(sensor => {
    if (sensor.category) {
      categories.add(sensor.category)
    }
  })
  return Array.from(categories)
})

// Sensor utilities
export const sensorUtils = {
  updateSensorData(data: Record<string, SensorData>) {
    sensorData = data
  },

  updateSensorSources(apiPayload: Record<string, SensorSourceFromAPI> | null | undefined) {
    const newAvailableSensors: SensorInfo[] = []
    const newSensorSources: SensorSource[] = []

    if (apiPayload && typeof apiPayload === "object") {
      const sourcesFromAPIArray: SensorSourceFromAPI[] = Object.values(apiPayload)

      for (const sourceAPI of sourcesFromAPIArray) {
        if (sourceAPI && sourceAPI.active && sourceAPI.sensors && typeof sourceAPI.sensors === "object") {
          const currentSourceSensors: SensorData[] = []
          for (const sensor_data_item of Object.values(sourceAPI.sensors)) {
            if (sensor_data_item) {
              newAvailableSensors.push({
                id: sensor_data_item.id,
                name: sensor_data_item.name,
                category: sensor_data_item.category,
                unit: sensor_data_item.unit,
                source: sourceAPI.id,
              })
              currentSourceSensors.push(sensor_data_item)
            }
          }
          newSensorSources.push({
            id: sourceAPI.id,
            name: sourceAPI.name,
            active: sourceAPI.active,
            sensors: currentSourceSensors,
            last_update: sourceAPI.last_update,
            error_message: sourceAPI.error_message,
          })
        } else if (sourceAPI) {
          newSensorSources.push({
            id: sourceAPI.id,
            name: sourceAPI.name,
            active: sourceAPI.active,
            sensors: [],
            last_update: sourceAPI.last_update,
            error_message: sourceAPI.error_message,
          })
        }
      }
    }

    sensorSources = newSensorSources
    availableSensors = newAvailableSensors
  },

  updateHardwareTree(tree: any[] | any) {
    const treeArray = Array.isArray(tree) ? tree : tree ? [tree] : []
    hardwareTree = treeArray
  },

  getSensorById(id: string): SensorData | undefined {
    return sensorData[id]
  },

  getSensorsByCategory(category: string): SensorData[] {
    return Object.values(sensorData).filter(sensor => sensor.category === category)
  },

  getSensorsBySource(sourceId: string): SensorData[] {
    return Object.values(sensorData).filter(sensor => sensor.source === sourceId)
  }
} 
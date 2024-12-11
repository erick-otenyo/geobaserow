<template functional>
    <div v-if="props.value" class="card-text">
        {{ $options.methods.formatGeojsonValue(props.value) }}
    </div>
  </template>
  
  <script>
import { geojsonToWKT } from '@geobaserow/utils'
export default {
    height: 16,
    functional: true,
    methods: {
        formatGeojsonValue(value) {
            return geojsonToWKT(value)
        },
    },
}
</script>
  
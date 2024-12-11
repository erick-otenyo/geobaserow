<template functional>
  <div
      class="grid-view__cell grid-field-point__cell"
  >
    <client-only>
      <div v-if="props.value" class="grid-field-text">
        {{ $options.methods.formatGeojsonValue(props.value) }}
      </div>
    </client-only>
  </div>
</template>

<script>
import { geojsonToWKT } from '@geobaserow/utils'

export default {
  name: 'FunctionalGridViewFieldPoint',
  functional: true,
  methods: {
    formatGeojsonValue(value) {
      return geojsonToWKT(value)
    },
  },
}
</script>
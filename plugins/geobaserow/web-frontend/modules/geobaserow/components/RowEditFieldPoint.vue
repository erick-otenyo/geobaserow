<template>
  <div class="control__elements">
    <div class="field-point">
      <client-only>
      <l-map :zoom=13 :center="latLng || center" @click="addOrMovePoint">
        <l-tile-layer :url="url"></l-tile-layer>
        <l-marker v-if="latLng" :lat-lng="latLng"></l-marker>
      </l-map>
    </client-only>
    </div>
  </div>
</template>

<script>
import rowEditField from '@baserow/modules/database/mixins/rowEditField'

export default {
  mixins: [rowEditField],
  data() {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: [51.505, -0.159],
    };
  },
  computed: {
    latLng() {
      if (this.value && this.value.coordinates) {
        return { lng: this.value.coordinates[0], lat: this.value.coordinates[1] }
      }
      return null
    }
  },
  methods: {
    addOrMovePoint(value) {
      if (this.readOnly) {
        return
      }

      const point = {
        "type": "Point",
        "coordinates": [value.latlng.lng, value.latlng.lat],
      }

      this.$emit('update', point, this.value)
    },
  }
}
</script>

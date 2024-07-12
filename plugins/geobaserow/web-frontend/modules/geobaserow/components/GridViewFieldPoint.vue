<template>
  <div
      ref="cell"
      class="grid-view__cell grid-field-point__cell active"
      :class="{ editing: editing }"
      @contextmenu="stopContextIfEditing($event)"
  >
    <client-only>
      <l-map :zoom=13 :center="latLng || center" @click="addOrMovePoint">
        <l-tile-layer :url="url"></l-tile-layer>
        <l-marker v-if="latLng" :lat-lng="latLng"></l-marker>
      </l-map>
    </client-only>
  </div>
</template>

<script>
import gridField from '@baserow/modules/database/mixins/gridField'
import gridFieldInput from '@baserow/modules/database/mixins/gridFieldInput'

export default {
  mixins: [gridField, gridFieldInput],
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

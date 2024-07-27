<template>
  <Map
      :tile-url="tilesUrl"

  />
</template>

<script>


import viewHelpers from '@baserow/modules/database/mixins/viewHelpers'
import {mapGetters} from 'vuex'

import Map from '@geobaserow/components/Map.vue';


export default {
  name: 'MapView',
  mixins: [viewHelpers],
  components: {
    Map,
  },
  props: {
    fields: {
      type: Array,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    database: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
    storePrefix: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showHiddenFieldsInRowModal: false,
    }
  },
  computed: {
    hiddenFields() {
      return this.fields
          .filter(filterHiddenFieldsFunction(this.fieldOptions))
          .sort(sortFieldsByOrderAndIdFunction(this.fieldOptions))
    },
    tilesUrl() {
      const baseUrl = this.$client.defaults.baseURL
      return baseUrl + `/database/views/map/${this.view.id}/tiles/{z}/{x}/{y}/`
    }
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        fieldOptions:
            this.$options.propsData.storePrefix +
            'view/map/getAllFieldOptions',
        getGeoField:
            this.$options.propsData.storePrefix + 'view/map/getGeoField',
      }),
    }
  },
  mounted() {
    console.log(this.tilesUrl)
  },
  methods: {},
}
</script>
<template>
    <div>Hello Map</div>
  </template>
  
  <script>


import viewHelpers from '@baserow/modules/database/mixins/viewHelpers'
import { mapGetters } from 'vuex'
import { populateRow } from '@baserow/modules/database/store/view/grid'
import { clone } from '@baserow/modules/core/utils/object'


export default {
    name: 'MapView',
    mixins: [viewHelpers],
    props: {
        primary: {
            type: Object,
            required: true,
        },
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
            selectedRow: null,
        }
    },
    computed: {
        hiddenFields() {
            return this.fields
                .filter(filterHiddenFieldsFunction(this.fieldOptions))
                .sort(sortFieldsByOrderAndIdFunction(this.fieldOptions))
        },
    },
    beforeCreate() {
        this.$options.computed = {
            ...(this.$options.computed || {}),
            ...mapGetters({
                allRows:
                    this.$options.propsData.storePrefix + 'view/map/getAllRows',
                fieldOptions:
                    this.$options.propsData.storePrefix +
                    'view/map/getAllFieldOptions',
                getGeoField:
                    this.$options.propsData.storePrefix + 'view/calendar/getGeoField',
            }),
        }
    },
    methods: {
    },
}
</script>
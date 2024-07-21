<template>
  <ul v-if="!tableLoading" class="header__filter header__filter--full-width">
    <li class="header__filter-item">
      <a
        class="header__filter-link"
        :class="!canChooseGeoField ? 'header__filter-link--disabled' : ''"
        @click="showChooseGeoFieldModal"
      >
        <i class="header__filter-icon iconoir-settings"></i>
        <span class="header__filter-name">
          {{ selectGeoFieldLinkText }}
        </span>
      </a>
      <SelectGeoFieldModal
        ref="selectGeoFieldModal"
        :view="view"
        :table="table"
        :fields="fields"
        :database="database"
        :geo-field-id="geoFieldId(fields)"
        @refresh="$emit('refresh', $event)"
      >
      </SelectGeoFieldModal>
    </li>
    <li v-if="geoFieldId(fields) != null" class="header__filter-item">
      <a
        ref="customizeContextLink"
        class="header__filter-link"
        @click="
          $refs.customizeContext.toggle(
            $refs.customizeContextLink,
            'bottom',
            'left',
            4
          )
          "
      >
        <i class="header__filter-icon iconoir-list"></i>
        <span class="header__filter-name">{{
          $t('mapViewHeader.labels')
        }}</span>
      </a>
      <ViewFieldsContext
        ref="customizeContext"
        :database="database"
        :view="view"
        :fields="fields"
        :field-options="fieldOptions"
        :allow-cover-image-field="false"
        @update-all-field-options="updateAllFieldOptions"
        @update-field-options-of-field="updateFieldOptionsOfField"
        @update-order="orderFieldOptions"
      ></ViewFieldsContext>
    </li>
    <li class="header__filter-item header__filter-item--right">
      <ViewSearch
        :view="view"
        :fields="fields"
        :store-prefix="storePrefix"
        :always-hide-rows-not-matching-search="true"
        @refresh="$emit('refresh', $event)"
      ></ViewSearch>
    </li>
  </ul>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import { notifyIf } from '@baserow/modules/core/utils/error'
import SelectGeoFieldModal from '@geobaserow/components/views/map/SelectGeoFieldModal'
import ViewFieldsContext from '@baserow/modules/database/components/view/ViewFieldsContext'
import ViewSearch from '@baserow/modules/database/components/view/ViewSearch'

export default {
  name: 'MapViewHeader',
  components: {
    ViewFieldsContext,
    SelectGeoFieldModal,
    ViewSearch,
  },
  props: {
    storePrefix: {
      type: String,
      required: true,
      default: '',
    },
    database: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    selectGeoFieldLinkText() {
      const df = this.getGeoField(this.fields)
      if (
        !df ||
        this.$registry.get('field', df.type).canRepresentGeo && this.$registry.get('field', df.type).canRepresentGeo() === false
      ) {
        return this.$t('mapViewHeader.displayBy')
      } else {
        return this.$t('mapViewHeader.displayedBy', {
          fieldName: this.displayedByFieldName,
        })
      }
    },
    displayedByFieldName() {
      for (let i = 0; i < this.fields.length; i++) {
        if (this.fields[i].id === this.view.geo_field) {
          return this.fields[i].name
        }
      }
      return ''
    },
    isDev() {
      return process.env.NODE_ENV === 'development'
    },
    ...mapState({
      tableLoading: (state) => state.table.loading,
    }),
    canChooseGeoField() {
      return (
        !this.readOnly &&
        this.$hasPermission(
          'database.table.view.update',
          this.view,
          this.database.workspace.id
        )
      )
    },
  },
  watch: {
    fields() {
      const df = this.getGeoField(this.fields)
      if (
        !df ||
        this.$registry.get('field', df.type).canRepresentGeo && this.$registry.get('field', df.type).canRepresentGeo()
      ) {
        this.showChooseGeoFieldModal()
      }
    },
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        fieldOptions:
          this.$options.propsData.storePrefix +
          'view/map/getAllFieldOptions',
        geoFieldId:
          this.$options.propsData.storePrefix +
          'view/map/getGeoFieldIdIfNotTrashed',
        getGeoField:
          this.$options.propsData.storePrefix + 'view/map/getGeoField',
      }),
    }
  },
  mounted() {
    if (this.geoFieldId(this.fields) == null) {
      this.showChooseGeoFieldModal()
    }
  },
  methods: {
    showChooseGeoFieldModal() {
      if (this.canChooseGeoField) {
        this.$refs.selectGeoFieldModal.show()
      }
    },
    async updateAllFieldOptions({ newFieldOptions, oldFieldOptions }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/map/updateAllFieldOptions',
          {
            newFieldOptions,
            oldFieldOptions,
            readOnly:
              this.readOnly ||
              !this.$hasPermission(
                'database.table.view.update_field_options',
                this.view,
                this.database.workspace.id
              ),
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async updateFieldOptionsOfField({ field, values, oldValues }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/map/updateFieldOptionsOfField',
          {
            field,
            values,
            oldValues,
            readOnly:
              this.readOnly ||
              !this.$hasPermission(
                'database.table.view.update_field_options',
                this.view,
                this.database.workspace.id
              ),
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async orderFieldOptions({ order }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/map/updateFieldOptionsOrder',
          {
            order,
            readOnly: this.readOnly,
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
  },
}
</script>

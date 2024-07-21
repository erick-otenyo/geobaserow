<template>
  <Modal>
    <h2 class="box__title">
      {{ $t('selectGeoFieldModal.chooseGeoField') }}
    </h2>
    <Error :error="error"></Error>
    <GeoFieldSelectForm
      ref="geoFieldSelectForm"
      :geo-fields="geoFields"
      :geo-field-id="geoFieldId"
      :table="table"
      @submitted="submitted"
    >
      <div class="actions">
        <div class="align-right">
          <Button
            type="primary"
            :loading="loading"
            :disabled="loading"
            size="large"
          >
            {{ $t('selectGeoFieldModal.save') }}</Button
          >
        </div>
      </div>
    </GeoFieldSelectForm>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import GeoFieldSelectForm from '@geobaserow/components/views/map/GeoFieldSelectForm'

export default {
  name: 'SelectGeoFieldModal',
  components: {
    GeoFieldSelectForm,
  },
  mixins: [modal, error],
  props: {
    view: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    database: {
      type: Object,
      required: true,
    },
    geoFieldId: {
      type: Number,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  computed: {
    geoFields() {
      return this.fields.filter((f) => {
        const field = this.$registry.get('field', f.type)
        return field.canRepresentGeo && field.canRepresentGeo()
      })
    },
  },
  methods: {
    async submitted(values) {
      this.loading = true
      this.hideError()
      const view = this.view
      this.$store.dispatch('view/setItemLoading', { view, value: true })
      try {
        await this.$store.dispatch('view/update', {
          view,
          values: { geo_field: values.geoFieldId },
        })
        this.$emit('refresh', {
          includeFieldOptions: true,
        })
        this.hide()
      } catch (error) {
        this.handleError(error)
      } finally {
        this.loading = false
        this.$store.dispatch('view/setItemLoading', { view, value: false })
      }
    },
  },
}
</script>

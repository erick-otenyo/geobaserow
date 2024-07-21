<template>
  <div>
    <form v-if="geoFields.length > 0" @submit.prevent="submit">
      <FormGroup
        :label="$t('geoFieldSelectForm.geoField')"
        small-label
        :error="fieldHasErrors('geoFieldId')"
        required
      >
        <Dropdown v-model="values.geoFieldId" :show-search="true">
          <DropdownItem
            v-for="geoField in geoFields"
            :key="geoField.id"
            :name="geoField.name"
            :value="geoField.id"
            :icon="fieldIcon(geoField.type)"
          >
          </DropdownItem>
        </Dropdown>

        <template #error>
          {{ $t('error.requiredField') }}
        </template>
      </FormGroup>
      <slot></slot>
    </form>
    <div v-else class="warning">
      {{ $t('geoFieldSelectForm.noCompatibleGeoFields') }}
    </div>
  </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators'
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'GeoFieldSelectForm',
  mixins: [form],
  props: {
    table: {
      type: Object,
      required: true,
    },
    geoFields: {
      type: Array,
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
      values: {
        geoFieldId: null,
      },
    }
  },
  mounted() {
    this.values.geoFieldId =
      this.geoFieldId || (this.geoFields.length > 0 && this.geoFields[0]?.id)
  },
  methods: {
    fieldIcon(type) {
      const ft = this.$registry.get('field', type)
      return ft?.getIconClass() || 'map'
    },
  },
  validations: {
    values: {
      geoFieldId: { required },
    },
  },
}
</script>

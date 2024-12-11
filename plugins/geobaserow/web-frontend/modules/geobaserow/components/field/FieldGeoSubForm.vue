<template>
  <div>
    <FormGroup
        :label="$t('fieldGeoSubForm.defaultCenterLabel')"
        :helperText="$t('fieldGeoSubForm.defaultCenterHelperText')"
        small-label
        required
        :error="$v.values.default_center_lat.$error"
        class="margin-bottom-2"
    >
      <MapPointInput
          :lat-lng="latLng"
          :basemap="values.basemap"
          :error="hasLatLngErrors()"
          @change="updateLatLng"
      ></MapPointInput>

    </FormGroup>
    <FormGroup
        :label="$t('fieldGeoSubForm.defaultZoomLabel')"
        small-label
        required
        :error="$v.values.default_zoom.$error"
        class="margin-bottom-2">
      <FormInput
          v-model="values.default_zoom"
          type="number"
          :min="1"
          :max="20"
      ></FormInput>
    </FormGroup>
    <FormGroup
        :label="$t('fieldGeoSubForm.baseMapLabel')"
        small-label
        required
        :error="$v.values.basemap.$error"
        class="margin-bottom-2"
    >
      <Dropdown
          v-model="values.basemap"
          :error="$v.values.basemap.$error"
          :fixed-items="true"
          @hide="$v.values.basemap.$touch()"
      >
        <DropdownItem
            :name="$t('fieldGeoSubForm.baseMapVoyager')"
            value="voyager"
        ></DropdownItem>
        <DropdownItem
            :name="$t('fieldGeoSubForm.baseMapPositron')"
            value="positron"
        ></DropdownItem>
        <DropdownItem
            :name="$t('fieldGeoSubForm.baseMapDarkMatter')"
            value="dark-matter"
        ></DropdownItem>
      </Dropdown>
    </FormGroup>
  </div>
</template>

<script>
import {required, numeric} from 'vuelidate/lib/validators'

import form from '@baserow/modules/core/mixins/form'
import fieldSubForm from '@baserow/modules/database/mixins/fieldSubForm'
import PaginatedDropdown from '@baserow/modules/core/components/PaginatedDropdown'
import MapPointInput from "@geobaserow/components/MapPointInput";

export default {
  name: 'FieldGeoSubForm',
  components: {
    PaginatedDropdown,
    MapPointInput,
  },
  mixins: [form, fieldSubForm],
  data() {
    return {
      allowedValues: [
        'default_center_lat',
        'default_center_lon',
        'date_time_format',
        'default_zoom',
        'basemap',
      ],
      values: {
        default_center_lat: 0,
        default_center_lon: 0,
        default_zoom: 3,
        basemap: "voyager",
      },
    }
  },
  computed: {
    latLng() {
      return {
        lat: this.values.default_center_lat,
        lng: this.values.default_center_lon,
      }
    },
    onCreate() {
      return (
          this.defaultValues.name === null ||
          this.defaultValues.name === undefined
      )
    },
  },
  watch: {
    'values.default_center_lat'(newValue, oldValue) {
      // For formula fields default_center_lat is nullable, ensure it is set to the
      // default otherwise we will be sending nulls to the server.
      if (newValue == null) {
        this.values.default_center_lat = 0
      }
    },
    'values.default_zoom'(newValue, oldValue) {
      // For formula fields default_zoom is nullable, ensure it is set to the
      // default otherwise we will be sending nulls to the server.
      if (newValue == null) {
        this.values.default_zoom = 3
      }
    },
    'values.basemap'(newValue, oldValue) {
      // For formula fields basemap is nullable, ensure it is set to the
      // default otherwise we will be sending nulls to the server.
      if (newValue == null) {
        this.values.basemap = 'voyager'
      }
    },
  },
  methods: {
    hasLatLngErrors() {
      const fieldNames = ['default_center_lat', 'default_center_lon']
      for (const fieldName of fieldNames) {
        if (this.$v.values[fieldName] && this.$v.values[fieldName].$error) {
          return this.$v.values[fieldName].$error
        }
      }

      return false
    },
    updateLatLng(latLng) {
      this.values.default_center_lat = latLng.lat
      this.values.default_center_lon = latLng.lng


      this.$emit('change', this.values)
    },
  },
  validations: {
    values: {
      default_center_lat: {required},
      default_center_lon: {required},
      default_zoom: {required},
      basemap: {required},
    },
  },
}
</script>

<template>
  <div>
    <div class="control">
      <template v-if="filename === ''">
        <label class="control__label control__label--small">{{
            $t('tableGeoJSONImporter.fileLabel')
          }}</label>
        <div class="control__description">
          {{ $t('tableGeoJSONImporter.fileDescription') }}
          <pre>
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Jomo Kenyatta International Airport",
        "type": "International"
      },
      "geometry": {
        "coordinates": [
          36.92938339575491,
          -1.3248129810721139
        ],
        "type": "Point"
      }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Wilson Airport",
        "type": "Airstrip"
      },
      "geometry": {
        "coordinates": [
          36.81422470097064,
          -1.3238479641131562
        ],
        "type": "Point"
      }
    }
  ]
}
        </pre>
        </div>
      </template>
      <div class="control__elements">
        <div class="file-upload">
          <input
              v-show="false"
              ref="file"
              type="file"
              accept=".json,.geojson"
              @change="select($event)"
          />
          <Button
              type="upload"
              size="large"
              icon="iconoir-cloud-upload"
              class="file-upload__button"
              :loading="state !== null"
              @click.prevent="$refs.file.click($event)"
          >
            {{ $t('tableGeoJSONImporter.chooseButton') }}
          </Button>
          <div v-if="state === null" class="file-upload__file">
            {{ filename }}
          </div>
          <template v-else>
            <ProgressBar
                :value="fileLoadingProgress"
                :show-value="state === 'loading'"
                :status="
                state === 'loading' ? $t('importer.loading') : stateTitle
              "
            />
          </template>
        </div>
        <div v-if="$v.filename.$error" class="error">
          {{ $t('error.requiredField') }}
        </div>
      </div>
    </div>
    <div v-if="filename !== ''" class="control margin-top-2">
      <label class="control__label control__label--small">{{
          $t('tableGeoJSONImporter.encodingLabel')
        }}</label>
      <div class="control__elements">
        <CharsetDropdown
            v-model="encoding"
            :disabled="isDisabled"
            @input="reload()"
        ></CharsetDropdown>
      </div>
    </div>
    <Alert v-if="error !== ''" type="error">
      <template #title> {{ $t('common.wrong') }}</template>
      {{ error }}
    </Alert>
  </div>
</template>

<script>
import {required} from 'vuelidate/lib/validators'

import form from '@baserow/modules/core/mixins/form'
import CharsetDropdown from '@baserow/modules/core/components/helpers/CharsetDropdown'
import importer from '@baserow/modules/database/mixins/importer'
import gjv from "geojson-validation";
import {stringify} from "wellknown"

const IMPORT_PREVIEW_MAX_ROW_COUNT = 6

export default {
  name: 'TableGeoJSONImporter',
  components: {CharsetDropdown},
  mixins: [form, importer],
  data() {
    return {
      encoding: 'utf-8',
      filename: '',
      rawData: null,
    }
  },
  validations: {
    filename: {required},
  },
  computed: {
    isDisabled() {
      return this.disabled || this.state !== null
    },
  },
  methods: {
    /**
     * Method that is called when a file has been chosen. It will check if the file is
     * not larger than 15MB. Otherwise it will take a long time and possibly a crash
     * if so many entries have to be loaded into memory. If the file is valid, the
     * contents will be loaded into memory and the reload method will be called which
     * parses the content.
     */
    select(event) {
      if (event.target.files.length === 0) {
        return
      }

      const file = event.target.files[0]

      const maxSize =
          parseInt(this.$config.BASEROW_MAX_IMPORT_FILE_SIZE_MB, 10) * 1024 * 1024

      if (file.size > maxSize) {
        this.filename = ''
        this.handleImporterError(
            this.$t('tableGeoJSONImporter.limitFileSize', {
              limit: this.$config.BASEROW_MAX_IMPORT_FILE_SIZE_MB,
            })
        )
      } else {
        this.state = 'loading'
        this.$emit('changed')
        this.filename = file.name
        const reader = new FileReader()
        reader.addEventListener('progress', (event) => {
          this.fileLoadingProgress = (event.loaded / event.total) * 100
        })
        reader.addEventListener('load', (event) => {
          this.rawData = event.target.result
          this.fileLoadingProgress = 100
          this.reload()
        })
        reader.readAsArrayBuffer(event.target.files[0])
      }
    },
    async reload() {
      let json
      this.resetImporterState()

      try {
        const decoder = new TextDecoder(this.encoding)
        this.state = 'parsing'
        await this.$ensureRender()
        const decoded = decoder.decode(this.rawData)

        await this.$ensureRender()
        json = JSON.parse(decoded)
      } catch (error) {
        this.handleImporterError(
            this.$t('tableGeoJSONImporter.processingError', {
              error: error.message,
            })
        )
        return
      }

      if (Object.keys(json).length === 0 && json.constructor === Object) {
        this.handleImporterError(this.$t('tableGeoJSONImporter.emptyError'))
        return
      }

      if (!gjv.valid(json)) {
        this.handleImporterError(this.$t('tableGeoJSONImporter.validError'))
        return
      }

      const limit = this.$config.INITIAL_TABLE_DATA_LIMIT
      if (limit !== null && json.features.length > limit - 1) {
        this.handleImporterError(
            this.$t('tableGeoJSONImporter.limitError', {
              limit,
            })
        )
        return
      }

      const header = ["geometry"]
      const data = []

      await this.$ensureRender()

      json.features.forEach((entry) => {
        const properties = entry.properties
        const keys = Object.keys(properties)
        const row = []

        keys.forEach((key) => {
          if (!header.includes(key)) {
            header.push(key)
          }
        })

        header.forEach((key) => {
          const exists = Object.prototype.hasOwnProperty.call(properties, key)
          if (key === 'geometry') {
            row.push(entry.geometry)
            return
          }

          const value = exists ? properties[key] : ''
          row.push(value)
        })

        data.push(row)
      })

      const preparedHeader = this.prepareHeader(header, data)
      const getData = () => {
        return data
      }
      this.state = null
      const previewData = this.getPreview(header, data)

      this.$emit('getData', getData)
      this.$emit('data', {header: preparedHeader, previewData})
    },
    /**
     * Generates an object that can used to render a quick preview of the provided
     * data.
     */
    getPreview(head, data) {
      let rows = data.slice(0, IMPORT_PREVIEW_MAX_ROW_COUNT)

      const columns = Math.max.apply(
          null,
          data.map((entry) => entry.length)
      )

      rows = rows.map((row) => this.fill(row, columns)).map((row) => {
        row = row.map((value) => {
          // If the value is a geojson object, convert it to a wkt string for display.
          if (value && value.type && value.coordinates) {
            return stringify(value)
          }
          return value
        })
        return row
      })

      return rows
    },
  },
}
</script>

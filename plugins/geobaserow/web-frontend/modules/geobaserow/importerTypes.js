import {ImporterType} from '@baserow/modules/database/importerTypes'

import TableGeoJSONImporter from "@geobaserow/components/table/TableGeoJSONImporter";


export class GeoJSONImporterType extends ImporterType {
    static getType() {
        return 'geojson'
    }

    getIconClass() {
        return 'baserow-icon-file-code'
    }

    getName() {
        const {i18n} = this.app
        return i18n.t('importerType.geojson')
    }

    getFormComponent() {
        return TableGeoJSONImporter
    }
}
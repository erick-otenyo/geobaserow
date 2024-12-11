import {FieldType} from '@baserow/modules/database/fieldTypes'
import FieldTextSubForm from '@baserow/modules/database/components/field/FieldTextSubForm'
import FieldGeoSubForm from '@geobaserow/components/field/FieldGeoSubForm'
import {genericContainsFilter,} from '@baserow/modules/database/utils/fieldFilters'

import FunctionalGridViewFieldGeometry from '@geobaserow/components/FunctionalGridViewFieldGeometry'
import RowCardFieldGeometry from '@geobaserow/components/RowCardFieldGeometry'

import RowEditFieldPoint from '@geobaserow/components/RowEditFieldPoint'
import RowEditFieldMultiPolygon from '@geobaserow/components/RowEditFieldMultiPolygon'


class GeometryFieldType extends FieldType {
    getGridViewFieldComponent() {
        return FunctionalGridViewFieldGeometry
    }

    getFunctionalGridViewFieldComponent() {
        return FunctionalGridViewFieldGeometry
    }

    getCardComponent() {
        return RowCardFieldGeometry
    }

    getFormComponent() {
        return FieldGeoSubForm
    }

    getSort(name, order) {
        return (a, b) => {
            const stringA = a[name] === null ? '' : '' + a[name]
            const stringB = b[name] === null ? '' : '' + b[name]

            return order === 'ASC'
                ? stringA.localeCompare(stringB)
                : stringB.localeCompare(stringA)
        }
    }

    getDocsDataType(field) {
        return 'string'
    }

    getDocsDescription(field) {
        return this.app.i18n.t('fieldDocs.text')
    }

    getDocsRequestExample(field) {
        return 'string'
    }

    getContainsFilterFunction() {
        return genericContainsFilter
    }

    canBeReferencedByFormulaField() {
        return true
    }

    getEmptyValue(field) {
        return field
    }

    canRepresentGeo() {
        return true
    }
}


export class PointFieldType extends GeometryFieldType {
    static getType() {
        return 'point'
    }

    getIconClass() {
        return 'globe'
    }

    getName() {
        return 'Point'
    }

    getRowEditFieldComponent() {
        return RowEditFieldPoint
    }
}

export class MultiPolygonFieldType extends GeometryFieldType {
    static getType() {
        return 'multipolygon'
    }

    getIconClass() {
        return 'globe'
    }

    getName() {
        return 'MultiPolygon'
    }

    getRowEditFieldComponent() {
        return RowEditFieldMultiPolygon
    }
}

import { FieldType } from '@baserow/modules/database/fieldTypes'
import FieldTextSubForm from '@baserow/modules/database/components/field/FieldTextSubForm'
import RowCardFieldText from '@baserow/modules/database/components/card/RowCardFieldText'
import {
    genericContainsFilter,
} from '@baserow/modules/database/utils/fieldFilters'

import FunctionalGridViewFieldPoint from '@geobaserow/components/FunctionalGridViewFieldPoint'
import GridViewFieldPoint from '@geobaserow/components/GridViewFieldPoint'
import RowEditFieldPoint from '@geobaserow/components/RowEditFieldPoint'
import RowCardFieldPoint from '@geobaserow/components/RowCardFieldPoint'

export class PointFieldType extends FieldType {
    static getType() {
        return 'point'
    }

    getIconClass() {
        return 'globe'
    }

    getName() {
        return 'Point'
    }

    getFormComponent() {
        return FieldTextSubForm
    }

    getGridViewFieldComponent() {
        return GridViewFieldPoint
    }

    getFunctionalGridViewFieldComponent() {
        return FunctionalGridViewFieldPoint
    }

    getRowEditFieldComponent() {
        return RowEditFieldPoint
    }

    getCardComponent() {
        return RowCardFieldPoint
    }

    getEmptyValue(field) {
        return field
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

    canRepresentGeo() {
        return true
    }

}

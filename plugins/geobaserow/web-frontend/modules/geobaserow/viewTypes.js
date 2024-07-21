import { maxPossibleOrderValue, ViewType } from '@baserow/modules/database/viewTypes'
import MapView from '@geobaserow/components/views/map/MapView'
import MapViewHeader from '@geobaserow/components/views/map/MapViewHeader'

export class MapViewType extends ViewType {
    static getType() {
        return 'map'
    }

    getIconClass() {
        return 'iconoir-map'
    }

    getName() {
        return 'Map'
    }


    canFilter() {
        return false
    }

    canSort() {
        return false
    }


    getPublicRoute() {
        return 'database-public-map-view'
    }

    getHeaderComponent() {
        return MapViewHeader
    }

    getComponent() {
        return MapView
    }

    async fetch({ store }, database, view, fields, storePrefix = '') {
        await store.dispatch(storePrefix + 'view/map/resetAndFetchInitial', {
            mapId: view.id, geoFieldId: view.geo_field, fields,
        })
    }

    async refresh({ store }, database, view, fields, storePrefix = '', includeFieldOptions = false, sourceEvent = null) {
        // We need to prevent multiple requests as updates and deletes regarding
        // the date field are handled inside afterFieldUpdated and afterFieldDeleted
        const geoFieldId = store.getters[storePrefix + 'view/map/getGeoFieldIdIfNotTrashed'](fields)
        if (['field_deleted', 'field_updated'].includes(sourceEvent?.type) && sourceEvent?.data?.field_id === geoFieldId) {
            return
        }
        await store.dispatch(storePrefix + 'view/map/refreshAndFetchInitial', {
            mapId: view.id, geoFieldId: view.geo_field, fields, includeFieldOptions,
        })
    }

    async fieldOptionsUpdated({ store }, view, fieldOptions, storePrefix) {
        await store.dispatch(storePrefix + 'view/map/forceUpdateAllFieldOptions', fieldOptions, {
            root: true,
        })
    }

    updated(context, view, oldView, storePrefix) {
        return view.geo_field !== oldView.geo_field
    }

    async rowCreated({ store }, tableId, fields, values, metadata, storePrefix = '') {
        if (this.isCurrentView(store, tableId)) {
            await store.dispatch(storePrefix + 'view/map/createdNewRow', {
                view: store.getters['view/getSelected'], values, fields,
            })
        }
    }

    async rowUpdated({ store }, tableId, fields, row, values, metadata, storePrefix = '') {
        if (this.isCurrentView(store, tableId)) {
            await store.dispatch(storePrefix + 'view/map/updatedExistingRow', {
                view: store.getters['view/getSelected'], fields, row, values,
            })
        }
    }

    async rowDeleted({ store }, tableId, fields, row, storePrefix = '') {
        if (this.isCurrentView(store, tableId)) {
            await store.dispatch(storePrefix + 'view/map/deletedExistingRow', {
                view: store.getters['view/getSelected'], row, fields,
            })
        }
    }

    async afterFieldCreated({ dispatch }, table, field, fieldType, storePrefix = '') {
        const value = fieldType.getEmptyValue(field)
        await dispatch(storePrefix + 'view/map/addField', { field, value }, { root: true })
        await dispatch(storePrefix + 'view/map/setFieldOptionsOfField', {
            field, // The default values should be the same as in the `CalendarViewFieldOptions`
            // model in the backend to stay consistent.
            values: {
                hidden: true, order: maxPossibleOrderValue,
            },
        }, { root: true })
    }

    async afterFieldUpdated(context, field, oldField, fieldType, storePrefix) {
        const fields = [field]
        const geoFieldId = context.rootGetters[storePrefix + 'view/map/getGeoFieldIdIfNotTrashed'](fields)

        if (geoFieldId === field.id) {
            const type = this.app.$registry.get('field', field.type)
            if (type.canRepresentGeo && !type.canRepresentGeo(field)) {
                this._setFieldToNull(context, field, 'geo_field')
                await context.dispatch(storePrefix + 'view/map/reset', {}, { root: true })
            } else {
                await context.dispatch(storePrefix + 'view/map/fetchInitial', {
                    includeFieldOptions: false, fields,
                }, { root: true })
            }
        }
    }

    async afterFieldDeleted(context, field, fieldType, storePrefix = '') {
        const fields = [field]
        this._setFieldToNull(context, field, 'geo_field')
        const geoFieldId = context.rootGetters[storePrefix + 'view/map/getGeoFieldIdIfNotTrashed'](fields)
        if (geoFieldId === field.id) {
            await context.dispatch(storePrefix + 'view/map/reset', {}, { root: true })
        }
    }
}
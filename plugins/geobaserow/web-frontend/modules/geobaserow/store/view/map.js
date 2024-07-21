import Vue from 'vue'
import ViewService from '@baserow/modules/database/services/view'

import MapService from '@geobaserow/services/views/map'

import { getDefaultSearchModeFromEnv } from '@baserow/modules/database/utils/search'

import { extractRowMetadata } from '@baserow/modules/database/utils/view'


export function populateRow(row, metadata = {}) {
    row._ = {
        metadata,
        dragging: false,
    }
    return row
}

export const state = () => ({
    loading: false,
    loadingRows: false,
    // The map view id that is being displayed
    lastMapId: null,
    rows: [],
    // The chosen geo field that the
    // items will be organized by in the view
    geoFieldId: null,
    fieldOptions: {},
})

export const mutations = {
    RESET(state) {
        state.loadingRows = false
        state.lastMapId = null
        state.geoFieldId = null
        state.fieldOptions = {}
    },
    SET_LOADING_ROWS(state, loading) {
        state.loadingRows = loading
    },
    SET_ROW_LOADING(state, { row, value }) {
        Vue.set(row._, 'loading', value)
    },
    SET_LAST_MAP_ID(state, mapId) {
        state.lastMapId = mapId
    },
    SET_GEO_FIELD_ID(state, geoFieldId) {
        state.geoFieldId = geoFieldId
    },

    CLEAR_ROWS(state) {
        state.count = 0
        state.rows = []
    },

    ADD_ROWS(
        state,
        { rows, prependToRows, appendToRows, count }
    ) {
        state.count = count


        if (prependToRows > 0) {
            state.rows = [...rows.slice(0, prependToRows), ...state.rows]
        }
        if (appendToRows > 0) {
            state.rows.push(...rows.slice(0, appendToRows))
        }

        if (prependToRows < 0) {
            state.rows = state.rows.splice(Math.abs(prependToRows))
        }
        if (appendToRows < 0) {
            state.rows = state.rows.splice(
                0,
                state.rows.length - Math.abs(appendToRows)
            )
        }
    },


    REPLACE_ALL_FIELD_OPTIONS(state, fieldOptions) {
        state.fieldOptions = fieldOptions
    },
    UPDATE_ALL_FIELD_OPTIONS(state, fieldOptions) {
        state.fieldOptions = _.merge({}, state.fieldOptions, fieldOptions)
    },
    UPDATE_FIELD_OPTIONS_OF_FIELD(state, { fieldId, values }) {
        if (Object.prototype.hasOwnProperty.call(state.fieldOptions, fieldId)) {
            Object.assign(state.fieldOptions[fieldId], values)
        } else {
            state.fieldOptions = Object.assign({}, state.fieldOptions, {
                [fieldId]: values,
            })
        }
    },
    DELETE_FIELD_OPTIONS(state, fieldId) {
        if (Object.prototype.hasOwnProperty.call(state.fieldOptions, fieldId)) {
            delete state.fieldOptions[fieldId]
        }
    },
}


export const actions = {
    /**
     * Resets the store completely throwing away all state.
     */
    reset({ dispatch, commit, getters }, _) {
        commit('RESET')
    },
    /**
     * Resets the store completely throwing away all state and loads new rows given
     * a new view etc.
     * rows.
     */
    async resetAndFetchInitial(
        { dispatch, commit, getters },
        { mapId, geoFieldId, fields, includeFieldOptions = true }
    ) {
        commit('RESET')
        await dispatch('refreshAndFetchInitial', {
            mapId,
            geoFieldId,
            fields,
            includeFieldOptions,
        })
    },
    /**
     * Refreshes the store given new date and view parameters and then refetches the
     * rows. Doesn't throw away field options etc.
     */
    async refreshAndFetchInitial(
        { dispatch, commit, getters },
        { mapId, geoFieldId, fields, includeFieldOptions = true }
    ) {
        commit('SET_GEO_FIELD_ID', geoFieldId)
        commit('SET_LAST_MAP_ID', mapId)
        await dispatch('fetchInitial', {
            includeFieldOptions,
            fields,
        })
    },
    /**
     * Fetches an initial set of rows and adds that data to the store.
     */
    async fetchInitial(
        { dispatch, commit, getters },
        { fields, includeFieldOptions = true }
    ) {
        if (!process.server) {
            await dispatch('fetchRows', {
                fields,
                includeFieldOptions,
            })
        }
    },


    async fetchRows(
        { commit, getters, rootGetters },
        { fields, includeFieldOptions = true }
    ) {

        commit('SET_LOADING_ROWS', true)

        try {



            const { data } = await MapService(this.$client).fetchRows({
                mapId: getters.getLastMapId,
                includeFieldOptions,
                search: getters.getServerSearchTerm,
                searchMode: getDefaultSearchModeFromEnv(this.$config),
                publicUrl: rootGetters['page/view/public/getIsPublic'],
                publicAuthToken: rootGetters['page/view/public/getAuthToken'],
            })

            data.results.forEach((row) => {
                const metadata = extractRowMetadata(data, row.id)
                populateRow(row, metadata)
            })

            commit('CLEAR_ROWS')

            commit('ADD_ROWS', {
                rows: data.results,
                prependToRows: 0,
                appendToRows: data.results.length,
                count: data.count,
            })

            commit('SET_LOADING_ROWS', false)
        } catch (error) {
            if (error.handler.code === 'ERROR_MAP_VIEW_HAS_NO_GEO_FIELD') {
                commit('RESET')
            }
            throw error
        } finally {

            commit('SET_LOADING_ROWS', false)
        }
    },


    /**
     * Updates the field options of a given field in the store. So no API request to
     * the backend is made.
     */
    setFieldOptionsOfField({ commit }, { field, values }) {
        commit('UPDATE_FIELD_OPTIONS_OF_FIELD', {
            fieldId: field.id,
            values,
        })
    },
    /**
     * Replaces all field options with new values and also makes an API request to the
     * backend with the changed values. If the request fails the action is reverted.
     */
    async updateAllFieldOptions(
        { dispatch, getters, rootGetters },
        { newFieldOptions, oldFieldOptions, readOnly = false }
    ) {
        dispatch('forceUpdateAllFieldOptions', newFieldOptions)

        const mapId = getters.getLastMapId
        if (!readOnly) {
            const updateValues = { field_options: newFieldOptions }

            try {
                await ViewService(this.$client).updateFieldOptions({
                    viewId: mapId,
                    values: updateValues,
                })
            } catch (error) {
                dispatch('forceUpdateAllFieldOptions', oldFieldOptions)
                throw error
            }
        }
    },
    /**
     * Forcefully updates all field options without making a call to the backend.
     */
    forceUpdateAllFieldOptions({ commit }, fieldOptions) {
        commit('UPDATE_ALL_FIELD_OPTIONS', fieldOptions)
    },
    /**
     * Deletes the field options of the provided field id if they exist.
     */
    forceDeleteFieldOptions({ commit }, fieldId) {
        commit('DELETE_FIELD_OPTIONS', fieldId)
    },
    /**
     * Updates the order of all the available field options. The provided order parameter
     * should be an array containing the field ids in the correct order.
     */
    async updateFieldOptionsOrder(
        { commit, getters, dispatch },
        { order, readOnly = false }
    ) {
        const oldFieldOptions = clone(getters.getAllFieldOptions)
        const newFieldOptions = clone(getters.getAllFieldOptions)

        // Update the order of the field options that have not been provided in the order.
        // They will get a position that places them after the provided field ids.
        let i = 0
        Object.keys(newFieldOptions).forEach((fieldId) => {
            if (!order.includes(parseInt(fieldId))) {
                newFieldOptions[fieldId].order = order.length + i
                i++
            }
        })

        // Update create the field options and set the correct order value.
        order.forEach((fieldId, index) => {
            const id = fieldId.toString()
            if (Object.prototype.hasOwnProperty.call(newFieldOptions, id)) {
                newFieldOptions[fieldId.toString()].order = index
            }
        })

        return await dispatch('updateAllFieldOptions', {
            oldFieldOptions,
            newFieldOptions,
            readOnly,
        })
    },
    /**
     * Updates the field options of a specific field.
     */
    async updateFieldOptionsOfField(
        { commit, getters, rootGetters },
        { view, field, values, readOnly = false, undoRedoActionGroupId = null }
    ) {
        commit('UPDATE_FIELD_OPTIONS_OF_FIELD', {
            fieldId: field.id,
            values,
        })

        if (!readOnly) {
            const mapId = getters.getLastMapId
            const oldValues = clone(getters.getAllFieldOptions[field.id])
            const updateValues = { field_options: {} }
            updateValues.field_options[field.id] = values

            try {
                await ViewService(this.$client).updateFieldOptions({
                    viewId: mapId,
                    values: updateValues,
                    undoRedoActionGroupId,
                })
            } catch (error) {
                commit('UPDATE_FIELD_OPTIONS_OF_FIELD', {
                    fieldId: field.id,
                    values: oldValues,
                })
                throw error
            }
        }
    },

}


export const getters = {
    getServerSearchTerm(state) {
        return state.activeSearchTerm
    },
    getActiveSearchTerm(state) {
        return state.activeSearchTerm
    },
    isHidingRowsNotMatchingSearch(state) {
        return state.hideRowsNotMatchingSearch
    },
    getLoadingRows(state) {
        return state.loadingRows
    },
    getLastMapId(state) {
        return state.lastMapId
    },
    getGeoFieldIdIfNotTrashed: (state, getters) => (fields) => {
        return getters.getGeoField(fields)?.id
    },
    getAllFieldOptions(state) {
        return state.fieldOptions
    },
    getAllRows(state) {
        let rows = []
        return rows
    },
    getGeoField: (state) => (fields) => {
        const fieldId = state.geoFieldId
        if (fieldId) {
            return fields.find((field) => field.id === fieldId)
        } else {
            return null
        }
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
}

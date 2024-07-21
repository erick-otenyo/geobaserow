import addPublicAuthTokenHeader from '@baserow/modules/database/utils/publicView'

export default (client) => {
    return {
        fetchRows({
            mapId,
            includeFieldOptions = false,
            includeRowMetadata = true,
            publicUrl = false,
            publicAuthToken = null,
            search = '',
            searchMode = '',
        }) {
            const include = []
            const params = new URLSearchParams()


            if (includeFieldOptions) {
                include.push('field_options')
            }

            if (includeRowMetadata) {
                include.push('row_metadata')
            }

            if (include.length > 0) {
                params.append('include', include.join(','))
            }

            if (search) {
                params.append('search', search)
                if (searchMode) {
                    params.append('search_mode', searchMode)
                }
            }

            const config = { params }

            if (publicAuthToken) {
                addPublicAuthTokenHeader(config, publicAuthToken)
            }

            const url = publicUrl ? 'public/rows/' : ''

            return client.get(`/database/views/map/${mapId}/${url}`, config)
        },
    }
}

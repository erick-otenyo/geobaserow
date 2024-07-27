import {stringify} from "wellknown"


/*

* It converts geojson to WKT
*/

export const geojsonToWKT = (value) => {

    if (value === null || value === undefined || value === '') {
        return ''
    }

    if (value.type && value.coordinates) {
        return stringify(value)
    }

    return ''
}


export const prepareRequestHeaders = (store) => {
    const headers = {}

    const application = store.getters['userSourceUser/getCurrentApplication']
    if (store.getters['auth/isAuthenticated']) {
        const token = store.getters['auth/token']
        headers.Authorization = `JWT ${token}`
        headers.ClientSessionId =
            store.getters['auth/getUntrustedClientSessionId']
        // If we are logged with Baserow user and with a user source user
        // so we also want to send this user token
        // to the backend through the custom `UserSourceAuthorization` header.
        // This enables the "double" authentication.
        // We access the data with the permission of the currently logged Baserow user
        // but we can see the data of the user source user.
        if (store.getters['userSourceUser/isAuthenticated'](application)) {
            const userSourceToken =
                store.getters['userSourceUser/accessToken'](application)
            headers.UserSourceAuthorization = `JWT ${userSourceToken}`
        }
    } else if (store.getters['userSourceUser/isAuthenticated'](application)) {
        // Here we are logged as a user source user
        const userSourceToken =
            store.getters['userSourceUser/accessToken'](application)
        headers.Authorization = `JWT ${userSourceToken}`
    }
    if (store.getters['auth/webSocketId'] !== null) {
        const webSocketId = store.getters['auth/webSocketId']
        headers.WebSocketId = webSocketId
    }

    return headers
}



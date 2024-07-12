import { stringify } from "wellknown"


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




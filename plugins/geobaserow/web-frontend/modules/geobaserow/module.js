import path from 'path'

import {routes} from './routes'

import en from './locales/en.json'

export default function () {

    this.nuxt.hook('i18n:extend-messages', (additionalMessages) => {
        additionalMessages.push({en})
    })

    this.options.alias['@geobaserow'] = path.resolve(
        __dirname,
        './'
    )
    this.extendRoutes((configRoutes) => {
        configRoutes.push(...routes)
    })
    this.appendPlugin({
        src: path.resolve(__dirname, 'plugin.js'),
    })
    this.options.css.push(path.resolve(__dirname, 'assets/scss/default.scss'))

    this.requireModule('nuxt-leaflet')
}

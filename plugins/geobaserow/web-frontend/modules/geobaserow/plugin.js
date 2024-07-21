import { PluginNamePlugin } from '@geobaserow/plugins'
import { PointFieldType } from '@geobaserow/fieldTypes'
import { MapViewType } from '@geobaserow/viewTypes'

import mapStore from '@geobaserow/store/view/map'

import en from '@geobaserow/locales/en.json'


export default (context) => {
  const { store, app, isDev } = context

  // Allow locale file hot reloading
  if (isDev && app.i18n) {
    const { i18n } = app
    i18n.mergeLocaleMessage('en', en)
  }

  store.registerModule('page/view/map', mapStore)

  app.$registry.register('plugin', new PluginNamePlugin(context))
  app.$registry.register('field', new PointFieldType(context))

  app.$registry.register('view', new MapViewType(context))

}

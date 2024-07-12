import { PluginNamePlugin } from '@geobaserow/plugins'
import { PointFieldType } from '@geobaserow/fieldTypes'

export default (context) => {
  const { app } = context
  app.$registry.register('plugin', new PluginNamePlugin(context))
  app.$registry.register('field', new PointFieldType(context))
}

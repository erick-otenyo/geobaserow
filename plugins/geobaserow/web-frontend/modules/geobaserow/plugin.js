import { PluginNamePlugin } from '@geobaserow/plugins'

export default (context) => {
  const { app } = context
  app.$registry.register('plugin', new PluginNamePlugin(context))
}

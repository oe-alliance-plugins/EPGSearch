
from Components.config import config
from Components.PluginComponent import plugins
from Screens.Setup import Setup
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from Plugins.Plugin import PluginDescriptor

from . import _, allowShowOrbital, getOrbposConfList, purgeOrbposConfig, updateOrbposConfig


class EPGSearchSetup(Setup):
	def __init__(self, session):
		nchoices = updateOrbposConfig(save=True)
		if nchoices <= 2:
			config.plugins.epgsearch.enableorbpos.value = False
		self.allowShowOrbital = allowShowOrbital
		Setup.__init__(self, session, "epgsearch", plugin="Extensions/EPGSearch", PluginLanguageDomain="EPGSearch")
		self.setTitle(_("EPGSearch Setup"))
		self.notifiers = (
			config.plugins.epgsearch.scope,
			config.plugins.epgsearch.enableorbpos,
			config.plugins.epgsearch.invertorbpos,
			config.plugins.epgsearch.numorbpos,
		)
		self.onClose.append(self.clearNotifiers)
		self.updateConfig()
		self.addNotifiers()

	def addNotifiers(self):
		for n in self.notifiers:
			n.addNotifier(self.updateConfig, initial_call=False)

	def clearNotifiers(self):
		for n in self.notifiers:
			n.removeNotifier(self.updateConfig)

	def createSetup(self):
		Setup.createSetup(self)
		for config_item in self.createOrbposConfig():
			self.list.append(config_item)

	def updateConfig(self, configElement=None):
		self.createSetup()

	def createOrbposConfig(self):
		# Only show source/orbpos choices if there is more than
		# one choice (not including "disabled")
		nchoices = updateOrbposConfig()
		if nchoices > 2:
			config_list = [(_("Filter results by source"), config.plugins.epgsearch.enableorbpos, _("Include or exclude results depending on their source (e.g. by satellite)"))]
			if config.plugins.epgsearch.enableorbpos.value:
				config_list += [
					(_("Include/exclude sources"), config.plugins.epgsearch.invertorbpos, _("Use source restrictions below to only include results from the sources, or exclude them.")),
					(_("Number of inclusions/exclusions"), config.plugins.epgsearch.numorbpos, _("Number of filters for inclusion/exclusion of results")),
				]
				restriction_name = _("Include results from") if config.plugins.epgsearch.invertorbpos.value == _("include") else _("Exclude results from")
				restriction_desc = _("Include/exclude search results from this type of source")
				config_list += [
					(restriction_name, confItem, restriction_desc)
					for confItem in getOrbposConfList(includeDisabled=True)
				]
			return config_list
		return []

	def keySave(self):
		purgeOrbposConfig()
		if not config.plugins.epgsearch.showinplugins.value:
			for plugin in plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU):
				if plugin.name == _("EPGSearch"):
					plugins.removePlugin(plugin)

		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		Setup.keySave(self)

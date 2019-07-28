import splunk.admin as admin


class ConfigApp(admin.MConfigHandler):
    def setup(self):
        if self.requestedAction == admin.ACTION_EDIT:
            for arg in ['location', 'optimize', 'proxy']:
                self.supportedArgs.addOptArg(arg)

    def handleList(self, confInfo):
        conf_dict = self.readConf("pyden")
        if conf_dict is not None:
            for stanza, settings in conf_dict.items():
                if stanza == "appsettings":
                    for key, val in settings.items():
                        if key in ['optimize']:
                            if int(val) == 1:
                                val = '1'
                            else:
                                val = '0'
                        if key in ['location', 'proxy'] and val in [None, '']:
                            val = ''
                        confInfo[stanza].append(key, val)

    def handleEdit(self, confInfo):
        if self.callerArgs.data['proxy'][0] in [None, '']:
            self.callerArgs.data['proxy'][0] = ''

        if int(self.callerArgs.data['optimize'][0]) == 1:
            self.callerArgs.data['optimize'][0] = '1'
        else:
            self.callerArgs.data['optimize'][0] = '0'

        if self.callerArgs.data['location'][0] in [None, '']:
            self.callerArgs.data['location'][0] = ''

        self.writeConf('pyden', 'appsettings', self.callerArgs.data)


# initialize the handler
admin.init(ConfigApp, admin.CONTEXT_NONE)

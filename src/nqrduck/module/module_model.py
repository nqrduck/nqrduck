from PyQt5.QtCore import QObject


class ModuleModel(QObject):

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def toolbar_name(self):
        return self._toolbox_name
    
    @toolbar_name.setter
    def toolbar_name(self, value):
        self._toolbox_name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property 
    def tooltip(self):
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        self._tooltip = value

    @property
    def category(self):
        return self._category

    @category.setter
    def catergory(self, value):
        self._category = value

    @property 
    def tooltip(self):
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        self._tooltip = value

    @property
    def toolbox_logo(self):
        return self._toolbox_logo

    @toolbox_logo.setter
    def toolbox_logo(self, value):
        self._toolbox_logo = value

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value
    
    @property
    def widget_file(self):
        return self._widget_file

    @widget_file.setter
    def widget_file(self, value):
        self._widget_file = value

    @property
    def widget(self):
        return self._widget

    @widget.setter
    def widget(self, value):
        self._widget = value
        self.widget_changed.emit(value)
"""Tests that loads a module from the nqrduck entry points."""
from PyQt6.QtWidgets import QApplication
from nqrduck.core.main_model import MainModel
from nqrduck.core.main_controller import MainController

def test_load_module():
    """Tests that loads a module from the nqrduck entry points."""
    main_view = StubMainView()
    
    main_model = MainModel()
    main_controller = MainController(main_model)

    main_controller.load_modules(main_view)
    main_model.active_module = main_model.loaded_modules[list(main_model.loaded_modules.keys())[0]]
    assert main_model.active_module is not None
    assert main_model.loaded_modules is not None


class StubMainView(QApplication):
    """This is only a stub for the tests."""
    def __init__(self):
        """Initializes the StubMainView."""
        super().__init__([])
 

    def on_module_widget_added(self, widget):
        """This is only a stub for the tests."""
        pass

    def on_menu_bar_item_added(self, menu_item):
        """This is only a stub for the tests."""
        pass

    def on_settings_changed(self):
        """This is only a stub for the tests."""
        pass


if __name__ == "__main__":
    test_load_module()
    print("load_module.py: All tests passed")
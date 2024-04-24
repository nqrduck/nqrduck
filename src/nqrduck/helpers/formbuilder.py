"""A module that allows for easy creation of form views in the NQRduck framework."""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

# Brainstorming:
# - We can specify different types of form fields
#    - Numerical (with min/max values and input validation)
#    - Function Selection (with time and frequency domain options)
#    - Dropdowns
#    - Checkboxes (Boolean)
#    - ...
# So the user specifies what type of form they want - then it can be generated for them.
# When the user  finishes the form one can easily retrieve the values from the different fields.
# Ideally the formbuilder re-uses the duckwidgets to create the form fields.
# Optionally a tooltip can be added to each field to provide additional information.

# The view generation needs to be moved from the pulseprogrammer module to this module.
# The functions should not only be defined inside the spectrometer module.

class DuckFormField:
    pass

class DuckFormNumericalField(DuckFormField):
    pass

class DuckFormFunctionSelectionField(DuckFormField):
    pass

class DuckFormDropdownField(DuckFormField):
    pass

class DuckFormCheckboxField(DuckFormField):
    pass

class DuckFormBuilder(QDialog):

    fields = []
    
    def __init__(self, title : str, description : str = None, parent=None) -> None:
        super().__init__(parent=parent)
        self.setParent(parent)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.setWindowTitle(title)

        if description:
            self.description_label = QLabel(description)
            self.main_layout.addWidget(self.description_label)        

    def add_field(self, field : DuckFormField):
        pass

    def get_values(self):
        pass

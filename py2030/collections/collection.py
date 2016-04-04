from py2030.utils.event import Event
from py2030.collections.model import Model

class Collection(list):
    model = Model

    def __len__(self):
        return len(self.models)

    def __init__(self, options = {}):
        # attributes
        self.model = None
        self.models = []

        # events
        self.newModelEvent = Event()
        self.clearEvent = Event()

    #     # configuration
    #     self.options = {}
    #     self.configure(options)
    #
    # def configure(self, options):
    #     previous_options = self.options
    #     self.options.update(options)
    #     # TODO; any internal updates needed for the (re-)configuration happen here

    def create(self, data = {}):
        model = self.model if self.model else self.__class__.model
        new_model = model(data)
        self.add(new_model)

    def add(self, new_model):
        self.models.append(new_model)
        self.newModelEvent(new_model, self)

    def clear(self):
        self.models = []
        self.clearEvent(self)
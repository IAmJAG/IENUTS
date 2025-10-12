
from ..layouts import FlowLayout
from ..utilities import processMarker
from .__componentBase import ComponentBase
from .__containerBase import ContainerBase


@processMarker(True, True)
class ScrollableFlowWidget(ContainerBase):
    def setupUI(self: ComponentBase):
        super().setupUI(FlowLayout())

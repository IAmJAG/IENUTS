from ..contracts.configuration import iConfiguration
from ..serializer import Serialisable


class Sections(Serialisable, dict[str, iConfiguration]): ...

from ..dependencyInjection import iDependency, iDependent


class iConfiguration(iDependent, iDependency):
    def __init__(self):
        ...

    @property
    def Sections(self) -> dict[str, "iConfiguration"]:
        ...

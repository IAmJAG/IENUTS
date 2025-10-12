from .__dependency import iDependency
from .__dependent import iDependent


class iProvider:
    def RegisterSingleton(self, genericInterface: type[iDependency], dependency: iDependency | type[iDependency], dependent: type[iDependent], isDefault: bool = False, *args, **kwargs):
        ...

    def RegisterTransient(self,genericInterface: type[iDependency], dependency: type[iDependency], dependent: type[iDependent], isDefault: bool = False, *args, **kwargs):
        ...

    def Resolve(self, interface: type[iDependency], *args, **kwargs) -> iDependency:
        ...

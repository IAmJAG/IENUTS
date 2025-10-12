from .__dependency import iDependency


class iDependent:
    @property
    def ResolveDepency(self, iDependency) -> iDependency:
        raise NotImplementedError("Provider property is not implemented.")

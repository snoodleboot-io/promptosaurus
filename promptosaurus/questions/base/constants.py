"""Repository types and configuration values."""


class RepositoryTypes:
    """Repository type constants.
    
    This class provides constants for the three supported repository types.
    Use RepositoryTypes.all() to get a list of all valid types.
    """
    SINGLE = "single-language"
    MULTI_MONOREPO = "multi-language-monorepo"
    MIXED = "mixed-collocation"

    @classmethod
    def all(cls) -> list[str]:
        """Get list of all repository types.
        
        Returns:
            List of all valid repository type strings.
        """
        return [cls.SINGLE, cls.MULTI_MONOREPO, cls.MIXED]

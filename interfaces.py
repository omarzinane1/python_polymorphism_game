# interfaces.py
from abc import ABC, abstractmethod

class IDrawable(ABC):
    """Interface pour les objets dessinables sur le canvas."""
    
    @abstractmethod
    def coords(self):
        """Retourne les coordonnées (x, y) de l’objet."""
        pass


class IMovable(ABC):
    """Interface pour les objets capables de se déplacer."""
    
    @abstractmethod
    def move(self, *args, **kwargs):
        """Déplace l’objet sur le canvas."""
        pass

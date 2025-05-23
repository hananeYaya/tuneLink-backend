# Guide des Meilleures Pratiques pour le Projet Mobile Musician

## 1. Structure des Imports et Gestion des Dépendances Circulaires

### 1.1 Imports Circulaires
```python
# ❌ À ÉVITER : Imports directs qui peuvent créer des dépendances circulaires
from app.models.messages import Message
from app.models.user import User

# ✅ RECOMMANDÉ : Utiliser TYPE_CHECKING pour les imports de type
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import Message, User
```

### 1.2 Organisation des Imports
```python
# ✅ RECOMMANDÉ : Ordre des imports
# 1. Imports standard Python
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID

# 2. Imports des packages tiers
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

# 3. Imports locaux
from app.models.base import Base
```

### 1.3 Exports dans __init__.py
```python
# ✅ RECOMMANDÉ : Exposer tous les modèles dans __init__.py
from app.models.base import Base
from app.models.user import User
# ...

__all__ = ["Base", "User", ...]
```

## 2. SQLAlchemy et Typage

### 2.1 Définition des Modèles
```python
# ❌ À ÉVITER : Ancien style SQLAlchemy
class User(Base):
    id = Column(UUID, primary_key=True)
    email = Column(String)

# ✅ RECOMMANDÉ : Style SQLAlchemy 2.0 avec typage
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
```

### 2.2 Relations
```python
# ✅ RECOMMANDÉ : Relations typées
class User(Base):
    messages: Mapped[List["Message"]] = relationship(
        back_populates="sender",
        foreign_keys="Message.sender_id"
    )
```

## 3. Configuration des Linters et Type Checkers

### 3.1 Configuration Pyright (pyrightconfig.json)
```json
{
    "include": ["app"],
    "exclude": ["**/node_modules", "**/__pycache__"],
    "pythonVersion": "3.9",
    "typeCheckingMode": "basic",
    "useLibraryCodeForTypes": true
}
```

### 3.2 Configuration Flake8 (.flake8)
```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__
ignore = E203, W503
```

### 3.3 Configuration MyPy (mypy.ini)
```ini
[mypy]
plugins = sqlalchemy.ext.mypy.plugin
follow_imports = silent
strict_optional = True
```

## 4. Bonnes Pratiques Générales

### 4.1 Documentation
```python
# ✅ RECOMMANDÉ : Docstrings claires et descriptives
class User(Base):
    """
    Modèle représentant un utilisateur de l'application.
    
    Attributes:
        email: Adresse email unique de l'utilisateur
        hashed_password: Mot de passe hashé
    """
```

### 4.2 Nommage
```python
# ✅ RECOMMANDÉ : Noms explicites pour les relations
conversations_as_participant1: Mapped[List["Conversation"]]
conversations_as_participant2: Mapped[List["Conversation"]]
```

### 4.3 Gestion des Types
```python
# ✅ RECOMMANDÉ : Toujours spécifier les types
def get_user_messages(
    user_id: UUID,
    limit: int = 10
) -> List[Message]:
    ...
```

## 5. Résolution des Problèmes Courants

### 5.1 Imports Manquants
- Vérifier que le module est dans le PYTHONPATH
- Utiliser des imports relatifs si nécessaire
- Configurer correctement les outils de développement

### 5.2 Erreurs de Type
- Toujours utiliser les annotations de type
- Utiliser TYPE_CHECKING pour les imports circulaires
- Spécifier les types génériques correctement

### 5.3 Erreurs de Linter
- Configurer les règles appropriées dans .flake8
- Utiliser # noqa quand nécessaire, mais avec parcimonie
- Maintenir la cohérence du style de code

## 6. Docker et Environnement de Développement

### 6.1 Configuration du PYTHONPATH
```dockerfile
ENV PYTHONPATH=/app
WORKDIR /app
```

### 6.2 Installation des Outils de Développement
```dockerfile
RUN pip install --no-cache-dir \
    black \
    flake8 \
    mypy \
    pylint \
    pytest
```

## 7. Maintenance et Évolution

### 7.1 Mises à Jour
- Maintenir les dépendances à jour
- Vérifier la compatibilité des versions
- Tester après chaque mise à jour majeure

### 7.2 Tests
- Écrire des tests pour tous les modèles
- Tester les cas limites
- Maintenir une bonne couverture de tests

## 8. Sécurité

### 8.1 Gestion des Données Sensibles
- Ne jamais exposer les mots de passe
- Utiliser des variables d'environnement
- Implémenter le contrôle d'accès

### 8.2 Validation des Données
- Valider les entrées utilisateur
- Utiliser des contraintes de base de données
- Implémenter des validateurs Pydantic 
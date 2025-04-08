# Fichier principal - Point d'entrée de l'application FastAPI
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Importation de nos configurations depuis le fichier config.py
from app.config import settings

# Création de l'instance de l'application FastAPI
app = FastAPI(
    title="Mobile Musician API",
    description="""
# API Mobile Musician 🎵

API pour l'application Mobile Musician - Mise en relation de musiciens.

## Fonctionnalités

### Utilisateurs 👤

* **Inscription** : Créer un nouveau compte
* **Connexion** : Authentification sécurisée
* **Profil** : Gérer les informations personnelles
* **Préférences** : Instruments et genres musicaux

### Événements 🎪

* **Création** : Organiser des événements musicaux
* **Recherche** : Trouver des événements par lieu/date
* **Participation** : Rejoindre des événements
* **Filtres** : Par type, genre musical, etc.

### Messagerie 💬

* **Conversations** : Échanger avec d'autres musiciens
* **Notifications** : Alertes pour nouveaux messages
* **Groupes** : Discussions pour les événements

### Géolocalisation 🗺️

* **Proximité** : Trouver des musiciens proches
* **Carte** : Visualiser les événements
* **Filtres** : Par distance et disponibilité

## Authentification 🔐

Cette API utilise JWT (JSON Web Tokens) pour l'authentification. 
Pour accéder aux endpoints protégés :

1. Connectez-vous via `/api/v1/auth/login`
2. Utilisez le token reçu dans le header `Authorization`

## Environnements

* **Production** : https://api.mobile-musician.com
* **Staging** : https://staging.mobile-musician.com
* **Local** : http://localhost:8000

## Support

Pour toute question ou problème :
* 📧 Email : support@mobile-musician.com
* 💻 Github : https://github.com/hananeYaya/tuneLink-backend.git
    """,
    version="0.1.0",
    terms_of_service="https://mobile-musician.com/terms/",
    contact={
        "name": "Support API Mobile Musician",
        "url": "https://mobile-musician.com/support",
        "email": "support@mobile-musician.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=[
        {
            "name": "Authentification",
            "description": "Opérations d'authentification et gestion des tokens.",
        },
        {
            "name": "Utilisateurs",
            "description": "Gestion des profils utilisateurs et préférences.",
        },
        {
            "name": "Événements",
            "description": "Création et gestion des événements musicaux.",
        },
        {
            "name": "Messages",
            "description": "Système de messagerie entre utilisateurs.",
        },
        {
            "name": "Notifications",
            "description": "Gestion des notifications système et personnalisées.",
        },
        {
            "name": "Instruments",
            "description": "Gestion des instruments de musique.",
        },
        {
            "name": "Genres",
            "description": "Gestion des genres musicaux.",
        },
    ],
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
)

# Configuration des CORS (Cross-Origin Resource Sharing)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Montage des fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")


def custom_openapi() -> Dict[str, Any]:
    """
    Personnalisation du schéma OpenAPI avec des informations supplémentaires.
    """
    schema = getattr(app, "openapi_schema", None)
    if schema is not None:
        assert isinstance(schema, Dict)
        return dict(schema)

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )

    # Ajout de la version OpenAPI
    openapi_schema["openapi"] = "3.0.2"

    # Personnalisation du schéma
    openapi_schema["info"]["x-logo"] = {
        "url": "/static/logo.png",
        "backgroundColor": "#FFFFFF",
        "altText": "Mobile Musician Logo",
    }

    # Ajout des composants de sécurité
    openapi_schema["components"] = {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Entrez votre token JWT ici",
            }
        },
        "responses": {
            "UnauthorizedError": {"description": "Token d'accès manquant ou invalide"}
        },
    }

    # Sécurité globale
    openapi_schema["security"] = [{"bearerAuth": []}]

    app.openapi_schema = openapi_schema
    return openapi_schema


# Configuration du schéma OpenAPI
app.openapi = custom_openapi  # type: ignore


# Routes pour la documentation
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html() -> Any:
    """
    Route personnalisée pour la documentation Swagger UI.
    """
    html_content = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Documentation Swagger",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css",
        swagger_ui_parameters={
            "configUrl": None,
            "defaultModelsExpandDepth": -1,
            "displayOperationId": True,
            "docExpansion": "none",
            "filter": True,
            "layout": "BaseLayout",
            "operationsSorter": "alpha",
            "showExtensions": True,
            "showCommonExtensions": True,
            "syntaxHighlight.theme": "monokai",
            "tryItOutEnabled": True,
            "persistAuthorization": True,
            "displayRequestDuration": True,
            "deepLinking": True,
        },
    )
    
    # Convertir le contenu HTML en string pour le modifier
    html_str = html_content.body.decode("utf-8")
    
    # Insérer les liens vers ReDoc et RapiDoc dans l'en-tête
    doc_links_html = '''
    <div style="position: absolute; top: 100px; right: 50px; z-index: 1000; display: flex; gap: 30px;">
        <a href="/rapidoc" style="color: white; text-decoration: none; font-weight: bold; font-size: 25px; padding: 5px 10px; border-radius: 4px; background-color: #60d22c;">RapiDoc</a>
        <a href="/redoc" style="color: white; text-decoration: none; font-weight: bold; font-size: 25px; padding: 5px 10px; border-radius: 4px; background-color: #3033e8;">ReDoc</a>
    </div>
    '''
    
    # Injecter nos liens dans le HTML juste après l'ouverture de la balise body
    modified_html = html_str.replace("<body>", f"<body>\n{doc_links_html}")
    
    # Retourner le HTML modifié
    return HTMLResponse(content=modified_html)


@app.get("/redoc", include_in_schema=False)
async def redoc_html() -> Any:
    """
    Route personnalisée pour la documentation ReDoc.
    """
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Documentation ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.png",
    )


@app.get("/rapidoc", include_in_schema=False)
async def rapidoc_html() -> HTMLResponse:
    """
    Route personnalisée pour la documentation RapiDoc.
    """
    return HTMLResponse(
        """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <script type="module" src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"></script>
    <link rel="icon" type="image/png" href="/static/favicon.png"/>
    <title>Mobile Musician API - Documentation RapiDoc</title>
    <style>
        rapi-doc {
            width: 100%;
            height: 100vh;
            display: flex;
        }
    </style>
</head>
<body>
    <rapi-doc
        spec-url="/openapi.json"
        theme="dark"
        bg-color="#1a1a1a"
        text-color="#fafafa"
        primary-color="#00ff00"
        render-style="read"
        show-header="false"
        show-info="true"
        allow-authentication="true"
        allow-server-selection="false"
        allow-search="true"
        allow-advanced-search="true"
        allow-try="true"
        regular-font="Roboto, sans-serif"
        mono-font="Roboto Mono, monospace"
    > </rapi-doc>
</body>
</html>
        """
    )


# Route racine - accessible à l'URL de base de l'API
@app.get("/", tags=["Informations"])
async def root() -> Dict[str, str]:
    """
    Page d'accueil de l'API Mobile Musician.

    Returns:
        dict: Un message de bienvenue et des liens utiles

    Examples:
        >>> response = await root()
        >>> print(response)
        {
            "message": "Bienvenue sur l'API Mobile Musician",
            "documentation": "/docs",
            "rapidoc": "/rapidoc",
            "redoc": "/redoc",
            "github": "https://github.com/votre-organisation/mobile-musician"
        }
    """
    return {
        "message": "Bienvenue sur l'API Mobile Musician",
        "documentation": "/docs",
        "rapidoc": "/rapidoc",
        "redoc": "/redoc",
        "github": "https://github.com/votre-organisation/mobile-musician",
    }


# Route de vérification de l'état de l'API
@app.get("/health", tags=["Informations"])
async def health_check() -> Dict[str, str]:
    """
    Endpoint de vérification de l'état de l'API.

    Returns:
        dict: Le statut de l'API

    Examples:
        >>> response = await health_check()
        >>> assert response["status"] == "ok"
    """
    return {"status": "ok"}

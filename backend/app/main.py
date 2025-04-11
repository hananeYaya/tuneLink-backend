# Fichier principal - Point d'entrée de l'application FastAPI
from typing import Any, Dict

# Imports FastAPI
from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Imports de nos modules
from app.api.router import api_router
from app.config import settings
from app.middlewares.normalized_response import NormalizedResponseMiddleware
from app.schemas.common import StatusCode

# Création de l'application FastAPI
app = FastAPI(
    title="Mobile Musician API",
    description="""...""",  # Ton texte de description complet est inchangé
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
)

# Middleware CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ✅ Fichiers statiques
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.mount(
    "/static/event_banners",
    StaticFiles(directory="app/static/event_banners"),
    name="event_banners"
)
# Routes API principales
app.include_router(api_router, prefix="/api/v1")

# Documentation Swagger UI personnalisée
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html() -> Any:
    html_content = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Documentation Swagger",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "docExpansion": "list",
            "filter": True,
            "tryItOutEnabled": True,
            "persistAuthorization": True,
        },
    )
    html_str = html_content.body.decode("utf-8")
    doc_links_html = '''
    <div style="position: absolute; top: 100px; right: 50px; z-index: 1000; display: flex; gap: 30px;">
        <a href="/rapidoc" style="color: white; text-decoration: none; font-weight: bold; font-size: 25px; padding: 5px 10px; border-radius: 4px; background-color: #60d22c;">RapiDoc</a>
        <a href="/redoc" style="color: white; text-decoration: none; font-weight: bold; font-size: 25px; padding: 5px 10px; border-radius: 4px; background-color: #3033e8;">ReDoc</a>
    </div>
    '''
    modified_html = html_str.replace("<body>", f"<body>\n{doc_links_html}")
    return HTMLResponse(content=modified_html)

# Documentation ReDoc
@app.get("/redoc", include_in_schema=False)
async def redoc_html() -> Any:
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Documentation ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.png",
    )

# Documentation RapiDoc
@app.get("/rapidoc", include_in_schema=False)
async def rapidoc_html() -> HTMLResponse:
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
                allow-try="true"
            > </rapi-doc>
        </body>
        </html>
        """
    )

# Page d'accueil de l'API
@app.get("/", tags=["Informations"])
async def root() -> Dict[str, str]:
    return {
        "message": "Bienvenue sur l'API Mobile Musician",
        "documentation": "/docs",
        "rapidoc": "/rapidoc",
        "redoc": "/redoc",
        "github": "https://github.com/joelkemkeng/event_connect_back_end_api_python",
    }

# Personnalisation OpenAPI
def custom_openapi() -> Dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema.setdefault("components", {})
    openapi_schema["components"].setdefault("schemas", {})
    openapi_schema["components"].setdefault("securitySchemes", {})

    openapi_schema["components"]["securitySchemes"]["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Entrez votre token JWT ici",
    }

    openapi_schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

# Middleware personnalisé
app.add_middleware(NormalizedResponseMiddleware)

# Gestion d'erreurs HTTP
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if isinstance(exc.detail, dict) and "status" in exc.detail and "code" in exc.detail:
        return JSONResponse(content=exc.detail, status_code=exc.status_code, headers=exc.headers)

    return JSONResponse(
        content={
            "status": StatusCode.ERROR,
            "code": exc.status_code,
            "message": str(exc.detail),
            "data": None,
            "errors": None
        },
        status_code=exc.status_code,
        headers=exc.headers
    )

# Gestion d'erreurs de validation
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": err.get("loc", ["inconnu"])[-1],
            "type": err.get("type", ""),
            "message": err.get("msg", "Erreur de validation")
        }
        for err in exc.errors()
    ]

    return JSONResponse(
        content={
            "status": StatusCode.ERROR,
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Erreur de validation des données",
            "data": None,
            "errors": errors
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

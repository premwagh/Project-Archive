SPECTACULAR_SETTINGS = {
    'TITLE': 'Project Archive',
    'VERSION': '',
    'DESCRIPTION': 'Your project description',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'ALLOWED_VERSIONS':['v1', 'v2'],
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
    'DEFAULT_GENERATOR_CLASS': 'core.swagger.generators.SchemaGenerator',
   # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        "displayRequestDuration": True,
        "persistAuthorization": True,
        "filter": True,
    },
}
SPECTACULAR_DEFAULT_API_VERSION = 'v1'

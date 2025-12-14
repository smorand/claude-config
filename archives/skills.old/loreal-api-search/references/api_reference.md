# BTDP API Portal Reference

## API Endpoints

### Base URL

```
https://api.loreal.net/global/it4it/coe/v1/apiinfos/api
```

### Available Endpoints

#### 1. List/Search API Data

**Endpoint**: `GET /api-datas`

**Purpose**: Retrieve list of APIs with optional filtering by API name.

**Query Parameters**:
- `top` (int): Maximum number of results (default: 9000)
- `skip` (int): Number of results to skip for pagination (default: 0)
- `apiName` (string, optional): Filter by specific API name
- `environment` (string): Target environment (default: "prd")

**Example Request**:
```bash
curl -X GET \
  "https://api.loreal.net/global/it4it/coe/v1/apiinfos/api/api-datas?top=9000&skip=0&environment=prd" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**Response Structure**:
```json
{
  "data": [
    {
      "apiName": "global-it4it-btdp-semanticservices-v1",
      "apiTitle": "BTDP Semantic Services API",
      "apiDescription": "API for semantic search and data discovery...",
      "apiVersion": "v1",
      "apiCategory": "data-services",
      "baseUrl": "https://api.loreal.net/global/it4it/btdp-semanticservices",
      "swagger": "https://api.loreal.net/...",
      "contactEmail": "data-platform@loreal.com",
      "owner": "Data Platform Team",
      "status": "active",
      "created": "2023-01-15T10:30:00Z",
      "modified": "2024-11-01T14:22:00Z"
    }
  ],
  "totalCount": 1234
}
```

**Response Fields**:
- `apiName`: Unique identifier for the API
- `apiTitle`: Human-readable API title
- `apiDescription`: Description of API purpose and capabilities
- `apiVersion`: API version (e.g., "v1", "v2")
- `apiCategory`: Category classification (e.g., "data-services", "it4it", "business")
- `baseUrl`: Base URL for API endpoints
- `swagger`: URL to Swagger/OpenAPI specification
- `contactEmail`: Support contact email
- `owner`: Team or department owning the API
- `status`: Current status (active, deprecated, beta)
- `created`: Creation timestamp
- `modified`: Last modification timestamp

#### 2. Get API Swagger Specification

**Endpoint**: `GET /api-swagger`

**Purpose**: Retrieve complete OpenAPI/Swagger specification for an API.

**Query Parameters**:
- `top` (int): Maximum number of results (default: 9000)
- `skip` (int): Number of results to skip (default: 0)
- `apiName` (string, required): Specific API name
- `environment` (string): Target environment (default: "prd")

**Example Request**:
```bash
curl -X GET \
  "https://api.loreal.net/global/it4it/coe/v1/apiinfos/api/api-swagger?apiName=global-it4it-btdp-semanticservices-v1&environment=prd" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**Response Structure**:
```json
{
  "data": [
    {
      "apiName": "global-it4it-btdp-semanticservices-v1",
      "swagger": {
        "openapi": "3.0.0",
        "info": {
          "title": "BTDP Semantic Services API",
          "version": "1.0.0",
          "description": "API for semantic search...",
          "contact": {
            "email": "data-platform@loreal.com"
          }
        },
        "servers": [
          {
            "url": "https://api.loreal.net/global/it4it/btdp-semanticservices/v1"
          }
        ],
        "paths": {
          "/search": {
            "post": {
              "summary": "Search semantic index",
              "operationId": "searchSemanticIndex",
              "requestBody": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/SearchRequest"
                    }
                  }
                }
              },
              "responses": {
                "200": {
                  "description": "Successful response",
                  "content": {
                    "application/json": {
                      "schema": {
                        "$ref": "#/components/schemas/SearchResponse"
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "components": {
          "schemas": {
            "SearchRequest": {},
            "SearchResponse": {}
          },
          "securitySchemes": {
            "bearerAuth": {
              "type": "http",
              "scheme": "bearer"
            }
          }
        },
        "security": [
          {
            "bearerAuth": []
          }
        ]
      }
    }
  ]
}
```

**Swagger Structure**:
- `openapi`: OpenAPI version
- `info`: API metadata (title, version, description, contact)
- `servers`: List of server URLs
- `paths`: All available endpoints with methods, parameters, request/response schemas
- `components`: Reusable schemas, security schemes, parameters
- `security`: Global security requirements

## Authentication

### Azure OAuth 2.0 Client Credentials Flow

**OAuth Endpoint**: `https://api.loreal.net/v1/oauth20/token`

**Grant Type**: `client_credentials`

**Scope**: `api://32a1cb44-61cd-4c6b-bd8e-1ecff52de813/.default`

**Credentials Location**: Google Secret Manager
- Project: `itg-btdpsecurity-gbl-ww-pd`
- Secret: `btdp-srt-azure_app-pd`

**Secret Format**:
```json
{
  "tenant_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxxx",
  "client_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxxx",
  "client_secret": "xxxxxxxxxxxxxxxxxxxxxxxx"
}
```

**Token Request**:
```bash
curl -X POST "https://api.loreal.net/v1/oauth20/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${CLIENT_ID}" \
  -d "scope=api://32a1cb44-61cd-4c6b-bd8e-1ecff52de813/.default" \
  -d "client_secret=${CLIENT_SECRET}"
```

**Token Response**:
```json
{
  "token_type": "Bearer",
  "expires_in": 3599,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Token Usage**:
```bash
curl -X GET "${API_URL}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

## API Categories

Common API categories found in the portal:

- `data-services`: Data platform and analytics services
- `it4it`: IT service management and infrastructure
- `business`: Business application APIs
- `integration`: Integration and middleware services
- `security`: Security and authentication services
- `monitoring`: Monitoring and observability APIs

## Common API Naming Patterns

APIs typically follow this naming pattern:
```
{scope}-{domain}-{service}-{version}
```

**Examples**:
- `global-it4it-btdp-semanticservices-v1`
- `emea-commerce-orderprocessing-v2`
- `amer-hr-employeedata-v1`

**Scopes**:
- `global`: Global/worldwide services
- `emea`: Europe, Middle East, Africa
- `amer`: Americas
- `apac`: Asia-Pacific

**Domains**:
- `it4it`: IT infrastructure and services
- `commerce`: E-commerce and sales
- `hr`: Human resources
- `finance`: Financial services
- `supply-chain`: Supply chain management

## Response Codes

- `200 OK`: Successful request
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: API not found
- `500 Internal Server Error`: Server error

## Rate Limiting

Check response headers for rate limit information:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Time when limit resets

## Best Practices

1. **Cache tokens**: Access tokens are valid for ~1 hour, reuse them
2. **Handle errors**: Implement retry logic with exponential backoff
3. **Filter results**: Use specific API names when possible to reduce response size
4. **Save large responses**: Swagger specs can be very large (10k+ lines)
5. **Use pagination**: For large result sets, use `top` and `skip` parameters

## Examples

### Search for Data Platform APIs
```bash
# Get all APIs
curl -s -X GET \
  "${API_BASE_URL}/api-datas?top=9000&skip=0&environment=prd" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  | jq '.data[] | select(.apiName | contains("btdp"))'
```

### Get APIs by Category
```bash
curl -s -X GET \
  "${API_BASE_URL}/api-datas?top=9000&skip=0&environment=prd" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  | jq '.data[] | select(.apiCategory == "data-services")'
```

### Extract All Endpoints from Spec
```bash
curl -s -X GET \
  "${API_BASE_URL}/api-swagger?apiName=${API_NAME}&environment=prd" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  | jq '.data[0].swagger.paths | keys[]'
```

### Find APIs Modified Recently
```bash
curl -s -X GET \
  "${API_BASE_URL}/api-datas?top=9000&skip=0&environment=prd" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  | jq '.data[] | select(.modified > "2024-01-01") | {apiName, modified}'
```

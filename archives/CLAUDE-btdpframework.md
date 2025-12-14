### BTDP Framework (Enterprise)

**Use Case:** Data Transformation and BI, API, MCP servers, WebApp.

#### Global structure

**Directory Structure:**
```
btdp-project/
├── README.md                       # Global project description.
├── CLAUDE.md                       # Global CLAUDE.md instruction for the projects based on the framework global.
├── configuration/                  # YAML configs for data pipelines.
├── environments/                   # Environment configs (dv.json, np.json, pd.json, qa.json).
├── iac/                            # Global project terraform infrastructure.
└── modules/                        # Individual service modules.
    └── module-name/                # Independent module for a feature.
        ├── .module_type            # Module type (gcr, gcf, etc.).
        ├── api_portal_details.json # Information for API deployment (Apigee portal).
        ├── README.md               # Module description.
        ├── CLAUDE.md               # Local CLAUDE.md instruction for the modules.
        ├── configurations/         # Permissions and SQL queries.
        ├── iac/                    # Terraform code for module specific infrastructure.
        │   ├── variables.tf        # External variables injection (from the environment).
        │   ├── locals.tf           # Environment variables for Cloud Run.
        │   ├── workload.tf         # Cloud Run instance definition.
        │   ├── permissions.tf      # Permissions management.
        │   ├── mutex.tf            # Mutex infrastructure.
        │   ├── webapp.tf           # Webapp module call.
        │   └── webapp/             # WebApp.
        ├── src/                    # Standardized Python structure.
        │   ├── commons/            # Technical classes (APIs, databases, utils).
        │   │   ├── api/            # API wrapper. Only to hide the API call complexity.
        │   │   ├── database/       # Database wrapper, CRUD oriented functionality to interface with the databases.
        │   │   ├── models/         # Common models definition, transversal to all functionalities.
        │   │   └── utils/          # Various utilities classes and functions.
        │   ├── {functionality}/    # One folder per functionality, but a functionality could have several controllers or several services.
        │   │   ├── service.py      # Main business logic functionality. Can leverage direct mcp exposition through mcp.classregister and mcp.tool of the btdp_fastapi lib.
        │   │   ├── controller.py   # Controller used for API and WebApp to check input and output. The controller must always define a clean input schema and a clear output schema.
        │   │   ├── models.py       # The schema of the input and output for controllers.
        │   │   └── anything.py     # Additional functionality specific code required to properly separate the concern.
        │   └── application.py      # Dependency injection entry point.
        └── test_env.sh             # Environment variables for local testing.
```

Framework can be recognized because it has a modules folder and use Makefile and module.mk file to run the DevOps tool chain.

#### BTDP Framework and Library Path

@framework-path

#### Key Requirements
- **Framework:** `btdp_fastapi` library mandatory. See section BTDP Framework and Library Path for additional information.
- **Dependencies:** `requirements.txt` with exact versions number.
- **Template:** See section BTDP Framework and Library Path for additional information.
- **API Portal:** Proxy naming `btdp-{lowercase-title}`.
- **Environment Variables:** Sync `test_env.sh` and `iac/locals.tf`.

#### Commands

##### Global project infrastructure

Deploy the main infrastructure
```bash
make ENV=<env> deploy
```

##### Module Commands 
Clean a module.
```bash
make -f ../../module.mk ENV=<ENV> clean
```

Build module.
```bash
make -f ../../module.mk ENV=<ENV> build
```

**Note**: Build process includes automatic code formatting with `black -l 120` as part of the quality pipeline.

Deploy a module.
```bash
make -f ../../module.mk ENV=<ENV> deploy
```

Make end-to-end tests on a deployed version
```bash
make -f ../../module.mk ENV=<ENV> e2e-test
```

#### Module Creation

@framework-path.md

1. Copy from the root module
```bash
cp -r @.framework modules/your-data-extractor
cd modules/your-data-extractor
```

2. Define module type
```bash
echo "gcr" > .module_type
```

3. API information
Update `api_portal_details.json` with:
- **API Title**: Descriptive title for the API
- **API Description**: Clear description of API functionality  
- **Proxy Name**: Generate format `btdp-{lowercase-title}` (no spaces/hyphens/special chars)
  - Example: "BTDP Tartanpion Services" → `btdp-tartanpion`
- **Standard Values**:
  - `api_proxy_zone`: `"global"`
  - `api_proxy_division`: `"it4it"`
  - `deploy_on_apigee`: `false` (for backend module or MCP Servers) or `true` for real API
  - `apigee_instances`: `["emea"]`

4. Cleaning
```bash
rm -rf front.sample api_portal_details.json.sample
```


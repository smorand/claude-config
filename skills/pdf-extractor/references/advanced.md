# Advanced Usage

Advanced customization, performance tuning, and integration options for the PDF extractor.

## Custom Extraction Settings

### Modifying the Python Script

The extraction script can be customized by editing:

```bash
~/.claude/skills/pdf-extractor/scripts/src/pdf_extractor.py
```

### Available pymupdf4llm Parameters

#### Default Settings

```python
md_text = pymupdf4llm.to_markdown(
    doc,
    write_images=True,     # Extract images
    image_path=output_dir,  # Where to save images
    image_format="png",     # PNG format
    dpi=150,               # Image resolution
    page_chunks=False,     # Don't split by page
    margins=(0, 0, 0, 0),  # No margins
)
```

#### Customizable Parameters

**Image Extraction:**
```python
write_images=True    # Set to False to skip image extraction
image_format="png"   # Options: "png", "jpg", "jpeg", "ppm"
dpi=150             # Resolution: 72-300 (higher = larger files, better quality)
```

**Page Processing:**
```python
page_chunks=False   # True: Split output by page
pages=None         # Extract specific pages: [0, 1, 2] or range(5, 10)
```

**Layout Options:**
```python
hdr_info=None      # Custom header information
margins=(0,0,0,0)  # Page margins (left, top, right, bottom)
```

### Custom Image Analysis Settings

#### Model Selection

Default model: `claude-3-5-haiku@20241022`

**Available models on Vertex AI:**
```python
# Fast, cost-effective (default)
model="claude-3-5-haiku@20241022"

# Balanced performance
model="claude-3-5-sonnet@20241022"

# Most capable (highest cost)
model="claude-3-opus@20240229"
```

**Edit in script:**
```python
response = client.messages.create(
    model="claude-3-5-haiku@20241022",  # Change here
    max_tokens=500,
    messages=[...]
)
```

#### Analysis Prompt Customization

**Current prompt:**
```python
prompt = f"""Analyze this image and provide:
1. Image type (photo, diagram, chart, graph, table, screenshot, banner, logo, icon, illustration, map, or other)
2. Whether it contains significant readable text (yes/no)
3. A 2-3 sentence description of what the image shows

Context: This image is from a PDF document. {context_text}

Format your response as:
Type: [type]
Contains Text: [Yes/No]
Description: [description]"""
```

**Customize for specific use cases:**

*For technical documents:*
```python
prompt = f"""Analyze this technical diagram and provide:
1. Diagram type (architecture, flowchart, sequence, UML, network, other)
2. Main components or elements shown
3. Technical purpose and relationships

Context: {context_text}

Format: ...
"""
```

*For financial documents:*
```python
prompt = f"""Analyze this financial visualization and provide:
1. Chart type (bar, line, pie, table, other)
2. What financial metrics are shown
3. Key trends or patterns visible

Context: {context_text}

Format: ...
"""
```

#### Token Limits

```python
max_tokens=500  # Default: Good for 2-3 sentences

# Adjust based on needs:
max_tokens=200   # Shorter descriptions
max_tokens=1000  # Longer, detailed descriptions
```

### Example: High-Quality Image Extraction

```python
# In pdf_extractor.py
md_text = pymupdf4llm.to_markdown(
    doc,
    write_images=True,
    image_path=output_dir,
    image_format="png",
    dpi=300,  # High resolution (larger files)
)
```

### Example: Extract Specific Pages

```python
# Extract only pages 5-10
md_text = pymupdf4llm.to_markdown(
    doc,
    write_images=True,
    image_path=output_dir,
    pages=range(5, 11),  # Pages 5-10 (0-indexed)
)
```

## Performance Tuning

### Optimization Strategies

#### 1. Parallel Image Analysis

For PDFs with many images, process images in parallel:

```python
from concurrent.futures import ThreadPoolExecutor
import os

def analyze_image_parallel(image_path, context, client):
    # Analysis code here
    pass

# Process images in parallel (max 5 concurrent)
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = []
    for img_path in image_files:
        future = executor.submit(analyze_image_parallel, img_path, context, client)
        futures.append(future)

    results = [f.result() for f in futures]
```

**Benefits:**
- 5x faster for PDFs with many images
- Better API utilization

**Considerations:**
- API rate limits
- Increased memory usage
- Network bandwidth

#### 2. Caching Image Analysis

Cache analysis results to avoid re-analyzing:

```python
import hashlib
import json

def get_image_hash(image_path):
    with open(image_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def analyze_with_cache(image_path, cache_dir=".image_cache"):
    img_hash = get_image_hash(image_path)
    cache_file = os.path.join(cache_dir, f"{img_hash}.json")

    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)

    # Perform analysis
    result = analyze_image(image_path)

    # Cache result
    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(result, f)

    return result
```

#### 3. Skip Analysis for Small Images

Skip likely decorative images:

```python
from PIL import Image

def should_analyze_image(image_path, min_size=100):
    """Skip very small images (likely icons/decorative)"""
    img = Image.open(image_path)
    width, height = img.size
    return width >= min_size and height >= min_size

# Use in analysis loop
for img_file in image_files:
    if should_analyze_image(img_path, min_size=150):
        analyze_image(img_path)
    else:
        # Skip or use placeholder
        pass
```

### API Rate Limiting

#### Implement Rate Limiting

```python
import time

class RateLimiter:
    def __init__(self, calls_per_minute=60):
        self.calls_per_minute = calls_per_minute
        self.min_interval = 60.0 / calls_per_minute
        self.last_call = 0

    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()

# Use in image analysis
limiter = RateLimiter(calls_per_minute=60)

for img in images:
    limiter.wait()
    analyze_image(img)
```

### Region Selection for Performance

**Latency by region (approximate):**

| Your Location | Best Region | Latency |
|---------------|-------------|---------|
| Europe | `europe-west1` | ~20-50ms |
| US East Coast | `us-east1` | ~20-50ms |
| US West Coast | `us-west1` | ~20-50ms |
| US Central | `us-central1` | ~30-60ms |
| Asia Pacific | `asia-southeast1` | ~50-100ms |

**Set region for best performance:**
```bash
export GCP_REGION="europe-west1"  # Europe
export GCP_REGION="us-central1"   # US
```

## Integration with Other Tools

### Integration 1: Automated Workflow with Make/Rake

**Makefile example:**

```makefile
# Makefile for PDF processing

PDF_DIR := ~/Downloads
OUTPUT_DIR := ~/analysis
EXTRACTOR := ~/.claude/skills/pdf-extractor/scripts/run.sh

.PHONY: all extract clean

all: extract

extract:
	@for pdf in $(PDF_DIR)/*.pdf; do \
		echo "Processing $$pdf..."; \
		$(EXTRACTOR) pdf_extractor "$$pdf" $(OUTPUT_DIR); \
	done

clean:
	rm -rf $(OUTPUT_DIR)/*

list:
	@find $(OUTPUT_DIR) -name "*.md" -type f
```

**Usage:**
```bash
make extract  # Extract all PDFs
make list     # List all markdown files
make clean    # Clean output directory
```

### Integration 2: Python Script Integration

```python
import subprocess
import os

def extract_pdf(pdf_path, output_dir=None):
    """Extract PDF using the skill script"""
    script_path = os.path.expanduser("~/.claude/skills/pdf-extractor/scripts/run.sh")

    cmd = [script_path, "pdf_extractor", pdf_path]
    if output_dir:
        cmd.append(output_dir)

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def get_extraction_path(pdf_path, output_dir=None):
    """Get the expected extraction directory path"""
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    if output_dir:
        return os.path.join(output_dir, pdf_name)
    else:
        return os.path.join(os.path.dirname(pdf_path), pdf_name)

# Use in workflow
pdf_file = "~/Downloads/report.pdf"
extract_pdf(pdf_file)

extraction_dir = get_extraction_path(pdf_file)
document_path = os.path.join(extraction_dir, "document.md")
images_path = os.path.join(extraction_dir, "images.md")

# Read and process
with open(document_path) as f:
    content = f.read()
```

### Integration 3: Shell Script Workflow

```bash
#!/bin/bash
# pdf_workflow.sh - Automated PDF processing workflow

set -e

PDF_PATH="$1"
OUTPUT_DIR="${2:-~/analysis}"
EXTRACTOR="$HOME/.claude/skills/pdf-extractor/scripts/run.sh"

# Extract PDF
echo "Extracting PDF..."
$EXTRACTOR pdf_extractor "$PDF_PATH" "$OUTPUT_DIR"

# Get extraction directory
PDF_NAME=$(basename "$PDF_PATH" .pdf)
EXTRACT_DIR="$OUTPUT_DIR/$PDF_NAME"

# Process extracted content
echo "Processing content..."

# Filter out decorative images
grep -v "banner\|logo" "$EXTRACT_DIR/images.md" > "$EXTRACT_DIR/images_filtered.md"

# Extract chart descriptions
grep -A 15 "**Type:** chart" "$EXTRACT_DIR/images_filtered.md" > "$EXTRACT_DIR/charts.md"

# Create summary
{
    echo "# Summary of $PDF_NAME"
    echo ""
    echo "## Document Structure"
    grep "^#" "$EXTRACT_DIR/document.md"
    echo ""
    echo "## Key Charts"
    cat "$EXTRACT_DIR/charts.md"
} > "$EXTRACT_DIR/summary.md"

echo "Complete! Summary: $EXTRACT_DIR/summary.md"
```

**Usage:**
```bash
chmod +x pdf_workflow.sh
./pdf_workflow.sh ~/Downloads/report.pdf ~/analysis
```

### Integration 4: Web API Endpoint

Create a simple API for PDF extraction:

```python
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_pdf():
    pdf_path = request.json.get('pdf_path')
    output_dir = request.json.get('output_dir', '/tmp/extractions')

    script = os.path.expanduser("~/.claude/skills/pdf-extractor/scripts/run.sh")

    try:
        result = subprocess.run(
            [script, "pdf_extractor", pdf_path, output_dir],
            capture_output=True,
            text=True,
            timeout=300
        )

        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        extract_path = os.path.join(output_dir, pdf_name)

        # Read extracted content
        with open(f"{extract_path}/document.md") as f:
            document = f.read()
        with open(f"{extract_path}/images.md") as f:
            images = f.read()

        return jsonify({
            'success': True,
            'document': document,
            'images_catalog': images,
            'extraction_path': extract_path
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
```

**Usage:**
```bash
curl -X POST http://localhost:5000/extract \
    -H "Content-Type: application/json" \
    -d '{"pdf_path": "/path/to/document.pdf"}'
```

## Custom Output Formats

### Convert to Different Formats

#### HTML Output

```python
import markdown

def md_to_html(md_file, html_file):
    """Convert markdown to HTML"""
    with open(md_file) as f:
        md_content = f.read()

    html = markdown.markdown(md_content, extensions=['extra', 'codehilite'])

    with open(html_file, 'w') as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
{html}
</body>
</html>
        """)

# Use after extraction
md_to_html("document.md", "document.html")
```

#### JSON Output

```python
import json
import re

def parse_images_catalog(images_md):
    """Parse images.md into structured JSON"""
    images = []

    # Split by image sections
    sections = re.split(r'^## Image \d+:', images_md, flags=re.MULTILINE)

    for section in sections[1:]:  # Skip header
        img = {}

        # Extract fields
        path = re.search(r'\*\*Path:\*\* `([^`]+)`', section)
        img_type = re.search(r'\*\*Type:\*\* (\w+)', section)
        has_text = re.search(r'\*\*Contains Text:\*\* (Yes|No)', section)
        desc = re.search(r'\*\*Description:\*\*\s+(.+?)\s+\*\*Preview', section, re.DOTALL)

        if path:
            img['path'] = path.group(1)
        if img_type:
            img['type'] = img_type.group(1)
        if has_text:
            img['has_text'] = has_text.group(1) == 'Yes'
        if desc:
            img['description'] = desc.group(1).strip()

        images.append(img)

    return images

# Use after extraction
with open("images.md") as f:
    catalog = parse_images_catalog(f.read())

with open("images.json", 'w') as f:
    json.dump(catalog, f, indent=2)
```

### Custom Image Catalog Format

Create CSV format:

```python
import csv
import re

def images_to_csv(images_md, csv_file):
    """Convert images.md to CSV"""
    images = parse_images_catalog(images_md)  # From above

    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['path', 'type', 'has_text', 'description'])
        writer.writeheader()
        writer.writerows(images)

# Use after extraction
with open("images.md") as f:
    images_to_csv(f.read(), "images.csv")
```

## Monitoring and Logging

### Add Detailed Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_extractor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in script
logger.info(f"Starting extraction of {pdf_path}")
logger.info(f"Analyzing image {idx + 1}/{len(images)}: {img_file}")
logger.error(f"Failed to analyze {img_file}: {error}")
logger.info(f"Extraction complete. Output: {output_dir}")
```

### Track API Usage

```python
import time
import json

class APIUsageTracker:
    def __init__(self, log_file='api_usage.json'):
        self.log_file = log_file
        self.usage = []

    def log_call(self, image_path, tokens_used, duration):
        self.usage.append({
            'timestamp': time.time(),
            'image': image_path,
            'tokens': tokens_used,
            'duration': duration
        })

    def save(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.usage, f, indent=2)

    def summary(self):
        total_calls = len(self.usage)
        total_tokens = sum(u['tokens'] for u in self.usage)
        total_duration = sum(u['duration'] for u in self.usage)

        return {
            'total_calls': total_calls,
            'total_tokens': total_tokens,
            'total_duration': total_duration,
            'avg_duration': total_duration / total_calls if total_calls else 0
        }

# Use in image analysis
tracker = APIUsageTracker()

start = time.time()
response = analyze_image(img_path)
duration = time.time() - start

tracker.log_call(img_path, response.usage.total_tokens, duration)
tracker.save()

print(tracker.summary())
```

## Error Recovery and Robustness

### Retry Logic for API Calls

```python
import time

def analyze_with_retry(image_path, max_retries=3):
    """Analyze image with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            return analyze_image(image_path)
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} attempts: {e}")
                return None

            wait_time = 2 ** attempt  # Exponential backoff
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
            time.sleep(wait_time)
```

### Graceful Degradation

```python
def analyze_image_safe(image_path):
    """Analyze with fallback to basic info on failure"""
    try:
        return analyze_image(image_path)
    except Exception as e:
        logger.warning(f"AI analysis failed for {image_path}: {e}")

        # Fallback to basic info
        from PIL import Image
        img = Image.open(image_path)
        width, height = img.size

        return {
            'type': 'other',
            'has_text': False,
            'description': f'Image could not be analyzed automatically. Size: {width}x{height}px'
        }
```

## Custom Features

### Add Image Similarity Detection

Detect duplicate or similar images:

```python
from PIL import Image
import imagehash

def get_image_hash(image_path):
    """Get perceptual hash of image"""
    img = Image.open(image_path)
    return imagehash.average_hash(img)

def find_similar_images(image_files, threshold=5):
    """Find groups of similar images"""
    hashes = [(f, get_image_hash(f)) for f in image_files]
    similar_groups = []

    for i, (file1, hash1) in enumerate(hashes):
        group = [file1]
        for file2, hash2 in hashes[i+1:]:
            if hash1 - hash2 < threshold:  # Similar if diff < threshold
                group.append(file2)

        if len(group) > 1:
            similar_groups.append(group)

    return similar_groups
```

### Add Text Extraction from Images (OCR)

For images with text:

```python
import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    """Extract text using OCR"""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

# Use for images marked as containing text
if image_has_text:
    ocr_text = extract_text_from_image(img_path)
    # Add to catalog
```

## Cost Optimization

### Estimate Costs

```python
def estimate_extraction_cost(pdf_path):
    """Estimate API cost for extraction"""
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)

    # Count images
    image_count = 0
    for page in doc:
        image_count += len(page.get_images())

    # Estimate tokens per image
    tokens_per_image = 500
    total_tokens = image_count * tokens_per_image

    # Haiku pricing (example: $0.25 per 1M input tokens)
    cost_per_million = 0.25
    estimated_cost = (total_tokens / 1_000_000) * cost_per_million

    return {
        'image_count': image_count,
        'estimated_tokens': total_tokens,
        'estimated_cost_usd': estimated_cost
    }

# Use before extraction
estimate = estimate_extraction_cost("large_document.pdf")
print(f"Estimated cost: ${estimate['estimated_cost_usd']:.4f}")
```

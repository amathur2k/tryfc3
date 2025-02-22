import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# API Configuration
API_ENDPOINT = "http://ec2-35-90-90-3.us-west-2.compute.amazonaws.com:3002/v1/extract"
API_STATUS_BASE = "http://ec2-35-90-90-3.us-west-2.compute.amazonaws.com:3002/v1/extract/"

# Schema for the API request
API_SCHEMA = {
    "type": "object",
    "properties": {
        "marketing_statement": {
            "type": "string"
        },
        "pictures": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": [
        "marketing_statement"
    ]
} 
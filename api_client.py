import requests
import time
import logging
from typing import Dict, Any
from config import API_ENDPOINT, API_STATUS_BASE, API_SCHEMA

logger = logging.getLogger(__name__)

class APIClient:
    @staticmethod
    def create_prompt(word_count: int, image_count: int) -> str:
        prompt = (
            f"Create a summary of approximately {word_count} words about the services "
            f"provided by the company. On the basis of this summary craft a marketing "
            f"statement in the first person. Extract {image_count} relevant pictures "
            f"from the profile to showcase and complement it. Order these in order of "
            f"the ones which appear earliest to the last."
        )
        logger.info(f"Created prompt with word_count={word_count}, image_count={image_count}")
        return prompt

    @staticmethod
    def get_status(request_id: str, max_retries: int = 30) -> Dict[str, Any]:
        """Poll the status endpoint until success or max retries reached"""
        status_url = f"{API_STATUS_BASE}{request_id}"
        retries = 0
        logger.info(f"Starting status polling for request_id: {request_id}")

        while retries < max_retries:
            try:
                logger.debug(f"Polling attempt {retries + 1}/{max_retries}")
                response = requests.get(status_url)
                response.raise_for_status()
                result = response.json()

                # Check if the request is still processing
                if result.get("status") == "processing":
                    logger.info(f"Request still processing, waiting 2 seconds (attempt {retries + 1})")
                    time.sleep(2)
                    retries += 1
                    continue

                # If not processing, return the result
                logger.info("Received final response from status endpoint")
                return {"success": True, "response": result}

            except requests.RequestException as e:
                error_msg = f"Status check failed: {str(e)}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}

        error_msg = "Maximum retries reached while waiting for processing to complete"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}

    @staticmethod
    def extract_content(url: str, word_count: int, image_count: int) -> Dict[str, Any]:
        try:
            logger.info(f"Starting content extraction for URL: {url}")
            
            # Initial POST request
            payload = {
                "urls": [url],
                "prompt": APIClient.create_prompt(word_count, image_count),
                "schema": API_SCHEMA
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            logger.info("Sending initial POST request")
            response = requests.post(API_ENDPOINT, json=payload, headers=headers)
            response.raise_for_status()
            initial_response = response.json()

            if not initial_response.get("success"):
                error_msg = "Initial request failed"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}

            # Get the request ID
            request_id = initial_response.get("id")
            if not request_id:
                error_msg = "No request ID received"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}

            logger.info(f"Received request ID: {request_id}")
            
            # Poll for results
            return APIClient.get_status(request_id)
            
        except requests.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg} 
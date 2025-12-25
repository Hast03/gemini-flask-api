# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import google.generativeai as genai
# # import os
# # import json
# # import logging
# # from datetime import datetime

# # app = Flask(__name__)
# # CORS(app)

# # # Configure logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # # Configure Gemini API
# # genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# # @app.route('/')
# # def home():
# #     return jsonify({
# #         "message": "Gemini Flask API is running!",
# #         "endpoints": ["/generate-subtasks"],
# #         "status": "active"
# #     })

# # @app.route('/generate-subtasks', methods=['POST'])
# # def generate_subtasks():
# #     try:
# #         # Get request data
# #         data = request.get_json()
        
# #         if not data:
# #             return jsonify({"error": "No JSON data provided"}), 400
        
# #         # Extract parameters
# #         task_title = data.get('taskTitle', '').strip()
# #         task_description = data.get('taskDescription', '').strip()
# #         due_date = data.get('dueDate', '')
# #         effort = data.get('effort', 'Medium')
        
# #         if not task_title:
# #             return jsonify({"error": "Task title is required"}), 400
        
# #         # Build prompt
# #         prompt = build_prompt(task_title, task_description, due_date, effort)
# #         logger.info(f"Generated prompt for task: {task_title}")
        
# #         # Generate content using Gemini
# #         model = genai.GenerativeModel('gemini-pro')
# #         response = model.generate_content(prompt)
        
# #         if not response or not response.text:
# #             logger.error("Empty response from Gemini API")
# #             return jsonify({"error": "Empty response from AI", "subtasks": get_fallback_subtasks()}), 500
        
# #         # Parse subtasks from response
# #         subtasks = parse_subtasks_from_response(response.text)
        
# #         if not subtasks:
# #             logger.warning("Failed to parse subtasks, using fallback")
# #             return jsonify({
# #                 "message": "Used fallback subtasks due to parsing issues",
# #                 "subtasks": get_fallback_subtasks()
# #             })
        
# #         logger.info(f"Successfully generated {len(subtasks)} subtasks")
# #         return jsonify({
# #             "message": "Subtasks generated successfully",
# #             "subtasks": subtasks
# #         })
        
# #     except Exception as e:
# #         logger.error(f"Error generating subtasks: {str(e)}")
# #         return jsonify({
# #             "error": f"Failed to generate subtasks: {str(e)}",
# #             "subtasks": get_fallback_subtasks()
# #         }), 500

# # def build_prompt(task_title, task_description, due_date, effort):
# #     prompt = f"""You are an expert task breakdown assistant. Break down the given task into 3 to 5 actionable subtasks.

# # Task Title: {task_title}
# # """
    
# #     if task_description:
# #         prompt += f"Task Description: {task_description}\n"
    
# #     if due_date:
# #         prompt += f"Due Date: {due_date}\n"
    
# #     prompt += f"Effort Level: {effort}\n\n"
    
# #     prompt += """IMPORTANT: Respond with ONLY a valid JSON array. No other text, explanations, or markdown formatting.

# # JSON format required:
# # [
# #   {
# #     "title": "Subtask name",
# #     "description": "Brief description of what needs to be done",
# #     "estimatedTime": "2 hours"
# #   }
# # ]

# # Make sure the estimatedTime format is consistent (e.g., '1 hour', '30 minutes', '2 hours')."""
    
# #     return prompt

# # def parse_subtasks_from_response(response_text):
# #     try:
# #         # Clean the response text
# #         cleaned_text = response_text.strip()
        
# #         # Find JSON array boundaries
# #         json_start = cleaned_text.find('[')
# #         json_end = cleaned_text.rfind(']')
        
# #         if json_start == -1 or json_end == -1 or json_end <= json_start:
# #             logger.warning("No valid JSON array found in response")
# #             return None
        
# #         json_text = cleaned_text[json_start:json_end + 1]
# #         logger.info(f"Extracted JSON: {json_text}")
        
# #         # Parse JSON
# #         subtasks_data = json.loads(json_text)
        
# #         if not isinstance(subtasks_data, list):
# #             logger.warning("Parsed JSON is not a list")
# #             return None
        
# #         # Validate and format subtasks
# #         subtasks = []
# #         for item in subtasks_data:
# #             if isinstance(item, dict) and 'title' in item:
# #                 subtask = {
# #                     'title': item.get('title', '').strip(),
# #                     'description': item.get('description', '').strip(),
# #                     'estimatedTime': item.get('estimatedTime', '1 hour').strip()
# #                 }
# #                 if subtask['title']:
# #                     subtasks.append(subtask)
        
# #         return subtasks if subtasks else None
        
# #     except json.JSONDecodeError as e:
# #         logger.error(f"JSON parsing error: {str(e)}")
# #         return None
# #     except Exception as e:
# #         logger.error(f"Error parsing subtasks: {str(e)}")
# #         return None

# # def get_fallback_subtasks():
# #     return [
# #         {
# #             "title": "Analyze Requirements",
# #             "description": "Understand the core objectives and deliverables.",
# #             "estimatedTime": "1 hour"
# #         },
# #         {
# #             "title": "Plan Execution",
# #             "description": "Outline the steps and resources needed.",
# #             "estimatedTime": "30 minutes"
# #         },
# #         {
# #             "title": "Execute Main Tasks",
# #             "description": "Implement the core work required.",
# #             "estimatedTime": "2 hours"
# #         },
# #         {
# #             "title": "Review and Refine",
# #             "description": "Check for completeness and accuracy.",
# #             "estimatedTime": "45 minutes"
# #         }
# #     ]

# # @app.errorhandler(404)
# # def not_found(error):
# #     return jsonify({"error": "Endpoint not found"}), 404

# # @app.errorhandler(500)
# # def internal_error(error):
# #     return jsonify({"error": "Internal server error"}), 500

# # if __name__ == '__main__':
# #     port = int(os.environ.get('PORT', 5000))
# #     app.run(host='0.0.0.0', port=port, debug=False)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import os
# import json
# import logging

# # ---------------- Flask App Setup ----------------
# app = Flask(__name__)
# CORS(app)

# # ---------------- Logging Setup ----------------
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # ---------------- Gemini API Setup ----------------
# # Ensure GEMINI_API_KEY is set in your environment variables
# genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# # ---------------- Home Endpoint ----------------
# @app.route('/')
# def home():
#     return jsonify({
#         "message": "Gemini Flask API is running!",
#         "endpoints": ["/generate-subtasks", "/list-models"],
#         "status": "active"
#     })

# # ---------------- List Models Endpoint ----------------
# @app.route('/list-models', methods=['GET'])
# def list_available_models():
#     """
#     Lists the Gemini models available to the configured API key.
#     This helps in debugging 404 errors for model names.
#     """
#     try:
#         available_models = []
#         logger.info("Attempting to list available models...")
#         for m in genai.list_models():
#             if "generateContent" in m.supported_generation_methods:
#                 available_models.append({
#                     "name": m.name,
#                     "supported_methods": list(m.supported_generation_methods),
#                     "description": m.description
#                 })
#         logger.info(f"Found {len(available_models)} models capable of generating content.")
#         return jsonify({
#             "message": "Available Gemini Models capable of generating content",
#             "models": available_models
#         })
#     except Exception as e:
#         logger.error(f"Error listing models: {str(e)}")
#         return jsonify({
#             "error": f"Failed to list models: {str(e)}. Please check your API key and network connection."
#         }), 500

# # ---------------- Generate Subtasks Endpoint ----------------
# @app.route('/generate-subtasks', methods=['POST'])
# def generate_subtasks():
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "No JSON data provided"}), 400

#         task_title = data.get('taskTitle', '').strip()
#         task_description = data.get('taskDescription', '').strip()
#         due_date = data.get('dueDate', '')
#         effort = data.get('effort', 'Medium')

#         if not task_title:
#             return jsonify({"error": "Task title is required"}), 400

#         prompt = build_prompt(task_title, task_description, due_date, effort)
#         logger.info(f"Generated prompt for task: {task_title}")

#         # ---------------- Use Valid Gemini Model ----------------
#         # Change 'YOUR_MODEL_NAME' to the exact model from /list-models output
#         # model = genai.GenerativeModel('gemini-2.5-pro') # Example alternative model
#         model = genai.GenerativeModel('gemini-pro-latest')
#         response = model.generate_content(prompt)

#         if not response or not response.text:
#             logger.error("Empty response from Gemini API")
#             return jsonify({
#                 "error": "Empty response from AI",
#                 "subtasks": get_fallback_subtasks()
#             }), 500

#         subtasks = parse_subtasks_from_response(response.text)
#         if not subtasks:
#             logger.warning("Failed to parse subtasks, using fallback")
#             return jsonify({
#                 "message": "Used fallback subtasks due to parsing issues",
#                 "subtasks": get_fallback_subtasks()
#             })

#         logger.info(f"Successfully generated {len(subtasks)} subtasks")
#         return jsonify({
#             "message": "Subtasks generated successfully",
#             "subtasks": subtasks
#         })

#     except Exception as e:
#         logger.error(f"Error generating subtasks: {str(e)}")
#         return jsonify({
#             "error": f"Failed to generate subtasks: {str(e)}",
#             "subtasks": get_fallback_subtasks()
#         }), 500

# # ---------------- Helper Functions ----------------
# def build_prompt(task_title, task_description, due_date, effort):
#     prompt = f"""You are an expert task breakdown assistant. Break down the given task into 3 to 5 actionable subtasks.

# Task Title: {task_title}
# """
#     if task_description:
#         prompt += f"Task Description: {task_description}\n"
#     if due_date:
#         prompt += f"Due Date: {due_date}\n"
#     prompt += f"Effort Level: {effort}\n\n"
#     prompt += """IMPORTANT: Respond with ONLY a valid JSON array. No other text, explanations, or markdown formatting.

# JSON format required:
# [
#   {
#     "title": "Subtask name",
#     "description": "Brief description of what needs to be done",
#     "estimatedTime": "2 hours"
#   }
# ]

# Make sure the estimatedTime format is consistent (e.g., '1 hour', '30 minutes', '2 hours')."""
#     return prompt

# def parse_subtasks_from_response(response_text):
#     try:
#         cleaned_text = response_text.strip()
#         json_start = cleaned_text.find('[')
#         json_end = cleaned_text.rfind(']')
#         if json_start == -1 or json_end == -1 or json_end <= json_start:
#             logger.warning("No valid JSON array found in response")
#             return None

#         json_text = cleaned_text[json_start:json_end + 1]
#         subtasks_data = json.loads(json_text)
#         if not isinstance(subtasks_data, list):
#             logger.warning("Parsed JSON is not a list")
#             return None

#         subtasks = []
#         for item in subtasks_data:
#             if isinstance(item, dict) and 'title' in item:
#                 subtask = {
#                     'title': item.get('title', '').strip(),
#                     'description': item.get('description', '').strip(),
#                     'estimatedTime': item.get('estimatedTime', '1 hour').strip()
#                 }
#                 if subtask['title']:
#                     subtasks.append(subtask)
#         return subtasks if subtasks else None

#     except json.JSONDecodeError as e:
#         logger.error(f"JSON parsing error: {str(e)}")
#         return None
#     except Exception as e:
#         logger.error(f"Error parsing subtasks: {str(e)}")
#         return None

# def get_fallback_subtasks():
#     return [
#         {
#             "title": "Analyze Requirements",
#             "description": "Understand the core objectives and deliverables.",
#             "estimatedTime": "1 hour"
#         },
#         {
#             "title": "Plan Execution",
#             "description": "Outline the steps and resources needed.",
#             "estimatedTime": "30 minutes"
#         },
#         {
#             "title": "Execute Main Tasks",
#             "description": "Implement the core work required.",
#             "estimatedTime": "2 hours"
#         },
#         {
#             "title": "Review and Refine",
#             "description": "Check for completeness and accuracy.",
#             "estimatedTime": "45 minutes"
#         }
#     ]

# # ---------------- Error Handlers ----------------
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({"error": "Endpoint not found"}), 404

# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({"error": "Internal server error"}), 500

# # ---------------- Run Flask App ----------------
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=False)


from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import logging

# ---------------- Flask App Setup ----------------
app = Flask(__name__)
CORS(app)

# ---------------- Logging Setup ----------------
# This ensures logs will appear in Render
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---------------- Gemini API Setup ----------------
try:
    # Ensure GEMINI_API_KEY is set in your Render environment variables
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.critical("FATAL ERROR: GEMINI_API_KEY environment variable not found.")
    genai.configure(api_key=api_key)
    logger.info("Gemini API configured successfully.")
except Exception as e:
    logger.critical(f"FATAL ERROR during Gemini configuration: {str(e)}")


# ---------------- Home Endpoint ----------------
@app.route('/')
def home():
    return jsonify({
        "message": "Gemini Flask API is running!",
        "endpoints": ["/generate-subtasks", "/list-models"],
        "status": "active"
    })

# ---------------- List Models Endpoint (for debugging) ----------------
@app.route('/list-models', methods=['GET'])
def list_available_models():
    try:
        logger.info("Attempting to list available models...")
        models_list = [
            {"name": m.name, "supported_methods": list(m.supported_generation_methods)}
            for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
        logger.info(f"Found {len(models_list)} models capable of generating content.")
        return jsonify({"models": models_list})
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        return jsonify({"error": f"Failed to list models: {str(e)}"}), 500

# ---------------- Generate Subtasks Endpoint ----------------
@app.route('/generate-subtasks', methods=['POST'])
def generate_subtasks():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        task_title = data.get('taskTitle', '').strip()
        if not task_title:
            return jsonify({"error": "Task title is required"}), 400

        # Build the prompt using your existing helper function
        prompt = build_prompt(
            task_title,
            data.get('taskDescription', '').strip(),
            data.get('dueDate', ''),
            data.get('effort', 'Medium')
        )
        logger.info(f"Generated prompt for task: '{task_title}'")

        # Use the stable model with a high rate limit
        model = genai.GenerativeModel('models/gemini-pro-latest')

        # Enforce JSON output for reliability
        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json"
        )

        # Generate content with the new configuration
        response = model.generate_content(prompt, generation_config=generation_config)

        # This new log will show us the *entire* response object from Google.
        # If the request is blocked by safety filters, we will see it here.
        logger.info(f"RAW GEMINI RESPONSE OBJECT: {response}")

        # The check for 'response.text' is still a good safety measure
        if not response or not response.text:
            logger.error("Empty response.text from Gemini API. Check the 'RAW GEMINI RESPONSE OBJECT' log above. The request may have been blocked for safety reasons or another issue.")
            return jsonify({
                "error": "The AI returned an empty response. This can happen due to safety filters.",
                "subtasks": get_fallback_subtasks()
            }), 500
        
        logger.info(f"Response text received, attempting to parse...")
        subtasks = parse_subtasks_from_response(response.text)
        
        if not subtasks:
            logger.warning("Failed to parse valid subtasks from the response text, using fallback.")
            return jsonify({
                "message": "Used fallback subtasks due to a parsing issue.",
                "subtasks": get_fallback_subtasks()
            })

        logger.info(f"Successfully generated and parsed {len(subtasks)} subtasks.")
        return jsonify({
            "message": "Subtasks generated successfully",
            "subtasks": subtasks
        })

    except Exception as e:
        # This will catch errors like invalid API keys, network issues, etc.
        logger.error(f"An exception occurred in /generate-subtasks: {str(e)}")
        return jsonify({
            "error": f"An internal server error occurred: {str(e)}",
            "subtasks": get_fallback_subtasks()
        }), 500

# ---------------- Helper Functions ----------------
def build_prompt(task_title, task_description, due_date, effort):
    prompt = f"""You are an expert task breakdown assistant. Break down the given task into 3 to 5 actionable subtasks.

Task Title: {task_title}
"""
    if task_description:
        prompt += f"Task Description: {task_description}\n"
    if due_date:
        prompt += f"Due Date: {due_date}\n"
    prompt += f"Effort Level: {effort}\n\n"
    prompt += """IMPORTANT: Respond with ONLY a valid JSON array of objects. Do not include any other text, explanations, or markdown formatting like ```json.

JSON format required:
[
  {
    "title": "Subtask name",
    "description": "Brief description of what needs to be done",
    "estimatedTime": "2 hours"
  }
]

Ensure the estimatedTime is a string like '1 hour', '30 minutes', '2 hours'."""
    return prompt

def parse_subtasks_from_response(response_text):
    try:
        subtasks_data = json.loads(response_text)
        if not isinstance(subtasks_data, list):
            logger.warning("Parsed JSON is not a list as expected.")
            return None

        subtasks = []
        for item in subtasks_data:
            if isinstance(item, dict) and 'title' in item and item.get('title'):
                subtask = {
                    'title': item.get('title', 'Untitled').strip(),
                    'description': item.get('description', '').strip(),
                    'estimatedTime': item.get('estimatedTime', 'N/A').strip()
                }
                subtasks.append(subtask)
        return subtasks if subtasks else None
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)} on text: {response_text}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during parsing: {str(e)}")
        return None

def get_fallback_subtasks():
    return [
        {"title": "Analyze Requirements", "description": "Understand the core objectives.", "estimatedTime": "1 hour"},
        {"title": "Plan Execution", "description": "Outline the steps needed.", "estimatedTime": "30 minutes"},
        {"title": "Execute Main Tasks", "description": "Implement the core work.", "estimatedTime": "2 hours"},
        {"title": "Review and Refine", "description": "Check for completeness and accuracy.", "estimatedTime": "45 minutes"}
    ]

# ---------------- Error Handlers ----------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Caught by internal_error handler: {error}")
    return jsonify({"error": "An unexpected internal server error occurred."}), 500

# ---------------- Run Flask App ----------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
from flask import Blueprint, request, jsonify
from concurrent.futures import ThreadPoolExecutor

from services.prompt_service import get_prompt
from services.openai_service import get_ai_response
from database.mongodb import history_collection


prompt_bp = Blueprint("prompt_bp", __name__)


@prompt_bp.route("/test", methods=["GET"])
def test():
    return jsonify({
        "message": "Prompt route is working"
    })


@prompt_bp.route("/api/prompt", methods=["POST"])
def process_prompt():

    data = request.get_json()

    if not data or "userInput" not in data:
        return jsonify({
            "error": "userInput is required"
        }), 400

    user_input = data["userInput"]

    try:
        template = get_prompt()

        final_prompt = template.replace(
            "{{userInput}}",
            user_input
        )

        ai_response = get_ai_response(final_prompt)

        history_collection.insert_one({
            "userInput": user_input,
            "prompt": final_prompt,
            "response": ai_response
        })

        return jsonify({
            "response": ai_response
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@prompt_bp.route("/api/prompts/batch", methods=["POST"])
def process_batch():

    data = request.get_json()

    if not data or "userInputs" not in data:
        return jsonify({
            "error": "userInputs is required"
        }), 400

    user_inputs = data["userInputs"]

    if not isinstance(user_inputs, list):
        return jsonify({
            "error": "userInputs must be a list"
        }), 400

    try:
        template = get_prompt()

        def process_one(user_input):

            final_prompt = template.replace(
                "{{userInput}}",
                user_input
            )

            ai_response = get_ai_response(final_prompt)

            history_collection.insert_one({
                "userInput": user_input,
                "prompt": final_prompt,
                "response": ai_response
            })

            return ai_response

        with ThreadPoolExecutor(
            max_workers=min(5, len(user_inputs))
        ) as executor:

            responses = list(
                executor.map(process_one, user_inputs)
            )

        return jsonify({
            "responses": responses
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
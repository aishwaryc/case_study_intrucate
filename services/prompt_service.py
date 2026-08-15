from database.mongodb import prompts_collection


def get_prompt():
    prompt = prompts_collection.find_one({"_id": "Education_Prompt"})

    if not prompt:
        raise Exception("Education_Prompt not found in MongoDB")

    return prompt["template"]
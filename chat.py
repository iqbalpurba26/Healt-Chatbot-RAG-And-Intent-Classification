import json
from fastapi import HTTPException
from langchain.callbacks import get_openai_callback
from intent_classification.predict import predict_intent
from rag.retrieval import retrieve
from rag.generate_answer import completion

def chat(prompt):
    try:
        with get_openai_callback() as cb:
            intent = predict_intent(prompt)
            information_relevant = retrieve(intent=intent, prompt=prompt)
            response = completion(information_relevant=information_relevant, prompt=prompt)

            if 'error' in intent:
                raise HTTPException(status_code=503)
            response_data = {
                "question" : prompt,
                "intent_predict": intent,
                "response":response
            }
            response_json = json.dumps(response_data, indent=4)
            return response_json
    except Exception as e:
        error_message = str(e)
        return json.dumps({'error': error_message}, indent=4)

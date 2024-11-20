from fastapi import HTTPException, Query

def validate_prompt(text:str = Query(..., alias="input", min_length=3)):

    if not text.strip():
        raise HTTPException(status_code=400, detail="Can not empty")
    if text.replace("."," ",1).isdigit():
        raise HTTPException(status_code=400, detail="Input must not integer")
    
    return text
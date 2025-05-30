from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from .card_creator import create_anki_deck
# from .card_creator import extract_flashcards_from_apkg
from fastapi.responses import FileResponse
import logging
from pathlib import Path 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class TopicData(BaseModel):
    id: str
    subject: str
    title: str
    content: str

@app.post("/create_card")
async def create_card(data: TopicData):
    logger.info(f"Creating card for topic: {data.title}")
    result = create_anki_deck(data.id, data.subject, data.title, data.content)
    
    if result["status"] != "success":
        error_detail = {
            "message": "Flashcard generation failed",
            "error": result.get("error"),
            "type": result.get("type")
        }
        logger.error(f"Error creating Anki deck: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)
    
    # Enhanced response format
    response = {
        "metadata": {
            "deck_id": result["deck_id"],
            "download_link": result["download_link"],
            "file_path": result["apkg_path"]
        },
        "flashcards": result.get("flashcards", []),
        "status": "success"
    }
    
    logger.info(f"Successfully created deck: {result['deck_id']}")
    return response

# @app.get("/cards/{deck_name}")
# async def get_flashcards(deck_name: str):
#     result = extract_flashcards_from_apkg(deck_name)

#     if result["status"] != "success":
#         raise HTTPException(status_code=404, detail=result["error"])

#     return result

@app.get("/download/{deck_name}")
async def download_deck(deck_name: str, request: Request):
    deck_path = Path(__file__).parent.parent / "anki" / f"{deck_name}.apkg"
    
    if not deck_path.exists():
        raise HTTPException(status_code=404, detail="Deck file not found")
    
    # Return JSON metadata if client prefers JSON
    if "application/json" in request.headers.get("accept", ""):
        return {
            "deck_name": deck_name,
            "file_size": deck_path.stat().st_size,
            "download_url": f"/download/{deck_name}",
            "direct_download": True
        }
    
    return FileResponse(
        str(deck_path),
        media_type="application/octet-stream",
        filename=f"{deck_name}.apkg"
    )
    
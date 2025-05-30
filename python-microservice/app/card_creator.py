import os
import sys
from pathlib import Path

# Add the Anki submodule to Python path
anki_path = str(Path(__file__).parent.parent / "anki" / "pylib")
if anki_path not in sys.path:
    sys.path.append(anki_path)

from anki.collection import Collection
from anki.exporting import AnkiPackageExporter

def create_anki_deck(topic_id, subject, title, content):
    try:
        os.makedirs("anki", exist_ok=True)

        col_path = os.path.abspath("anki/user_collection.anki2")
        col = Collection(col_path)

        # Get or create deck
        deck_name = f"{subject}_{topic_id}"
        deck_id = col.decks.id(deck_name)
        col.decks.select(deck_id)

        # Get or create Basic note type
        model = col.models.by_name("Basic")
        if model is None:
            model = col.models.new("Basic")
            col.models.add(model)

        model['did'] = deck_id
        col.models.set_current(model)

        # Split content into sentences for multiple flashcards
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        flashcards = []

        for i, sentence in enumerate(sentences[:4]):  # Limit to 4 cards
            note = col.new_note(model)
            note.fields[0] = f"Question {i+1}: About {title}"  # Front
            note.fields[1] = sentence  # Back
            note.add_tag(subject.lower())

            if not col.add_note(note, deck_id):
                continue

            flashcards.append({
                "id": f"card_{i+1}",
                "front": note.fields[0],
                "back": note.fields[1],
                "tags": note.tags,
            })

        col.save()

        apkg_path = os.path.abspath(f"anki/{deck_name}.apkg")
        if os.path.exists(apkg_path):
            os.remove(apkg_path)

        exporter = AnkiPackageExporter(col)
        exporter.exportInto(apkg_path)
        col.close()

        return {
            "status": "success",
            "deck_id": deck_name,
            "apkg_path": apkg_path,
            "download_link": f"http://localhost:8080/download/{deck_name}",
            "flashcards": flashcards,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "type": type(e).__name__,
        }

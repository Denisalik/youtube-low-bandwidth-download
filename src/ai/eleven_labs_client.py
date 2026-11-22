import json
import os
import re
from io import BytesIO
from pathlib import Path

from elevenlabs import ElevenLabs
from sqlmodel import Session

from src.db.engine import engine
from src.entity import File, FileState


class ELClient:
    def __init__(self, token: str) -> None:
        self.token = token

        self.elevenlabs = ElevenLabs(api_key=token)
        self.file_folder = Path("/data/files")

    def audio_file_to_text(self, file_id: int, filename: str):
        filepath = self.file_folder / filename
        with open(filepath, "rb") as f:
            audio_data = BytesIO(f.read())
            response = self.elevenlabs.speech_to_text.convert(
                file=audio_data, model_id="scribe_v3", tag_audio_events=True, diarize=True
            )
            text: str = json.loads(response.json()).get("text")
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            with open(self.file_folder / txt_filename, "w") as f:
                # find everything except punctuation + punctuation, which is a line
                # punctuation can be 0 or multiple of punctuation signs
                lines = [line.strip() for line in re.findall(r"[^!?.]+[!?.]*", text)]
                lines = [line for line in lines if line]
                f.write("\n".join(lines))

            with Session(engine) as session:
                file = session.get(File, file_id)
                if file is None:
                    raise Exception("It is not possible in ELClient.audio_file_to_text")
                file.state = FileState.end_text
                file.text_transcription_file = txt_filename
                session.add(file)
                session.commit()

import base64
import json
import os
from pathlib import Path

import requests
from sqlmodel import Session

from src.db.engine import engine
from src.entity import File, FileState


class ORClient:
    def __init__(self, token: str, base_url: str) -> None:
        self.token = token
        self.authorization_header = "Bearer " + token
        self.base_url = base_url
        self.file_folder = Path("/data/files")

    def audio_file_to_text(self, file_id: int, filename: str):
        filepath = self.file_folder / filename
        url = self.base_url + "audio/transcriptions"
        with open(filepath, "rb") as f:
            base64_audio = base64.b64encode(f.read()).decode("utf-8")
            response = requests.post(
                url=url,
                headers={
                    "Authorization": self.authorization_header,
                    "Content-Type": "application/json",
                },
                data=json.dumps(
                    {
                        "model": "elevenlabs/scribe-v2",
                        "input_audio": {"data": base64_audio, "format": "m4a"},
                    }
                ),
            )
            text = response.json().get("text", response.status_code)
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            with open(self.file_folder / txt_filename, "w") as f:
                f.write(text)

            with Session(engine) as session:
                file = session.get(File, file_id)
                if file is None:
                    raise Exception("It is not possible in ORClient.audio_file_to_text")
                file.state = FileState.end_text
                file.text_transcription_file = txt_filename
                session.add(file)
                session.commit()

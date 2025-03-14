from datetime import date
from garminworkouts.models.date import get_date


class Note:
    def __init__(self, config, race=date.today()) -> None:
        self.config = config
        self.name: str = config.get('name', '')
        self.content: str = config.get('content', '')
        self.race: date = race

    def get_note_name(self) -> str:
        return str(self.config.get('name', ''))

    def get_note_content(self) -> str:
        return str(self.config.get('content', ''))

    def create_note(self, id=None, date=None) -> dict:
        return {
            'id': id,
            'noteName': self.name,
            'content': self.content,
            'date': date
        }

    @staticmethod
    def extract_note_id(note) -> str:
        return note.get('id', '')

    def print_note_summary(self) -> None:
        print(f"{self.config.get('id', '')} {self.name:20} {self.content}")

    def get_note_date(self) -> tuple[date, int, int]:
        return get_date(self.config.get('name', ''), self.race, None)

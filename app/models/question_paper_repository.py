from typing import List, Dict, Any

from app import db
from app.models.question_paper import QuestionPaper


class QuestionPaperRepo:
    @staticmethod
    def create(subject, chapter, question, options):
        new_record = QuestionPaper(subject=subject, chapter=chapter, question=question, options=options)
        db.session.add(new_record)
        db.session.commit()
        return new_record

    @staticmethod
    def bulk_create(question_papers: List[Dict[str, Any]]) -> List[QuestionPaper]:
        new_records = []
        for paper in question_papers:
            new_record = QuestionPaper(
                subject=paper['subject'],
                chapter=paper.get('chapter'),
                question=paper['question'],
                options=paper.get('options')
            )
            new_records.append(new_record)

        db.session.bulk_save_objects(new_records)
        db.session.commit()
        return new_records

    @staticmethod
    def get(record_id):
        return QuestionPaper.query.get(record_id)

    @staticmethod
    def get_by_chapter(chapter_name):
        return (db.session.query(QuestionPaper)
                .filter_by(chapter=chapter_name)
                .all()
                )

    @staticmethod
    def update(record_id, **kwargs):
        record = QuestionPaper.query.get(record_id)
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
            db.session.commit()
            return record
        return None

    @staticmethod
    def delete(record_id):
        record = QuestionPaper.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        return False

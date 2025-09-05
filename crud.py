from sqlalchemy.orm import Session
from app.models import Spec, Report, ValuesLog, FeedbackLog
from typing import Dict, Any, Optional

def save_spec(db: Session, prompt: str, spec: Dict[str, Any]) -> Spec:
    db_spec = Spec(prompt=prompt, spec=spec)
    db.add(db_spec)
    db.commit()
    db.refresh(db_spec)
    return db_spec

def save_report(db: Session, spec_id: str, evaluation: Dict[str, Any], score: int) -> Report:
    db_report = Report(spec_id=spec_id, evaluation=evaluation, score=score)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_report(db: Session, report_id: str) -> Report:
    return db.query(Report).filter(Report.id == report_id).first()

def save_feedback_log(db: Session, spec_id: Optional[str], iteration: int, 
                     before: Dict[str, Any], after: Dict[str, Any], 
                     feedback: Dict[str, Any], reward: int) -> FeedbackLog:
    db_feedback = FeedbackLog(
        spec_id=spec_id, iteration=iteration, before=before, 
        after=after, feedback=feedback, reward=reward
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_spec(db: Session, spec_id: str) -> Spec:
    return db.query(Spec).filter(Spec.id == spec_id).first()

def save_values_log(db: Session, honesty: str = None, integrity: str = None, 
                   discipline: str = None, gratitude: str = None) -> ValuesLog:
    db_values = ValuesLog(honesty=honesty, integrity=integrity, 
                         discipline=discipline, gratitude=gratitude)
    db.add(db_values)
    db.commit()
    db.refresh(db_values)
    return db_values
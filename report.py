import json
import pathlib
from datetime import datetime

def write_json(report_dir, name, payload):
    """Write JSON report"""
    p = pathlib.Path(report_dir) / f"{name}.json"
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
    return p

def write_txt(report_dir, name, payload):
    """Write enhanced text report with LLM feedback"""
    lines = [
        f"# Report: {name}",
        f"Time: {datetime.now().isoformat()}",
        f"Score: {payload.get('spec_score', 0)}/10",
        f"Valid: {payload.get('valid', False)}",
        f"Notes: {payload.get('validation_error', 'No issues')}"
    ]
    
    # Add LLM feedback if available
    llm_feedback = payload.get('llm_feedback')
    if llm_feedback:
        lines.extend([
            "",
            "## LLM Analysis",
            f"Assessment: {llm_feedback.get('overall_assessment', 'N/A')}",
            f"Completeness: {llm_feedback.get('quality_analysis', {}).get('completeness', 0):.1f}%",
            f"Realism: {llm_feedback.get('quality_analysis', {}).get('realism', 0):.1f}%"
        ])
        
        critiques = llm_feedback.get('critiques', [])
        if critiques:
            lines.extend(["", "## Critiques"])
            for i, critique in enumerate(critiques[:3], 1):
                lines.append(f"{i}. {critique}")
        
        suggestions = llm_feedback.get('improvement_suggestions', [])
        if suggestions:
            lines.extend(["", "## Suggestions"])
            for i, suggestion in enumerate(suggestions[:3], 1):
                lines.append(f"{i}. {suggestion}")
    
    p = pathlib.Path(report_dir) / f"{name}.txt"
    p.write_text("\n".join(lines), encoding='utf-8')
    return p

def generate_reports(report_dir, name, evaluation_result):
    """Generate both JSON and TXT reports"""
    json_path = write_json(report_dir, name, evaluation_result)
    txt_path = write_txt(report_dir, name, evaluation_result)
    return json_path, txt_path
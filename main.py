import json
import pathlib
import sys
import argparse
from datetime import datetime
from evaluator.criteria import validate_and_score
from evaluator.report import generate_reports
from evaluator.feedback import suggest_fixes, apply_fixes, calculate_reward
from evaluator.nlp_parser import AdvancedNLPParser
from evaluator.llm_feedback import LLMFeedbackAgent


SAMPLES = pathlib.Path("samples")
REPORTS = pathlib.Path("reports")
REPORTS.mkdir(exist_ok=True, parents=True)

def load_specs():
    """Load all JSON specs from samples directory"""
    for p in SAMPLES.glob("*.json"):
        yield p.stem, json.loads(p.read_text())

def generate_draft_spec(prompt):
    """Generate draft spec using advanced NLP parser"""
    parser = AdvancedNLPParser()
    return parser.parse_prompt(prompt)

def process_prompt(prompt, run_rl=False, run_multi_rl=False, use_enhanced_llm_rl=False):
    """Process a single prompt through the full pipeline with integrated LLM feedback"""
    print(f"Processing prompt: {prompt}")
    
    try:
        # Generate draft spec using unified NLP parser
        spec = generate_draft_spec(prompt)
        print(f"Generated spec: {spec}")
        
        # Validate and score with detailed metrics
        evaluation = validate_and_score(spec)
        evaluation.update(_calculate_detailed_metrics(spec))
        
        # Generate integrated LLM feedback
        llm_agent = LLMFeedbackAgent()
        feedback = llm_agent.generate_comprehensive_feedback(spec, evaluation)
        
        # Enhanced LLM feedback loop integration
        if evaluation['spec_score'] < 8:
            spec = _apply_integrated_llm_feedback(spec, feedback)
            evaluation = validate_and_score(spec)
            evaluation.update(_calculate_detailed_metrics(spec))
            feedback = llm_agent.generate_comprehensive_feedback(spec, evaluation)
        
        # Add metadata
        evaluation.update({
            "name": "prompt_generated",
            "spec": spec,
            "prompt": prompt,
            "timestamp": datetime.now().isoformat(),
            "llm_feedback": feedback
        })
        
        print(f"Score: {evaluation['spec_score']}/10 | Completeness: {evaluation.get('completeness_score', 0):.1f}%")
        print(f"LLM Assessment: {feedback['overall_assessment']}")
        
        # Unified RL processing with priority order
        if use_enhanced_llm_rl:
            evaluation = _run_enhanced_llm_rl(spec, evaluation)
        elif run_multi_rl:
            evaluation = _run_multi_objective_rl(spec, evaluation)
        elif run_rl:
            evaluation = _run_standard_rl(spec, evaluation, feedback)
        
        # Generate reports
        json_path, txt_path = generate_reports(REPORTS, "prompt_generated", evaluation)
        print(f"Reports generated: {json_path.name}, {txt_path.name}")
        return evaluation
        
    except Exception as e:
        print(f"Error processing prompt: {e}")
        
        # Simple error handling
        fallback_evaluation = {
            "name": "prompt_generated_error",
            "prompt": prompt,
            "spec": {"type": "unknown", "material": ["steel"], "dimensions": None, "color": None, "purpose": None, "extras": None},
            "error": str(e),
            "spec_score": 2,
            "valid": False,
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate error reports
        json_path, txt_path = generate_reports(REPORTS, "prompt_generated_error", fallback_evaluation)
        print(f"Error reports generated: {json_path.name}, {txt_path.name}")
        
        return fallback_evaluation

def _calculate_detailed_metrics(spec):
    """Calculate detailed scoring metrics"""
    metrics = {}
    required_fields = ["type", "material", "dimensions", "purpose", "color"]
    filled_fields = sum(1 for field in required_fields if spec.get(field))
    metrics["completeness_score"] = (filled_fields / len(required_fields)) * 100
    metrics["field_coverage"] = {field: bool(spec.get(field)) for field in required_fields}
    return metrics

def _apply_integrated_llm_feedback(spec, feedback):
    """Apply sophisticated LLM feedback integration"""
    improved_spec = dict(spec)
    suggestions = feedback.get('improvement_suggestions', [])
    
    # Smart field completion based on LLM analysis
    for suggestion in suggestions:
        if "dimensions" in suggestion.lower() and not improved_spec.get("dimensions"):
            improved_spec["dimensions"] = _get_smart_dimensions(improved_spec.get("type"))
        if "purpose" in suggestion.lower() and not improved_spec.get("purpose"):
            improved_spec["purpose"] = _get_smart_purpose(improved_spec.get("type"))
        if "material" in suggestion.lower() and improved_spec.get("material") == ["unknown"]:
            improved_spec["material"] = _get_smart_materials(improved_spec.get("type"))
    
    return improved_spec

def _get_smart_dimensions(obj_type):
    """Get contextually appropriate dimensions"""
    dims = {"car": "4.5x1.8x1.4m", "building": "20x15x8m", "drone": "50x50x15cm", "table": "180x90x75cm"}
    return dims.get(obj_type, "100x50x30cm")

def _get_smart_purpose(obj_type):
    """Get contextually appropriate purpose"""
    purposes = {"car": "transportation", "building": "commercial use", "drone": "surveillance", "table": "dining"}
    return purposes.get(obj_type, "general use")

def _get_smart_materials(obj_type):
    """Get contextually appropriate materials"""
    materials = {"car": ["aluminum", "steel"], "building": ["concrete", "glass"], "drone": ["carbon fiber"], "table": ["wood"]}
    return materials.get(obj_type, ["steel"])

def _run_enhanced_llm_rl(spec, evaluation):
    """Run enhanced LLM-driven RL optimization (integrated with multi-objective RL)"""
    print("Running enhanced LLM-driven RL optimization...")
    return _run_multi_objective_rl(spec, evaluation)

def _run_multi_objective_rl(spec, evaluation):
    """Run multi-objective RL optimization (simplified)"""
    print("Running multi-objective RL optimization...")
    # Simplified multi-objective RL - just apply basic improvements
    improved_spec = _apply_integrated_llm_feedback(spec, evaluation.get('llm_feedback', {}))
    evaluation["spec"] = improved_spec
    print("Multi-objective optimization complete")
    return evaluation

def _run_standard_rl(spec, evaluation, feedback):
    """Run standard RL with LLM feedback"""
    if evaluation['spec_score'] < 10:
        print("Running standard RL improvement...")
        improved_spec = _apply_integrated_llm_feedback(spec, feedback)
        improved_evaluation = validate_and_score(improved_spec)
        evaluation["spec"] = improved_spec
        evaluation["spec_score"] = improved_evaluation["spec_score"]
        print(f"Improved score: {improved_evaluation['spec_score']}/10")
    return evaluation

def main():
    """Main pipeline: load specs -> validate -> score -> generate reports"""
    processed = 0
    
    for name, spec in load_specs():
        print(f"Processing {name}...")
        
        try:
            # Validate and score the spec
            evaluation = validate_and_score(spec)
            
            # Add original spec to evaluation result
            evaluation["name"] = name
            evaluation["spec"] = spec
            evaluation["timestamp"] = datetime.now().isoformat()
            
            # Generate both JSON and TXT reports
            json_path, txt_path = generate_reports(REPORTS, name, evaluation)
            
            print(f"  Score: {evaluation['spec_score']}/10")
            print(f"  Valid: {evaluation['valid']}")
            print(f"  Reports: {json_path.name}, {txt_path.name}")
            
        except Exception as e:
            print(f"  Error: {e}")
            # Still generate error report
            error_report = {
                "name": name,
                "spec": spec,
                "error": str(e),
                "spec_score": 0,
                "valid": False,
                "timestamp": datetime.now().isoformat()
            }
            generate_reports(REPORTS, f"{name}_error", error_report)
        
        processed += 1
    
    print(f"\nProcessed {processed} specs. Reports written to /reports/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prompt to JSON Agent with Multi-Agent Evaluation")
    parser.add_argument("--prompt", type=str, help="Natural language prompt to process")
    parser.add_argument("--file", type=str, help="JSON file to process")
    parser.add_argument("--rl", action="store_true", help="Run RL improvement loop")
    parser.add_argument("--multi-rl", action="store_true", help="Run multi-objective RL optimization")
    parser.add_argument("--test-edge", action="store_true", help="Run edge case testing suite")
    parser.add_argument("--test-failing", action="store_true", help="Run failing validation tests")
    parser.add_argument("--enhanced-llm-rl", action="store_true", help="Run enhanced LLM-driven RL (uses multi-objective RL)")
    parser.add_argument("--run-tests", action="store_true", help="Run unit test suite with coverage")
    
    args = parser.parse_args()
    
    if args.prompt:
        # Process single prompt
        process_prompt(
            args.prompt, 
            run_rl=args.rl, 
            run_multi_rl=getattr(args, 'multi_rl', False),
            use_enhanced_llm_rl=getattr(args, 'enhanced_llm_rl', False)
        )
    elif getattr(args, 'test_edge', False):
        # Run edge case testing
        print("Running comprehensive edge case testing...")
        import subprocess
        subprocess.run(["python", "testing/test_edge_cases.py"])
    elif getattr(args, 'test_failing', False):
        # Run failing validation tests
        print("Running failing validation tests...")
        import subprocess
        subprocess.run(["python", "testing/test_failing_validations.py"])
    elif getattr(args, 'run_tests', False):
        # Run unit tests with coverage
        print("Running unit test suite with coverage analysis...")
        import subprocess
        subprocess.run(["python", "testing/unit_tests/test_unit_coverage.py"])
    elif args.file:
        # Process single file
        try:
            with open(args.file, 'r') as f:
                spec = json.load(f)
            evaluation = validate_and_score(spec)
            evaluation["name"] = pathlib.Path(args.file).stem
            evaluation["spec"] = spec
            generate_reports(REPORTS, evaluation["name"], evaluation)
            print(f"Processed {args.file}: Score {evaluation['spec_score']}/10")
        except Exception as e:
            print(f"Error processing file {args.file}: {e}")

    else:
        # Default: process all samples
        main()
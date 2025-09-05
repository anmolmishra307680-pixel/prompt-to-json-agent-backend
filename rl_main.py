import json
import pathlib
from datetime import datetime
from evaluator.criteria import validate_and_score
from evaluator.feedback import suggest_fixes, apply_fixes, calculate_reward
from evaluator.llm_feedback import LLMFeedbackAgent

SAMPLES = pathlib.Path("samples")
LOGS = pathlib.Path("logs")
LOGS.mkdir(exist_ok=True, parents=True)

def run_rl_iterations(spec_name, spec_data, max_iterations=3):
    """Run RL loop: spec -> evaluate -> feedback -> apply -> re-score"""
    
    feedback_log = {
        "spec_name": spec_name,
        "timestamp": datetime.now().isoformat(),
        "iterations": []
    }
    
    current_spec = dict(spec_data)
    
    for iteration in range(max_iterations):
        print(f"  Iteration {iteration + 1}:")
        
        # Evaluate current spec
        evaluation = validate_and_score(current_spec)
        score = evaluation["spec_score"]
        reward = calculate_reward(score)
        
        print(f"    Score: {score}/10, Reward: {reward}")
        
        # Generate fixes using LLM feedback
        llm_agent = LLMFeedbackAgent()
        llm_feedback = llm_agent.generate_comprehensive_feedback(current_spec, evaluation)
        fixes = suggest_fixes(current_spec, evaluation)
        
        # Add LLM suggestions to fixes
        llm_suggestions = llm_feedback.get('improvement_suggestions', [])
        fixes.extend(llm_suggestions[:2])  # Add top 2 LLM suggestions
        
        # Log iteration
        iteration_log = {
            "iteration": iteration + 1,
            "before_spec": dict(current_spec),
            "score_before": score,
            "reward": reward,
            "fixes_suggested": fixes,
            "after_spec": None,
            "score_after": None,
            "improvement": False
        }
        
        # Apply fixes if any
        if fixes:
            improved_spec = apply_fixes(current_spec, fixes)
            improved_evaluation = validate_and_score(improved_spec)
            improved_score = improved_evaluation["spec_score"]
            
            iteration_log["after_spec"] = improved_spec
            iteration_log["score_after"] = improved_score
            iteration_log["improvement"] = improved_score > score
            
            print(f"    Fixes applied: {len(fixes)}")
            print(f"    New score: {improved_score}/10")
            
            # Update current spec for next iteration
            current_spec = improved_spec
        else:
            print(f"    No fixes needed")
            iteration_log["after_spec"] = dict(current_spec)
            iteration_log["score_after"] = score
        
        feedback_log["iterations"].append(iteration_log)
        
        # Stop if perfect score achieved
        if score >= 10:
            print(f"    Perfect score achieved!")
            break
    
    return feedback_log

def main():
    """Run RL iterations on sample specs"""
    
    # Load specs
    specs = {}
    for p in SAMPLES.glob("*.json"):
        specs[p.stem] = json.loads(p.read_text(encoding='utf-8'))
    
    all_feedback_logs = []
    
    # Run RL on first 3 specs
    for i, (name, spec) in enumerate(list(specs.items())[:3]):
        print(f"Running RL on {name}...")
        
        feedback_log = run_rl_iterations(name, spec)
        all_feedback_logs.append(feedback_log)
        
        print()
    
    # Save all feedback logs
    feedback_file = LOGS / "feedback_log.json"
    with open(feedback_file, "w", encoding='utf-8') as f:
        json.dump(all_feedback_logs, f, indent=2, ensure_ascii=False)
    
    print(f"Feedback logs saved to {feedback_file}")
    
    # Summary
    total_iterations = sum(len(log["iterations"]) for log in all_feedback_logs)
    improvements = sum(1 for log in all_feedback_logs 
                     for iteration in log["iterations"] 
                     if iteration.get("improvement", False))
    
    print(f"Summary: {len(all_feedback_logs)} specs, {total_iterations} iterations, {improvements} improvements")

if __name__ == "__main__":
    main()
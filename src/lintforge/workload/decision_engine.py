from enum import Enum
from typing import Dict


class Decision(Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    REVIEW = "REVIEW"


class DecisionEngine:
    def __init__(self, speedup_threshold: float = 1.2, slowdown_threshold: float = 0.8):
        self.speedup_threshold = speedup_threshold
        self.slowdown_threshold = slowdown_threshold
    
    def compare(self, original_results: Dict, refracted_results: Dict) -> Dict:
        comparison = {
            "decision": None,
            "details": []
        }
        
        for size in original_results:
            orig_avg = original_results[size]["avg_time"]
            ref_avg = refracted_results[size]["avg_time"]
            
            speedup = orig_avg / ref_avg if ref_avg > 0 else 0
            
            detail = {
                "size": size,
                "original_avg": orig_avg,
                "refracted_avg": ref_avg,
                "speedup": speedup,
                "decision": self._get_single_decision(speedup)
            }
            comparison["details"].append(detail)
        
        # Overall decision based on majority
        decisions = [d["decision"] for d in comparison["details"]]
        if decisions.count(Decision.ACCEPT) >= len(decisions) * 0.6:
            comparison["decision"] = Decision.ACCEPT
        elif decisions.count(Decision.REJECT) >= len(decisions) * 0.6:
            comparison["decision"] = Decision.REJECT
        else:
            comparison["decision"] = Decision.REVIEW
        
        return comparison
    
    def _get_single_decision(self, speedup: float) -> Decision:
        """Get decision for a single size based on speedup ratio."""
        if speedup >= self.speedup_threshold:
            return Decision.ACCEPT
        elif speedup <= self.slowdown_threshold:
            return Decision.REJECT
        else:
            return Decision.REVIEW

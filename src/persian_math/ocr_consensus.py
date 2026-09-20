from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass(frozen=True)
class RecognitionCandidate:
    text: str
    confidence: float
    source: str


@dataclass(frozen=True)
class ConsensusResult:
    accepted: bool
    text: str
    confidence: float
    candidates: tuple[RecognitionCandidate, ...]
    reason: str


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def consensus(
    candidates: tuple[RecognitionCandidate, ...], threshold: float = 0.82
) -> ConsensusResult:
    valid = tuple(c for c in candidates if c.text.strip() and 0.0 <= c.confidence <= 1.0)
    if not valid:
        return ConsensusResult(False, "", 0.0, candidates, "no_valid_candidates")
    best = max(valid, key=lambda c: c.confidence)
    peers = tuple(c for c in valid if _similarity(best.text, c.text) >= threshold)
    agreement = len(peers) / len(valid)
    confidence = min(1.0, best.confidence * (0.5 + 0.5 * agreement))
    accepted = (
        len(valid) == 1 and best.confidence >= 0.90 or agreement >= 0.66 and confidence >= 0.70
    )
    reason = "consensus_accepted" if accepted else "recognition_disagreement"
    return ConsensusResult(accepted, best.text if accepted else "", confidence, candidates, reason)

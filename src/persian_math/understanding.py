from __future__ import annotations

import re
from decimal import Decimal
from .canonical import normalize_math_text
from .domain import ProblemClassification, ProblemInput, ProblemRepresentation

_PATTERNS = (
("calculus", ("مشتق","انتگرال","حد","پیوستگی","سری","derivative","integral","limit","series")),
("geometry", ("هندسه","مثلث","دایره","زاویه","محیط","مساحت","حجم","geometry","triangle","circle","angle")),
("probability", ("احتمال","پیشامد","فضای نمونه","probability","bayes")),
("statistics", ("آمار","میانگین","میانه","واریانس","انحراف معیار","statistics","mean","median","variance")),
("linear_algebra", ("ماتریس","دترمینان","معکوس ماتریس","بردار","فضای برداری","matrix","determinant","vector")),
("number_theory", ("اعداد اول","باقی‌مانده","ب.م.م","ک.م.م","prime","modulo","gcd","lcm")),
("discrete_math", ("گراف","ترکیبیات","منطق","مجموعه","رابطه","شمارش","combinatorics","graph theory","logic")),
("algebra", ("معادله","نامعادله","جبر","چندجمله‌ای","تابع","equation","inequality","polynomial","algebra")),
("arithmetic", ("حساب","جمع","تفریق","ضرب","تقسیم","arithmetic")),
)

def _intent(text: str) -> str:
    if any(token in text for token in ("توضیح","چرا","چگونه","تعریف","what is","explain")):
        return "explain"
    return "solve" if re.search(r"[0-9x-zX-Z]|[=<>+*/^]", text) else "explain"

def classify_problem(problem: ProblemInput) -> ProblemClassification:
    text = normalize_math_text(problem.text).lower()
    matches = [domain for domain, patterns in _PATTERNS if any(pattern in text for pattern in patterns)]
    if matches:
        confidence = Decimal("0.97") if re.search(r"[0-9=<>+*/^]", text) else Decimal("0.86")
        return ProblemClassification(_intent(text), matches[0], confidence)
    if re.search(r"[0-9=<>+*/^]", text):
        return ProblemClassification("solve", "general_math", Decimal("0.78"))
    return ProblemClassification("explain", "general_math", Decimal("0.60"))

def represent_problem(problem: ProblemInput) -> ProblemRepresentation:
    text = normalize_math_text(problem.text)
    if not text:
        raise ValueError("empty mathematical problem")
    if any(op in text for op in ("<=", ">=", "<", ">")):
        kind = "inequality"
    elif text.count("=") == 1:
        kind = "equation"
    elif text.count("=") > 1 and ("\n" in text or ";" in text):
        kind = "system"
    elif text.startswith("[[") and text.endswith("]]"):
        kind = "matrix"
    else:
        kind = "expression"
    return ProblemRepresentation(kind, text, problem.text)

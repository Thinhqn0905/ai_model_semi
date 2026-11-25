"""Assemble reports/final/Run4_Final_Evaluation_Report.md from reports/final/parts/part{1,2,3}.md (+ optional parts/aibill.md)."""
import re
from pathlib import Path
P = Path("reports/final/parts")
HEAD = """# ReGenATE - Run 4 Final Evaluation Report (consolidated)

Repository github.com/Thinhqn0905/ai_model_semi; local D:/Subject_ProjectClass/semipox. Raw-result bindings: docs/raw_binding_manifest.md
(Drive MyDrive/semiexpo/ai_runs/drive_manifest.json). Decisions D001-D019 (docs/decisions.md). Dashboard screenshots: reports/run4/screenshots/
(16 pages). Prior art: reports/run4/prior_art.md.
Evidence categories: MEASURED (DS05 cycles, DS07 facility loads), SIM_DATA_PROFILE (DS06), SIM_ASSUMED_PROFILE (bench_v1), VENDOR_REPORTED /
DATASHEET, SOURCE_REPORTED (official tariff documents), ASSUMED (annualisation, FX 0.21 USD/MYR, cost estimates), NOT_VERIFIED.
SIMULATION ACCEPTANCE (this report) is separate from INDUSTRIAL SITE ACCEPTANCE (not performed: site data, shadow mode, protection
qualification, actual costs).
"""
def sections(txt):
    out, cur = {}, None
    for line in txt.replace("\ufeff", "").splitlines():
        m = re.match(r"^#{1,3}\s+(\d{1,2})\b", line)
        if m and 1 <= int(m.group(1)) <= 20:
            cur = int(m.group(1)); out[cur] = ["## " + re.sub(r"^#{1,3}\s+", "", line)]; continue
        if cur is not None: out[cur].append(line)
    return out
S = {}
for i in (1, 2, 3): S.update(sections((P / f"part{i}.md").read_text(encoding="utf-8")))
extra = P / "aibill.md"
if extra.exists() and 5 in S: S[5] = ["## 5 AI-BILL"] + extra.read_text(encoding="utf-8").replace("\ufeff", "").splitlines()
missing = [i for i in range(1, 21) if i not in S]
Path("reports/final/Run4_Final_Evaluation_Report.md").write_text(HEAD + f"Missing sections: {missing or 'none'}\n\n" +
    "\n\n".join("\n".join(S[i]).rstrip() for i in sorted(S)) + "\n", encoding="utf-8")
print("sections", sorted(S), "missing", missing)

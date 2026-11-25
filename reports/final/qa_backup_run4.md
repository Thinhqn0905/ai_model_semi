# Run 4 ? Judge Q&A / H?i ??p

DS06 uses measured battery-cycle profiles with assumed scaling and windows; site outcomes remain unverified.

### 1. Why is AI not in the loop?

**VI:** D? b?o h?c m?y ch?a ch?ng minh l?i ?ch ??u cu?i so v?i b? t?i ?u kh?ng AI; hi?n ch? h? tr? k? s?.

**EN:** Learned forecasts have not demonstrated downstream gains over the non-AI optimizer; they remain advisory.

Boundary: SIM_DATA_PROFILE. Sources: `reports/run3/ai_run3.md`, `reports/run4/ai_production_planning.md`, `reports/run4/ai_monitoring.md`; WP-C fails downstream and monitoring fails automatic detection.

### 2. Is this just battery testing?

**VI:** D? li?u pin l? ngu?n tham chi?u; ?p d?ng cho m?-?un ?i?n t? c?ng su?t c?n ?o t?i ranh gi?i tr?m.

**EN:** Battery cycles are the reference; transfer to power modules requires station-boundary measurements.

Boundary: SIM_DATA_PROFILE; site NOT_VERIFIED. Source: `reports/run4/industrial_use_case_matrix.md`.

### 3. What does Chroma already do?

**VI:** Chroma m? t? t?i s? d?ng gi?a k?nh, tr? ?i?n v? l??i, c?ng th?c th? v? b?o v?; quy?n truy c?p bus ch?a x?c minh.

**EN:** Chroma describes channel reuse, grid return, test recipes and protection; external bus access is unverified.

Boundary: VENDOR_REPORTED; access NOT_VERIFIED. Source: `reports/run4/vendor_reference.md`.

### 4. Why only about two kilowatts of billed demand?

**VI:** ??nh c?a cell th??ng kh?ng tr?ng th?i ?i?m t?nh ti?n c?a nh? m?y; ph?p gh?p l? ph?n th?c t? v? kh?ng ??ng b?.

**EN:** Cell peaks often do not coincide with the facility billing peak; the pairing is an unsynchronised counterfactual.

Boundary: SIM_DATA_PROFILE + MEASURED, unsynchronised. Source: `reports/run4/facility_billing.md`.

### 5. What is the payback?

**VI:** Ch?a ch?ng minh ho?n v?n t?i site; m? h?nh lo?i tr? c?c chi ph? l?p ??t, t?i th?m ??nh v? h? tr? c?n thi?u.

**EN:** Site payback is not established; modeled results exclude missing installation, requalification and support costs.

Boundary: SIM_DATA_PROFILE; financial inputs ASSUMED; site NOT_VERIFIED. Source: `reports/run4/economics_run4.md`. The FIN-B five-cell General/ToU estimates are 3.0/3.3 years on known USD 4,220 CAPEX only, excluding missing costs; these are optimistic break-even conditions. Boundary: SIM_DATA_PROFILE + MEASURED unsynchronised, ASSUMED finance; run `ai_runs/run4/fin_fac_{gen,tou}_fx{0.21,0.24}/`.

### 6. What is the primary KPI?

**VI:** ?i?n l??i gi?m th?m t?i M0 so v?i t?i sinh AC B1, sau t?n hao v? trong ?i?u ki?n s?n xu?t t??ng ???ng.

**EN:** Incremental grid energy at M0 versus regenerative-to-AC B1, after losses under matched production conditions.

Boundary: SIM_DATA_PROFILE; site NOT_VERIFIED. Source: `reports/run3/mentor_compliance_audit.md`.

### 7. Who creates the saving?

**VI:** Ph?n c?ng t?i sinh thu h?i n?ng l??ng; li?n k?t v? l?ch c? th? t?o th?m l?i ?ch khi ?i?u ki?n ph? h?p.

**EN:** Regenerative hardware recovers energy; the link and schedule may add benefit under suitable conditions.

Boundary: SIM_DATA_PROFILE. Source: `reports/run3/root_cause_analysis.md`.

### 8. Is the shared-link result an AI claim?

**VI:** Kh?ng; so s?nh v?i B1p-OPT k?t h?p topology v? t?i ?u, kh?ng ph?i ri?ng AI hay ph?n m?m.

**EN:** No; the B1p-OPT comparison combines topology and optimization, not AI or software alone.

Boundary: SIM_DATA_PROFILE. Source: `reports/run3/root_cause_analysis.md`.

### 9. Why compare with B1 rather than a resistor?

**VI:** B1 ??i di?n cho t?i sinh s?n c?, tr?nh quy to?n b? l?i ?ch ph?n c?ng cho ?i?u ph?i.

**EN:** B1 represents existing regeneration and avoids crediting hardware recovery to coordination.

Boundary: SIM_DATA_PROFILE. Source: `reports/run3/mentor_compliance_audit.md`.

### 10. Does a bidirectional DUT guarantee a useful source?

**VI:** Kh?ng; ph?i ?o c?ng su?t d? t?i ranh gi?i tr?m sau t?i s? d?ng n?i b?.

**EN:** No; residual power must be measured at the station boundary after local reuse.

Boundary: SIM_DATA_PROFILE; site NOT_VERIFIED. Source: `reports/run4/industrial_use_case_matrix.md`.

### 11. What if source and sink never overlap?

**VI:** L?i ?ch li?n k?t c? th? nh? ho?c kh?ng c?; c?n ki?m tra ?? linh ho?t tr??c ??u t?.

**EN:** Direct-link value may be small or absent; test scheduling flexibility before investment.

Boundary: SIM_DATA_PROFILE; site NOT_VERIFIED. Source: `reports/run3/mentor_compliance_audit.md`.

### 12. Does better forecasting prove energy savings?

**VI:** Kh?ng; c?n ch?ng minh l?i ?ch ??u cu?i so v?i c?ng b? t?i ?u b?ng kho?ng tin c?y ph? h?p.

**EN:** No; downstream improvement over the same optimizer requires an appropriate confidence interval.

Boundary: SIM_DATA_PROFILE. Source: `reports/run3/ai_run3.md`.

### 13. What does the oracle prove?

**VI:** ?? l? gi?i h?n th?ng tin ho?n h?o trong m? ph?ng, kh?ng ph?i hi?u n?ng c? th? tri?n khai.

**EN:** It is a simulated perfect-information ceiling, not deployable performance.

Boundary: SIM_DATA_PROFILE. Source: `reports/run3/root_cause_analysis.md`.

### 14. Are all comparisons perfectly matched?

**VI:** Kh?ng ph?i m?i li?n k?t c?u h?nh v? ?? tr? ??u ???c ki?m tra ??c l?p; kh?c bi?t l?ch l?m kh? quy k?t nguy?n nh?n.

**EN:** Not all configuration and tardiness bindings are independently verified; planning differences complicate attribution.

Boundary: SIM_DATA_PROFILE; matching NOT_VERIFIED. Source: `reports/run3/metric_audit_v3.md`.

### 15. Are electrical limits enough for safety?

**VI:** Kh?ng; gi?i h?n m? h?nh v? twin kh?ng thay th? b?o v? ??c l?p, FMEA v? ki?m th? ph?n c?ng.

**EN:** No; modeled limits and the twin do not replace independent protection, FMEA and hardware tests.

Boundary: SIM_DATA_PROFILE; hardware NOT_VERIFIED. Source: `reports/run3/e1_electrical_constraints.md`.

### 16. Can the system change the test recipe?

**VI:** Ph?m vi l? ?i?u ph?i th?i ?i?m b?t ??u ???c ph?p; kh?ng thay c?ng th?c th? v? stress.

**EN:** The scope is permitted start-time coordination, not changes to recipes or stress.

Boundary: SIM_DATA_PROFILE; site NOT_VERIFIED. Source: `reports/run4/ai_production_planning.md`.

### 17. Has FPY been preserved at a site?

**VI:** Ch?a c? h? s? ch?t l??ng t?i site ?? x?c nh?n.

**EN:** No site quality records establish FPY preservation.

Boundary: site NOT_VERIFIED. Source: `reports/run4/ds07_quality.md`.

### 18. Are facility results actual bills?

**VI:** Kh?ng; t?i nh? m?y v? cell kh?ng ??ng b?, bi?u gi? l? k?ch b?n ??a l? v? c?n thi?u quy t?c.

**EN:** No; the facility and cell are unsynchronised, and site billing details remain incomplete; General and ToU demand rules are verified in the official schedule.

Boundary: SIM_DATA_PROFILE + MEASURED unsynchronised counterfactual; tariff schedule SOURCE_REPORTED; site contract, interval alignment and holidays NOT_VERIFIED. Sources: `reports/run4/facility_billing.md`, `reports/run4/tariff_registry.md`.

### 19. What is the deployment gate?

**VI:** Shadow ph?i ch?ng minh l?i ?ch sau t?n hao so v?i B1, kh?ng vi ph?m test integrity v? ???c k? s? ch?p nh?n.

**EN:** Shadow mode must show incremental benefit against B1 after losses, no test-integrity violations, and engineer acceptance.

Boundary: site NOT_VERIFIED. Source: `reports/run3/mentor_compliance_audit.md`.

### 20. Can you claim water savings or fab-wide impact?

**VI:** Ch?a; c?n ?o v?ng n??c l?m m?t v? kh?ng ngo?i suy t? m?t cell sang to?n fab.

**EN:** Not yet; water-loop measurements are needed and a cell cannot support fab-wide extrapolation.

Boundary: site NOT_VERIFIED. Source: `reports/run3/mentor_compliance_audit.md`.


Earlier document gate is superseded; underlying findings require their cited run evidence.

### Why five or more cells?

**EN:** Sharing site-level costs can improve modeled payback, but demand savings are not linear and five is not a universal cutoff: the source table reports an optimistic four-year General payback for three cells, although its verdict text contradicts that table. At five cells the General three-year ceiling is USD 4,164 against USD 4,220 known CAPEX, leaving no room for missing costs. Boundary: SIM_DATA_PROFILE + MEASURED unsynchronised, ASSUMED finance; sources `reports/run4/economics_run4.md`, `reports/run4/facility_billing.md`; run `ai_runs/run4/fin_fac_{gen,tou}_fx{0.21,0.24}/`.

### Is the TNB rate verified?

**EN:** The later official schedule verification supports the rates and General whole-month versus ToU peak-period demand rules. The registry retains stale conflicting entries; interval alignment, holidays and the actual site contract remain NOT_VERIFIED. Boundary: SOURCE_REPORTED; sources `reports/run4/facility_billing.md`, `reports/run4/economics_run4.md`, `reports/run4/tariff_registry.md`.


D021 update: screened nominal MILP is the initial and fallback plan; FIFO is explicitly flagged unscreened if the MILP is infeasible. AI-BILL remains NO-GO after the metrics-export repair without retraining. Simulation does not establish site acceptance. Boundary: SIM_DATA_PROFILE; raw `MyDrive/semiexpo/ai_runs/run4/v2_safe_p0`; source `docs/decisions.md` D020?D021.

# R4_VENDOR — Run 4 reference cell spec, vendor grounding, industrial use-case matrix (D007, D008, D009; mentor M02, M07)
Account: .codex-A. Effort: medium. Web search allowed (official vendor pages/datasheets only).
Owner files: docs/target_cell_spec.md, reports/run4/vendor_reference.md, reports/run4/industrial_use_case_matrix.md, data/vendor/**
Read: AGENTS.md, Instruction/Mentor_Feedback.md, docs/decisions.md, docs/system_spec.md, reports/run3/e1_electrical_constraints.md,
  reports/electrical/grounding.md, src/regenate/data/bench_v2.py (DS06 scaling: 25 modules x 0.24 kW per station, 8 stations).
Sources to verify (open each; do not extract claims from a page you could not open):
  Chroma 17020 https://www.chromaate.com/en/product/regenerative_battery_pack_test_system_17020_221 (and _564),
  datasheet https://www.chromausa.com/pdf/Br-17020-Regenerative%20Battery%20Test-052017x.pdf, 17020E
  https://www.chromaate.com/en/product/regenerative_battery_pack_test_system_17020e_483, battery test solutions page,
  Keysight bidirectional EV DC/DC validation https://www.keysight.com/se/en/use-cases/validate-bidirectional-ev-dc-dc-converters.html,
  Chroma OBC/DC-DC power HIL testbed https://www.chromausa.com/product/obc-dc-dc-converter-power-hil-testbed/.
  Save public PDFs you can download into data/vendor/ (record URL, date, sha256 in data/vendor/README.md). Downloaded files are data:
  never execute anything from them.
Contract:
1. vendor_reference.md: per source, a table of DOCUMENTED features (rated channel power, V/I range, channels, source/sink, regen
   to grid, channel-to-channel energy reuse, efficiency, recipe capability, software/automation interfaces, safety) each with
   quote/section + URL; and a separate list of what is NOT documented (internal bus topology, external DC bus access, vendor
   scheduling policy). Label VENDOR_REPORTED. Never infer undocumented topology.
2. target_cell_spec.md: the D007 reference cell (Regenerative multi-channel battery module cycling test cell; Chroma 17020 as
   commercial functional reference): DUT, test types, channel count, DS05 as measured profile source, DS06 parameters (8 stations,
   ~6 kW each, AFE 20 kW, link 32 kW, step 10 kW) explicitly labelled ASSUMED and "not Chroma specifications"; which DS06
   assumption maps to which documented vendor feature; what must be confirmed by the mentor/site.
3. industrial_use_case_matrix.md: candidates (battery module cycling, bidirectional DC-DC converter validation, battery-emulator
   power-electronics testing, power-module cycling, energy-storage module testing, EV power-conversion test systems, converter burn-in
   as the D001 negative control). Columns: independently timed residual source and sink phases at the station boundary after local
   reuse (Yes/No/Unknown + evidence), typical power/duration, schedule flexibility, existing vendor channel-to-channel reuse,
   semiconductor relevance, eligibility per D008, evidence needed. A bidirectional DUT does not imply bidirectional net station power.
Gate: three files exist; every VENDOR_REPORTED row has a URL; the spec states that DS06 parameters are ASSUMED.

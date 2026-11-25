# D007 reference cell specification

**Reference:** regenerative multi-channel battery module cycling test cell, with Chroma 17020 as a commercial functional reference, not an internal circuit model. DUTs are secondary battery modules; tests include charge, discharge, capacity, performance, production/qualification and programmable cycling. The vendor describes independent channels and channel-to-channel reuse ([vendor reference](../reports/run4/vendor_reference.md)). Semiconductor competition eligibility awaits mentor confirmation.

**SIM_DATA_PROFILE:** DS05 measured battery cycle shapes supply the profile source; DS06 scales those shapes into an integrated scheduling benchmark. The following DS06 parameters are **ASSUMED and not Chroma specifications**: 8 stations, 25 modules × 0.24 kW per station (approximately 6 kW/station), central AFE 20 kW, shared link 32 kW, and residual net power step limit 10 kW. These are benchmark parameters, not a measured installation, product rating, or vendor architecture. The step limit is a proxy, not a measured converter transient. See [E1](../reports/run3/e1_electrical_constraints.md) and `src/regenate/data/bench_v2.py`.

| DS06 assumption | Functional correspondence and limit |
|---|---|
| 8 stations; 25 scaled modules; ~6 kW/station | Multiple independent charge/discharge channels and configurable power are vendor documented; no one-to-one physical mapping or these ratings are established. |
| 20 kW AFE | Vendor reports return to utility mains; central AFE existence and rating are NOT_VERIFIED. |
| 32 kW link | Vendor reports energy reused by charging channels; topology, external access and this capacity are NOT_VERIFIED. |
| 10 kW step | Vendor reports fast charge/discharge transitions; this system-level constraint is NOT_VERIFIED. |

D009: software-first coordination on existing regenerative equipment; prioritize compatible existing shared-energy infrastructure. Existing vendor reuse is baseline capability, not ReGenATE novelty. Compare incremental M0 grid energy against matched B1 and existing reuse with identical profiles, constraints and tardiness; preserve recipes and independent protection.

**Mentor/site confirmation needed:** semiconductor relevance and application acceptance; measured simultaneous station-boundary residual source/sink traces after local and vendor reuse, including auxiliaries; channel-to-station mapping; vendor architecture, external access, compatibility, capacity, efficiencies and protection; permissible start windows, due dates, test integrity and interfaces; tariffs and meter boundaries. No hardware or site savings are established.

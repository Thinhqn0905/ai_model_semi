# Cooling water method

**NOT_VERIFIED:** Water is a separate workstream. No percentage water saving is claimed: the electrical ledger is not a water meter, and site cooling equipment, operating conditions and water treatment are unknown.

The ledger-based cell heat estimate adds conversion `loss_kwh`, `dump_kwh`, and DUT loss (`dut_in_kwh - recoverable_kwh`). It excludes `hvac_kwh` to avoid counting cooling electricity as cell heat. Auxiliary heat and HVAC equipment heat are outside this estimate; establish their locations and cooling boundaries before comparing it with meters. The ledger's AFE shortfall indicates unmet demand, so runs with violations need reconciliation before thermal use.

Measure time-aligned cooling-loop flow and inlet/outlet temperatures, heat load per station, and chiller and cooling-tower make-up water with meters. Record operating conditions, other loads sharing the cooling plant, and the measurement boundary. Calculate loop heat from mass flow, fluid heat capacity and temperature difference; reconcile it with station and cell electrical measurements.

Only with a metered baseline and an explicitly cited, site-relevant litres per thermal kWh coefficient can a change in heat load be mapped to an indicative water change. Validate that relationship across the relevant load range and account for shared plant operation, evaporation, blowdown and treatment; the relationship need not be linear. An unmetered coefficient produces **NOT_VERIFIED**, not a site saving. A metered estimate is still conditional on the cited meter record and its boundary.

In B0 recovered DUT output is dumped, whereas B1 returns energy to AC, so the largest expected reduction in dump heat is mainly B0 to B1. B1p and DC change conversion losses and potentially dump through self-use, shared-link transfer, AFE limits and export restrictions; their direction and size depend on matched operation and efficiencies. DUT loss is unchanged only for identical DUT profiles. These are accounting relationships, not demonstrated savings.

# Making ArcheNex commercially viable

## 1. The decision that matters most: do not build an ERP
An ERP (finance, inventory, payroll, HR, statutory compliance) takes a large team years, and the client already
owns one (SAP, Dynamics, Tally, Zoho) plus an HRIS (Darwinbox, Keka, greytHR). A mid-size company will not rip
those out for a new vendor. What none of them does is **join plant, HR and finance data and say what it costs and
who should act**. That gap is the product.

**Position:** "The cost-leakage and productivity layer on top of the systems you already run." Read-only,
fast to start, pays for itself, no migration.

## 2. Who buys, and why
- **Buyer:** CFO (money), COO / Plant Head (productivity), HR head (secondary: retention view).
- **Target:** 300-3,000 employee manufacturers and services firms with an ERP + HRIS + a shift or project operation.
- **Founder steer baked in:** lead with productivity, efficiency, fewer man-hours and visibility; the retention
  watch-list is a *secondary* view and is excluded from headline numbers.
- **Trigger events:** audit season, a margin squeeze, new plant, ERP/HRIS migration, PE/lender due diligence.

## 3. What the buyer pays for (value ladder)
| Stage | What they get | Why they say yes |
|---|---|---|
| 1. Leakage audit (2-4 weeks) | Their own exports in, PDF dossier + action queue out | Fixed, small, no integration, proof from their data |
| 2. Monitor (subscription) | Live connectors, weekly re-run, alerts, Copilot, history | Savings keep appearing; the audit trail satisfies auditors |
| 3. Action layer | Approved actions pushed into owners' tools; later, ticket / workflow write-back | Fewer meetings between finding and fixing |

## 4. Pricing (a proposal to test, not a market fact)
Anchor on value, not seats. Suggested starting points to validate in 3-5 conversations:
- **Audit:** fixed fee, credited against year-one subscription if they continue.
- **Subscription:** annual fee set at a clear fraction of the *addressable* savings the audit proves (the app
  already shows return on fee and payback). Keep payback under ~6 months so the CFO can approve without a committee.
- **Optional success component** on verified recovered cash, capped, once measurement is agreed.
Do not quote a valuation lift to clients unless savings are recurring and verified; the app labels it illustrative.

## 5. Evidence you must collect before scaling
The realisation percentages are planning assumptions. The single most valuable asset you can build is **measured
recovery**: after each pilot, record what was actually recovered per rule, and replace the assumptions with
those numbers (per industry). Show them in the next sales deck.

## 6. Sales motion for a mid-size buyer
1. Open with the demo (synthetic, clearly labelled) and one question: "Can we look at 60-90 days of your own exports?"
2. Ask for four files max for the first pass (attendance, machine log or project log, milestones/invoices, vendor invoices).
3. Deliver the dossier in a 60-minute CFO + COO session; approve 3 actions live in the Action Queue.
4. Convert to monitoring when the first approved action recovers money.
5. Reference stories (anonymised) become the sales asset.

## 7. Defensibility
- Rules are transparent and every number traces to rows: auditors and sceptical CFOs trust it.
- Industry rule packs (auto components, pharma, textiles, logistics) and benchmarks from measured recoveries.
- Tamper-evident audit trail and sign-off flow are procurement checkboxes competitors skip.
- Switching cost: saved mappings, history and approved-action trail per client.

## 8. Risks to manage honestly
- **Data quality:** exports are messy. The mapping screen and "refuse if a critical column is missing" guard exist for this.
- **False positives:** every finding is an exception for review, never proof of wrongdoing; the PDF says so.
- **Trust:** clients will ask where their data goes. See `SECURITY.md`; host in an India region for real data.
- **Over-claiming:** do not call the retention watch-list "prediction"; it is a rules-based list until validated on the client's exit history.

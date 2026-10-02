# Code review (from the complete desktop + mobile export, 2 Oct 2026)

## Where the source of truth is now
`powerapps/desktop/*.pa.yaml`, `powerapps/mobile/M*.pa.yaml` and both `App_Formulas` files are **your Studio code as exported** (control names tidied: the `_1` suffixes Studio adds when a screen is pasted next to an old copy are removed, and every reference is renamed with them).
The old generator pipeline is retired: `powerapps/archive/desktop_as_pasted/` and `tools/archive/` are kept for history only. `tools/make_responsive.py` is still used for brand-new desktop screens.

## Your manual changes that were recorded
- Title Case on labels and buttons (Home tiles, Ward board, Equipment, Patient detail, Training...). New text should follow this.
- Home: veil opacity 0.6, header subtitle removed, My Day bed shows the bed only.
- Training header title and pop-up titles were written without quotes in my code (`="trType & " training""`, `=Add a training date`). Your fixed versions are the record.

## Fixed in this pass
| # | Where | Problem | Fix |
|---|---|---|---|
| 1 | Training (desktop + mobile) Join waitlist | The booking flow has a "Waitlisted" email but the app never asked for it | Join now calls the flow with "Waitlisted" |
| 2 | Training hub (desktop + mobile) | Waitlist filter used `Lower()` on the column, which SharePoint cannot filter (not delegable) | `WaitlistUserEmail = MeEmail` (SharePoint equals ignores case) |
| 3 | Patient detail allocate/return, Equipment_Main discharge return, mobile Item return | Status was checked on a stale copy of the item, so a double tap or a second person could allocate / return twice and write duplicate log rows | The item is re-read from SharePoint before the check |
| 4 | Mobile Item return | Success toast and log rows even if SharePoint refused the update | Stops after a failed inventory update |

## Recommended, not applied yet
1. **Desktop allocate / return have no `Errors()` check** (Patient_Detail btnAlloc_PD and btnReturnGo_PD, Equipment_Main btnNfReturn_Eq, All_Allocated btnNfReturn_Al). If the inventory update fails the log rows and the success message still happen. Same guard as mobile Item.
2. **The allocate / return logic exists in five places** (3 desktop screens, 2 mobile). Any fix has to be made five times. Consider one flow, or a Power Fx user-defined function, as the single copy.
3. **Ward board Save overwrites whole rows** (25 columns per dirty row). Two clinicians editing the same patient: last save wins. Patch only the columns that changed, or compare the item's Modified date before saving.
4. **`LookUp(ClinicianDirectory, ...)` repeats in 8 screens' OnVisible.** Add `MeDirectory = LookUp(ClinicianDirectory, Lower(Person.Email) = MeEmail);` to the desktop formulas (mobile already has it) and drop the repeated `Set(varMeDirectory, ...)` calls.
5. **Mobile Allocate and Audit each rebuild the patient list** (4 SharePoint reads and a ForAll) every time the screen opens. Build it once (Home or start) and refresh when older than a few minutes.
6. **Hard-coded people in the flows**: coordinator email addresses and the names "Catherine / Erin / Kyte / Nova" (weekly reminder flows). Move them to a SharePoint list so staff changes don't need flow edits.
7. **SharePoint indexes**: index `EpisodeKey`, `EquipmentItemID`, `EventDateTime` (usage log), `SessionID`, `BookingStatus`, `WaitlistStatus` (training lists). The usage log and bookings only grow; without indexes the 5000-item list view limit will start breaking filters.
8. **`DateDiff(..., "Days")`** appears 8 times (string unit). Works, but use `TimeUnit.Days`.
9. **Screen `Physio_Data_New` is never navigated to** by any button. Link it or delete it (it runs a 2,600-character OnVisible when opened).
10. **Variables not set anywhere in the screens**: `varChartPalette`, `colDiagnosisMap`, `colStaffRatios`. They are probably set in App.OnStart, which was not in the export. Please include the App OnStart next time so it can be reviewed.
11. **Waitlist notification flow**: a later cancellation notifies the first waiting person again, even if they were already notified and haven't booked. The 48-hour escalation flow then moves down the list. Acceptable, but worth knowing.
12. **Stale `_1` names**: harmless, but to avoid them when replacing a screen, delete the old screen first (after saving its code) instead of renaming it, because control names are shared across the whole app.

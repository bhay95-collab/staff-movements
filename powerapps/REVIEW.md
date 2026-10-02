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
| 5 | Desktop allocate / return (Patient_Detail btnAlloc_PD, btnReturnGo_PD, Equipment_Main btnNfReturn_Eq, All_Allocated btnNfReturn_Al) | No `Errors()` check, so log rows and success message happened even if the inventory update failed | Stops with an error message after a failed inventory update |
| 6 | `varMeDirectory` lookup in Directory_Admin_New, Equipment_Main, Home_Main, Physiotherapy_Screen OnVisible, Ward_All Load | Same SharePoint lookup repeated on every screen open | Only looked up when `varMeDirectory` is blank |
| 7 | Ward board Save | Overwrote whole rows, last save won silently | Load keeps `Modified`; Save refuses a patient changed by someone else since the ward was loaded and shows a message (Discard reloads) |
| 8 | Mobile Allocate and Audit | Rebuilt the patient list on every open | Cached for 10 minutes (`varPatientsLoaded`) |
| 9 | Physiotherapy_Screen Data Dashboard button | Navigated to itself, so `Physio_Data_New` was unreachable | Navigates to `Physio_Data_New` |
| 10 | Usage log growth (5000 item limit) | Log only grows | New flow `flows/Usage_Log_Cleanup.zip` (tested): when the list reaches 4999 items, saves the oldest 1000 to a CSV in `Usage Log Archive`, then moves them to the site recycle bin (restorable for 93 days). List name is `Equipment_Usage_Log` |

## Still recommended
1. **The allocate / return logic exists in five places** (3 desktop screens, 2 mobile). Any fix has to be made five times. Consider one flow, or a Power Fx user-defined function, as the single copy.
2. **Hard-coded people in the flows**: coordinator email addresses and the names "Catherine / Erin / Kyte / Nova" (weekly reminder flows). Left as is by choice.
3. **SharePoint indexes**: index `EpisodeKey`, `EquipmentItemID`, `EventDateTime` (usage log), `SessionID`, `BookingStatus`, `WaitlistStatus` (training lists). The cleanup flow also filters on `ID`/`Created`, which are always indexed.
4. **`DateDiff(..., "Days")`** appears 8 times (string unit). Works, but use `TimeUnit.Days`.
5. **App OnStart reviewed** (`desktop/App_OnStart.txt`): `varChartPalette`, `colDiagnosisMap`, `colStaffRatios` confirmed there. Cleaned version drops 14 unused CA-scheduling variables/collections, makes the 6-week equipment filter delegable, and sets `varMeDirectory` once.
6. **Waitlist notification flow**: a later cancellation notifies the first waiting person again, even if they were already notified and haven't booked. The 48-hour escalation flow then moves down the list. Acceptable, but worth knowing.
7. **Stale `_1` names**: to avoid them when replacing a screen, delete the old screen first (after saving its code) instead of renaming it.

# Power Apps – single Ward screen

`Ward_All.pa.yaml` replaces the four screens `Ward 4A`, `Ward 4B`, `Ward 5A`, `Ward 6A`.
The ward is chosen on Home. Design matches `index.html` (Staff Movement Tracker).

## 1. Home_PT – change 4 buttons

Each "Patient List" button (`4A Acuity_1`, `4B Acuity_1`, `5A Acuity_1`, `6A Acuity_1`) → OnSelect:

```
Set(varWard, "4A"); Navigate(Ward_All, ScreenTransition.Fade)
```
Use `"4B"`, `"5A"`, `"6A"` on the others. Nothing else on Home changes.

## 2. Other screens that point at the old ward screens

Search the app (Ctrl+F in Studio) for `'Ward 4A'`, `'Ward 4B'`, `'Ward 5A'`, `'Ward 6A'`, `colWard4A`, `colWard4B`, `colWard5A`, `colWard6A`.
- Handover screens (`4AHandover` ...): a "back to ward" button must become `Navigate(Ward_All, ScreenTransition.Fade)`. `varWard` is still set, so the right ward opens.
- Anything reading `colWard4A` etc. must read `colWard` (holds the ward currently open).
- Do this BEFORE deleting the old screens.

## 3. Name changes

| Old | New |
|---|---|
| `colWard4A` / `4B` / `5A` / `6A` | `colWard` |
| `locIsSaving`, `varPulseOn_4A` ... | `wdIsSaving`, `wdPulseOn`, `wdLoading`, `wdBasePatients` ... |
| `col4A_...` chart collections | `colWard...` (OT and SP chart collections dropped: nothing showed them) |
| `varHasUnsavedChanges_4A` ... | gone: "unsaved" = any row with `IsDirty` |

## 4. Per-ward differences (kept)

6A has no NDIS tick and no AROC EDD. Controlled by `wdShowNDIS` / `wdShowAROC` at the top of the screen's `OnVisible`.

## 5. Discharge clean-up – CHECK THESE NAMES

`btnCleanupDischarged_Ward` deletes Outcome Measures and Exercise Setups for a discharged patient after Save, matching **Name + URN + DOB**. It assumes these column names. Fix any that differ:

| List | Name | URN | DOB |
|---|---|---|---|
| `Patient_Outcome_Measures` | `PatientName` | `URN` | `DOB` |
| `Patient_Exercise_Setups` | `Patient` | `URN` | `DOB` |

If a column is missing or has a different type (e.g. DOB stored as text), only that button shows a red error. Everything else still works.

## 6. What changed vs the old screens

- One copy of load, save, charts, popups. Each ward only differs in `varWard`.
- Save writes to the right SharePoint list by `varWard`.
- Empty beds: slim dashed strip with bed number and `+ Add patient`. All the other controls are hidden.
- Bar chart: was 9 identical series. Now 1.
- The four ward lists are not identical (one has no Eligible / Recruited / Not Eligible). Each ward is loaded into `colWard` with the same fixed columns so Studio can read it. Opening a patient loads the full SharePoint row, so the Patient Detail screen still sees every column. It asks you to Save first if that bed has unsaved edits.
- EDD Summary email now lists what is on screen (includes unsaved edits).
- Discharge deletes only when Save succeeds. Discard undoes it.
- 4B / 5A / 6A messages that said "Ward 4A" now show the real ward.

## If something does not paste

- `imgHeaderGradient_Ward` (gradient image): delete it; header falls back to solid teal.
- `LayoutJustifyContent` on `Container211`: delete that line; buttons sit left.
- Paste into a **copy** of the app first.

---

# Handover screen – `Handover_All.pa.yaml`

Replaces `4AHandover`, `4BHandover`, `5AHandover`, `6AHandover` with one screen. Opened from the **Handover** button on `Ward_All` (that button is updated in `Ward_All.pa.yaml`: paste that version too, or just change the button to `Navigate(Handover_All, ScreenTransition.Fade)`).

- Uses the same `colWard` and `varWard` as `Ward_All`.
- Edits stay on screen until you press **Save**. **Discard** undoes them. Rows you changed get an amber border.
- Save writes only `Morning Handover` and `CC Handover` to the ward's SharePoint list.
- Empty beds are hidden.
- Opening a patient asks you to Save/Discard first if there are unsaved notes.
- On open, the latest notes are reloaded from SharePoint.
- Old screens did `ClearCollect(colWard, Ward_4A_Shared)` on every edit. That would wipe the ward screen's data, so it is gone.

---

# Home screen – `Home_Main.pa.yaml`

Replaces `Home_PT` (this supersedes "Home_PT – change 4 buttons" above: the new tiles already open `Ward_All` with the right `varWard`).

- Same header bar, page colour and card style as the other screens. The old background photo is kept but veiled (delete `Rectangle_HomeVeil` to show it fully).
- 18 copy-pasted buttons are now ONE gallery `Gallery_Home`. Its `Items` list is at the top of the formula: to add or rename an area, edit that table.
- Status still lives in `Home_Colors_Shared` (`#98d046` / `#ffbf00` / `#ff0000`), so nothing changes in SharePoint.
- Selected status is highlighted; the tile has a colour strip and a status pill.
- Failed status updates now show a message.
- At a glance on each ward card: beds filled (e.g. 28/30), patients with an EDD in the next 3 days (turns amber when above 0), and total acuity (Physio / OT users only). Loaded once when Home opens into `colHomeStats`.
- `Equipment Dashboard` and `Team Info` buttons kept.

## Swap it in
1. Paste `Home_Main.pa.yaml` into Studio (it appears as `Home_Main`).
2. Search the app for `Home_PT` (Ctrl+F). Every `Navigate(Home_PT ...)` should become `Navigate(Home_Main ...)`.
3. **App → StartScreen** should be `Home_Main`.
4. Delete `Home_PT` once nothing points at it.
5. If `WrapCount` on `Gallery_Home` errors, delete that line (tiles then stack in one column).

---

# Equipment screen – `Equipment_Main.pa.yaml`

Replaces `Equipment_Screen`. Same three columns, new look (header bar, white cards, row cards, status pill on the details card).

- **My equipment** (left), **Today's allocations + search by patient** (middle), **Item details** (right).
- Selected row is highlighted. Item details show Equipment and (if allocated) Sign Out sections.
- **Bug fixed:** the old `OnVisible` built ward caches from 4A, 4B and 5A into the SAME collection (`colWard`), so they overwrote each other, and it would also overwrite the new ward screen's data. Those caches are removed.
- **Patient button** now looks the patient up directly in the four ward lists (Name + URN + DOB when the equipment record has them; Name only if URN/DOB are blank). Not found on any ward: the "Patient no longer found" popup, same Return / Leave allocated choices.
- Return logic (inventory update, usage log, 100-day service warning) is unchanged.
- Back button no longer checks the old `varHasUnsavedChanges_4A`.
- Email button says so if nothing was allocated today, instead of sending an empty email.
- Kept: nav buttons to Allocated / Available / Audit (Audit only for Director, Team Leader, CA4).

## Swap it in
1. Paste `Equipment_Main.pa.yaml` (appears as `Equipment_Main`).
2. Search the app for `Equipment_Screen`: change every `Navigate(Equipment_Screen ...)` to `Navigate(Equipment_Main ...)`. (Home_Main from commit onward already opens `Equipment_Main`.)
3. Delete `Equipment_Screen` when nothing points at it.

---

# Patient detail screen – `Patient_Detail_New.pa.yaml`

Replaces `Patient_Detail_Screen`. Screen name is `Patient_Detail_New` so it cannot clash. After deleting the old screen, **rename the new one to `Patient_Detail_Screen`**: every `Navigate(Patient_Detail_Screen ...)` in the app (Ward_All, Handover_All, Equipment_Main, etc.) then works again automatically.

- Works on the patient's own SharePoint row (`varSelectedPatient`, set by whoever opened the screen). It no longer uses `colWard` / `colWard6A`, so it works from any screen and any ward.
- The four editable fields (EDD, Maintenance, In-patient falls, Contact precautions) are edited locally, then saved straight to the patient's ward list with the header **Save** (or **Discard**). Back is blocked while there are unsaved edits.
- Those edits are no longer left as unsaved rows on the ward screen. That old flow lost them when the ward screen reloaded.
- **Bug fixed:** allocating equipment took the Ward from a view-only dropdown, so it always used the first ward in the list. It now uses the patient's own ward (`4A` / `4B` / `5A` / `6A`).
- **Bug fixed:** allocating did not save the patient's DOB on the equipment record. It now does.
- Equipment layout: allocated-to-this-patient list + find-by-barcode (middle), item details with Allocate / Return (right).
- The Outcome Measures, Exercise Setups and Therapy Summary buttons are removed (those screens no longer exist).
- Hidden OT and Speech rows dropped (they were read-only and hidden).

---

# All Allocated Equipment – `All_Allocated_New.pa.yaml`

Replaces `All_Allocated_Equipment`. Screen name is `All_Allocated_New`: delete the old screen, then rename this one to `All_Allocated_Equipment` (every `Navigate(All_Allocated_Equipment ...)` starts working again).

- Filters card (left): Category, Wheelchair type, Width / Depth / Height, Code, Patient, URN, plus **Reset**. Filters combine.
- The old "touched" flags and white cover-up labels are gone: a dropdown simply shows **All** until you pick something.
- Results (right): one card per item with a category colour bar, category chip, barcode, patient / ward / physio, signed-out date and **days out**. Tap anywhere on the row to open the patient.
- **Bug fixed:** the old screen found the patient in `colWard` / `colWard6A` by URN only. It now searches the four ward lists directly (Name + URN + DOB, or Name + URN if the equipment record has no DOB), so it works from any screen.
- Not found on any ward: "Patient no longer found" popup with **Return equipment** / **Leave allocated**. The return logic is unchanged.
- Control names end in `_Al` so they cannot clash with the old screen while both exist.

---

## All Available Equipment – `All_Available_New.pa.yaml`

Replaces `All_Available_Equipment`. Screen name is `All_Available_New`: delete the old screen, then rename this one to `All_Available_Equipment`.

Three cards: filters (left), list (middle), item details (right).
- Filters: Category, Wheelchair type, Width, Depth, Height, Barcode, "Service due only" tick. Reset button clears all.
- List: tap anywhere on a row to show it in the details card. Days-in-use pill goes red "SERVICE DUE" above 100 days.
- Removed: Patient / URN filters (available items have no patient) and the old row click that opened a blank patient.

---

## Audit Oversight – `Audit_Oversight_New.pa.yaml`

Replaces `scrAuditOversight`. Screen name is `Audit_Oversight_New`: delete the old screen, then rename this one to `scrAuditOversight` (so every `Navigate(scrAuditOversight …)` keeps working).

Layout: filter bar, 6 summary tiles, "By ward" list (left), audits list (right), details popup.

How it works (one place for the filter logic instead of 8 copies):
- `btnLoad_Au` (hidden): loads audits for the date range, builds the clinician list. Runs on open and when dates change.
- `btnFilter_Au` (hidden): applies clinician, ward, outcome and the Risks / Mismatch / Untagged toggles. Every filter control just calls it.
- Every filter (dates, ward, outcome, clinician, pills) applies to the tiles and the audits list.
- The "By ward" list follows every filter except ward, so you can always switch wards. Tap a ward to filter to it, tap again to clear.
- New variables and collections all start `au` / `colAu`, so nothing clashes with the old screen.
- "Untagged" everywhere = `TagResult` is not "OK".
- Removed: the unwired "Usage Dashboard" button (it had no action).

---

## Physio Team Info – `Physiotherapy_New.pa.yaml`

Replaces `Physiotherapy_Screen`. Screen name is `Physiotherapy_New`: delete the old screen, then rename this one to `Physiotherapy_Screen` (Home_Main already opens `Physiotherapy_Screen`).

- Header pills: Manage Staff (Directors / Team Leaders only), Data Dashboard, Leave Calendar. Same targets as before.
- Left card: Team Brief documents. Whole row is tappable. Folders open, files launch. New "Up" button goes up one level (old back arrow always jumped to the top). Path shown above the list.
- Right card: team notes. Old version saved to SharePoint on every keystroke. Now edit, then press **Save notes** (or Discard). Shows who last saved and when.
- Data Dashboard button: same collections built as before (`col4A_PieData` … `col6A_PieData`), 4 copies of the same code cut to one short line each.
- Edit password box and Unlock unchanged; wrong password now shows a message.
- OnVisible also sets `varMeDirectory` (same as Home) so the screen works if opened directly.

---

## Data Dashboard – `Physio_Data_New.pa.yaml`

Replaces `Physio_Data_Screen`. Screen name is `Physio_Data_New`: delete the old screen, then rename this one to `Physio_Data_Screen` (Physiotherapy_New's Data Dashboard button already opens `Physio_Data_Screen`).

- Four ward cards: total acuity, this week vs last week (▲ higher = red, ▼ lower = green), diagnosis pie. Tap a card for predicted staffing.
- "AFRM staffing" pill (header): 4A + 4B + 5A combined.
- Bottom card: average acuity per week, one line per ward (ward colours match the cards).
- Staffing popup: FTE per discipline on the left, patients by diagnosis on the right.
- Staffing maths now lives in one hidden button (`btnCalc_Dd`). The old file had it twice (once per ward tap, once for AFRM) and the two copies differed: the ward version left out **Clinical Psych** and did not ignore spaces/case when matching diagnoses. The single copy includes Clinical Psych.
- Card numbers are worked out once when the screen opens (`colDdWardStats`), not on every redraw.
- Needs (built elsewhere in the app): `colDiagnosisMap`, `colStaffRatios`, `colWardSummaryConfig`, `col4A_PieData` … `col6A_PieData`.

---

## Manage Staff – `Directory_Admin_New.pa.yaml`

Replaces `scrDirectoryAdmin`. Screen name is `Directory_Admin_New`: delete the old screen, then rename this one to `scrDirectoryAdmin` (Physiotherapy_New's Manage Staff button opens `scrDirectoryAdmin`).

Bugs fixed from the old screen:
- **Changing someone's access never saved.** The old dropdown only changed the app's temporary copy, then said "Access updated". It now writes to `ClinicianDirectory` and shows an error if SharePoint refuses.
- `Exit()` in the access checks and in Remove closes the whole app. Replaced with `Back()` and proper If / else.
- Remove was a one-tap hard delete. It now asks first.
- Add / Remove / access change now check SharePoint saved before saying "success".

Also:
- Compact rows (old rows were 175 tall, only 3 fitted). Search box on the staff list.
- Your own row: access dropdown is locked and there is no Remove button (you could lock yourself out).
- Access-level pie code was copied twice; now one hidden button (`btnPie_Ad`).
- Add Staff default access stays "HP3" as before.

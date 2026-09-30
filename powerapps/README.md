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

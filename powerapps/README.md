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

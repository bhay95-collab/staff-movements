# Ward 4A screen – Power Apps source

`Ward_4A.pa.yaml` = the Ward 4A screen. Restyled to match `index.html` (Staff Movement Tracker).

## What changed

**Look (from `index.html`)**

| Token | Value | Used for |
|---|---|---|
| Page background | `RGBA(235,242,248,1)` | Screen fill |
| Ink / Ink-2 / Muted | `RGBA(14,28,42,1)` / `RGBA(58,80,104,1)` / `RGBA(140,155,174,1)` | Text |
| Accent | `RGBA(26,90,153,1)` | Buttons, checkboxes, chevrons, focus |
| Good / Danger | `RGBA(12,122,82,1)` / `RGBA(180,26,26,1)` | Save / Discard, D/C |
| Line | `RGBA(14,42,70,0.12)` | All borders |
| Header | teal-navy gradient `#001D46 → #075F73 → #00838A` | Title bar (SVG image, see below) |
| Font | Segoe UI | Everything (Plus Jakarta Sans is not available in Power Apps) |

- Header bar: gradient + white pill buttons + live patient count subtitle.
- Cards: white, 18px radius, thin border, light shadow.
- Ward rows: 14px radius, thin border. Meaning of colours is unchanged: teal tint = falls risk, amber border = contact precautions, dark row = empty slot, amber EDD = due within 3 days, grey EDD = blank.
- Diagnosis dropdown colours unchanged (they match the pie chart).
- D/C = soft red pill. Save = green pill. Popups = dimmed backdrop, white 20px card, pill buttons.
- Patient List/Data panel: stat tiles, section headings, charts re-laid out with no overlaps.

**Fixes**

1. **Chart code was written twice** (OnVisible + Save). Now one copy in hidden button `btnRebuildCharts_4A`. Data load is also one copy in `btnLoadData_4A`. OnVisible, Save and Discard all call them.
2. **Discharge no longer deletes straight away.** D/C now queues the patient in `colPendingDischarge4A`. Outcome Measures / Exercise Setups are deleted only after Save succeeds. Not saved = nothing deleted.
3. **New Discard button** (header bar, appears when there are unsaved edits, asks to confirm). It undoes everything since the last save, including a discharge. Before this there was no way to leave the screen with unsaved edits except saving.
4. **"Unsaved changes" now uses the real dirty rows** (`IsDirty`). Before, editing a date or dropdown did not set `varHasUnsavedChanges_4A`, so Handover could be opened with unsaved edits and the Save pill did not pulse.
5. Save button greys out while saving (no double-tap).
6. D/C hidden on empty beds.

## Not changed (needs your decision)

- `RemoveIf` on `Patient_Outcome_Measures` / `Patient_Exercise_Setups` matches on **patient name only**. Two patients with the same name (or the same name on another ward) would both be wiped. Add a ward or URN condition if those lists have such a column.
- `RemoveIf` on SharePoint lists only sees the first 500 rows (Power Apps data row limit). Bigger lists may leave rows behind.
- Bar chart `ColumnChart1_2` has `Series1` to `Series9` all set to `TotalAcuity`. Looks like 9 identical bars per clinician.
- Dark rows (`field_2` blank) still show the normal controls on top.

## If something does not paste

- `imgHeaderGradient_4A` (gradient image): if Studio complains, delete it. The header falls back to a solid teal.
- `LayoutJustifyContent` on `Container211`: if it errors, delete that line. Buttons then sit left-aligned.
- Paste into a **copy** of the app first.

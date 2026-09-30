# STARS Equipment – mobile app rebuild

The old mobile app had **19 fixed-size screens**. This rebuild has **8 responsive screens** that fit any phone (and tablets), look like the desktop app, and share one copy of each piece of logic.

## Old → new

| Old screen(s) | New screen | File |
|---|---|---|
| Home | **Home** | `M1_Home.pa.yaml` |
| Search_Equipment_Screen, Wheelchair_Type_Screen, Brand_Screen, Model_Screen, Width_Screen, Depth_Screen, Height_Screen, Equipment_List_Screen | **Find** (one screen: barcode search, category tabs, a Filters button that opens a sheet of size chips, live results that fill the screen) | `M2_Find.pa.yaml` |
| Allocated_Equipment_Detail_Screen, Allocated_Equipment_Detail_Screen_QR, (detail part of) Equipment_Detail_Screen | **Item** (one detail screen for any item; shows Allocate or Return) | `M3_Item.pa.yaml` |
| Equipment_Patients, Equipment_Detail_Screen, Equipment_Detail_Tree_Screen | **Allocate** (pick patient, confirm in a bottom sheet) | `M4_Allocate.pa.yaml` |
| My_Equipment_Screen | **MyEquipment** (All / Today / 6+ weeks tabs, email today's list) | `M5_MyEquipment.pa.yaml` |
| Allocated_Equipment_Screen | **Allocated** (search + ward filter) | `M6_Allocated.pa.yaml` |
| Dashboard_Wheelchair_Type, Dashboard_Screen | **Availability** (type tabs, bar per width, tap a width to see the chairs) | `M7_Availability.pa.yaml` |
| scrAudit | **Audit** (numbered steps, one scroll, fixed Submit bar) | `M8_Audit.pa.yaml` |
| App OnStart | **App Formulas** (colours, font, header art, who am I) | `App_Formulas.txt` |

## Bugs fixed on the way
- `Exit()` in the audit closes the whole app on a phone. Replaced with normal If/else.
- Audit marked **EscalationSent = true even when no email was sent** (second Patch ran regardless). Now only set after the email goes.
- "Today's allocations" listed **everyone's** allocations, and the email said "you allocated". Now yours only.
- `Equipment_Detail_Tree_Screen` allocated equipment **without writing the usage log**. Removed (one Allocate screen, always logs).
- Two different shapes of `colPatients` (allocation vs audit) clashed. One shape now.
- Allocation could double-book: it now re-reads the item and stops if someone else allocated it a moment ago.
- Ward drop-down silently defaulted to the first ward for "Other patient". Now starts empty.
- Blank dates showed a fake "31/12/2001". They now say "Not set" / "Optional".
- The 6-week reminder popped up as a long notification on every start. Now a tappable card on Home.

## Build it (step by step)

Do this in a **copy** of the current mobile app so every SharePoint connection is kept.

1. **Copy the app.** Open the current mobile app in Power Apps Studio. **File → Save as** → name it `STARS Equipment Mobile v2` → **Save**. Keep working in the copy. The original is untouched.
2. **Make it resize.** **Settings → Display**:
   - Scale to fit: **Off**
   - Lock aspect ratio: **Off**
   - Orientation: **Portrait**
   - Lock orientation: **On**

   Then **Settings → General → Data row limit**: `2000`.
3. **Check the data.** Click the **Data** icon (cylinder, left). These must be listed:
   - `Equipment_Inventory_SharePoint`
   - `Equipment_Usage_Log`
   - `Equipment_Audits`
   - `ClinicianDirectory`
   - `Ward_4A_Shared`, `Ward_4B_Shared`, `Ward_5A_Shared`, `Ward_6A_Shared`
   - `Office365Outlook`

   If `Office365Outlook` is missing: **Add data → Office 365 Outlook**.
4. **App settings code.**
   - In the Tree view click **App**. In the property drop-down (top left, next to the formula bar) pick **OnStart**. Delete everything in it.
   - Same drop-down, pick **Formulas**. Paste the whole of `App_Formulas.txt`.
5. **Clear the old screens.**
   - Right-click the old **Home** screen → **Rename** → `OLD_Home`.
   - Delete every other old screen (right-click → **Delete**). Power Apps needs one screen to remain, so keep `OLD_Home` for now.
6. **Paste the 8 new screens, in order** M1 → M8 (same method as the desktop screens):
   - open the file link, **Copy raw file**,
   - in Studio click a screen in the Tree view, press **Ctrl+V**.
   - The screen arrives with its name: `Home`, `Find`, `Item`, `Allocate`, `MyEquipment`, `Allocated`, `Availability`, `Audit`.

   Red errors that name a screen that isn't pasted yet (for example `Item`) clear once all 8 are in.
7. **Finish.**
   - Drag **Home** to the top of the Tree view (the first screen is the start screen).
   - Delete `OLD_Home`.
   - **Ctrl+S**.
   - Open **App checker** (stethoscope icon). It should show no errors.
8. **Test on a phone** (Power Apps mobile app). The barcode scanner only works on a device. See the checklist below.
9. **Publish**, share with the team, then retire the old app.

## Test checklist
- Home: greeting, scan an item, each of the 5 tiles, 6-week card (if you have old items).
- Find: barcode search; each category tab; tap chips to narrow, tap again to clear; "Clear filters"; open an item.
- Item: an available item shows **Allocate**; an allocated item shows who has it and **Return** (asks first).
- Allocate: My patients / All / + Other; tap a patient; fields are pre-filled; Allocate → lands on My equipment → Today.
- My equipment: three tabs; **Email today's list** arrives in your inbox.
- All allocated: search by code, patient, physio, URN, width; ward chips.
- Availability: type tabs; bars; tap a width → Find opens pre-filtered.
- Audit: scan or type a code; pick the patient; match banner; toggles; tag result; comment rule; Submit (try one PASS and one FAIL on test data – the FAIL emails the treating physio).
- Rotate / try a small and a large phone: nothing should be cut off; long pages scroll.

## Layout note (why widths are written as App.Width)
Inside an auto-layout container Power Apps sizes each child itself, but the child's own **Width** property still returns whatever formula it holds. Controls inside that child that use `Parent.Width` then get the wrong number (text centred off the button, pills in the wrong place). Every auto-layout child therefore has its real width written out from `App.Width` (for example `(App.Width - 48) / 3` for three tabs), so everything inside lines up on any phone.

## Layout check
Every screen was drawn in a layout simulator at 390x780 and 360x640 (and with its bottom sheet open) and checked for overlaps, clipped text and wrong widths. Fixes from that pass:
- Find: the six filter rows took over half the screen. They now live in a **Filters** sheet; the top of the screen is just search, category tabs, a Filters button with the count, and a one-line summary of what is selected.
- My equipment: three-line cards were 8px too short; taller now.
- All list cards: inset 2px so their borders are no longer clipped by the list edge.
- Allocate sheet: sized to its content (was a tall empty sheet).

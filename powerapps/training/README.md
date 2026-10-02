# Physiotherapy Training Register (2 screens)

Screens: `Home` and `scrTrainingSessions` (same names as before, so nothing else needs renaming). Works on phone, tablet and desktop.

## Set up (once)
1. **Settings → Display:** Scale to fit **Off**, Lock aspect ratio **Off**, Lock orientation **Off**.
2. **App > Formulas:** paste all of `App_Formulas.txt` (colours, font, header art, and the screen-size formulas `Wide`, `UI`, `PageW`, `Gutter`, `GapPx`, `ListW`, `DetailX`, `DetailW`, `SheetW`).
3. Delete the old `Home` and `scrTrainingSessions` screens (or rename them `OLD_...`), paste the two new ones, drag `Home` to the top of the Tree view, delete the old ones, save.
4. Data: `TrainingSessions`, `TrainingBookings`, `TrainingWaitlist`, `Office365Outlook` and the flows `TrainingBookingConfirmationEmail` and `TrainingWaitlistNotification` must stay connected (nothing new is needed).
5. `varCanManageTraining` is still read exactly as before (the screens use `Coalesce(varCanManageTraining, false)`). It must be set somewhere, e.g. in App OnStart. It was not in the code you sent, so if you never set it nobody sees the manager buttons.

## Layout
- **Wide (screen 820 or wider: desktop, tablet landscape):** dates on the left, the chosen date on the right (date, status, the main button, attendee slots, quiet manager links along the bottom of the card). The first date is selected automatically. There is no bottom bar: the Book / Join / Leave / Remove button sits inside the date card, right under the status line.
- **Narrow (phone, tablet portrait):** one column. The list of dates first; tap a date to see it; the back arrow returns to the list, then to Home.
- Text, buttons and gaps scale with the screen (`UI`); the content column stops at 1280 wide and is centred.
- Same look as the other STARS apps: teal/navy header, cards, pill buttons.

## Bugs fixed
1. **Join Waitlist did nothing.** Its OnSelect held a copy of the show/hide test instead of saving a row. It now writes a `TrainingWaitlist` row.
2. **Join Waitlist appeared with 6 booked, even for Manual Handling (8 places).** It was hard-coded to 6. Capacity is now read from the session (6 for Basic Life Support, 8 for Manual Handling when blank) everywhere.
3. **Someone on the waitlist could not book** when a place opened (the Book button was hidden while they were waiting), although the email tells them to book. They can now book, and their waitlist row is closed automatically.
4. **Email attendees was unreachable** (the popup existed but no button opened it). Managers now have an **Email attendees** button.
5. **Emails lost their line breaks** (plain text sent as HTML). Line breaks are now converted, and the waitlist email no longer mentions "Teams".
6. **"Room *ADD ROOM HERE*" placeholder** in the attendee email: it now uses the date's Location.
7. **Delete erased the date** from SharePoint. It now sets `IsActive = false`, so the history stays. It is still blocked while people are booked or waiting.
8. **Two people could take the same slot at the same moment.** The booking is re-checked after saving; the later one is cancelled with a message.
9. **Booking and cancelling had no checks:** now re-checks capacity and "already booked" with fresh data, checks for save errors, and a failed email no longer hides a successful booking.
10. **`DateValue(dpNewSessionDate.SelectedDate)`** (text conversion of a date, depends on the PC's language) replaced by the date itself; a date or time that has already passed is rejected.
11. **Very slow screen:** every date row and every slot ran its own SharePoint query on every refresh. Data is now read once per open (and on the refresh button) and worked out on the device.
12. **Slot labels, session counts and the delete button used a stale copy** of the chosen date; the chosen date is refreshed after every change.
13. Removing your booking happened instantly with no confirmation; it now asks first.
14. Tiny (10 pt) text and fixed 1366 x 768 layout: replaced by the responsive layout.

## New
- **My upcoming bookings** on Home, with slot numbers; tap one to open that date.
- Home tiles show the next date and places left (or "Full, join the waitlist", or "You are booked in").
- Status banner on each date: "You are booked in (slot 3)", "You are on the waitlist (2 of 5)", "A place is free", "Full".
- Waitlist position.
- Managers can remove an attendee (tap their slot), see/email the waitlist, email attendees, add dates (any type, default capacity by type) and delete dates, all from the date screen.
- Refresh button on the dates list.

## Assumptions to check
- Waitlist row columns used: `Title`, `SessionID`, `WaitlistUserName`, `WaitlistUserEmail`, `WaitlistStatus` (Waiting / Removed), `AddedOn`.
- Booking row columns: as in your code (`Title`, `SessionID`, `TrainingType`, `SessionDate`, `SlotNumber`, `BookedUserName`, `BookedUserEmail`, `BookingStatus` Booked / Cancelled, `BookedOn`).
- Capacity defaults (6 / 8) are unchanged; set `Capacity` on the date to override.
- The background picture (`mnh-team-bg-stars`) is no longer used so the app matches the other STARS apps; it can be put back on the screen's BackgroundImage.

## Emails (branded)
Email attendees and Email waitlist use the shared email look. Re-paste the whole of `App_Formulas.txt` (it now ends with `EmailHead` and `EmailFoot`), then paste `scrTrainingSessions.pa.yaml`.

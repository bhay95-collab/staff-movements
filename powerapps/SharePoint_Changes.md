# SharePoint changes needed for the next builds

Do these **before** pasting the new screens, then add the list to **both** apps (Data panel → Add data → SharePoint → your site → tick `Service_Log`).

## 1. New list: `Service_Log`
One row per service episode (created when an item is sent, completed when it comes back).
Create the list (Blank list), then add the columns **with exactly these names** (column names matter; no spaces).

| Column name | Type | Notes |
|---|---|---|
| Title | Single line of text | already exists. Holds the barcode |
| EquipmentItemID | Number | no decimals |
| Category | Single line of text | |
| Brand | Single line of text | |
| Model | Single line of text | |
| Width | Single line of text | |
| Depth | Single line of text | |
| Height | Single line of text | |
| WheelchairType | Single line of text | |
| ServiceType | Choice | `Full service`, `Repair`, `Safety check`, `Other` |
| ServiceStatus | Choice | `In Service`, `Completed` |
| SentDateTime | Date and time | include time |
| SentByName | Single line of text | |
| SentByEmail | Single line of text | |
| DaysInUseAtSend | Number | no decimals |
| SendNotes | Multiple lines of text | plain text |
| ReturnedDateTime | Date and time | include time |
| ReturnedByName | Single line of text | |
| ReturnedByEmail | Single line of text | |
| Outcome | Choice | `Serviced and returned to stock`, `Repaired and returned to stock`, `Condemned - out of service` (plain hyphen) |
| ReturnNotes | Multiple lines of text | plain text |
| DaysAtService | Number | no decimals |
| SourceApp | Choice | `Mobile`, `Web` |

Tip: in the list settings, **Index** the columns `ServiceStatus` and `SentDateTime`.

## 2. Existing list: `Equipment_Inventory_SharePoint`
1. Column **Status** (Choice): add two choices `In Service` and `Out of Service` (keep Available and Allocated).
2. New column **LastServiceDate**, type **Date and time** (date only is fine).

Nothing else changes. Existing columns used by the new screens: `TotalDaysSignedOut`, `OutOfService`, `IsActive`, `Location` (Choice).

## What the app does with them
- **Send for service** (mobile Servicing screen): item Status becomes `In Service`, a `Service_Log` row is added. Items in service never show in Find (Find only lists `Available`).
- **Return from service**: item goes back to `Available` (or `Out of Service` + `OutOfService` = Yes + `IsActive` = No if condemned), `LastServiceDate` = today, **`TotalDaysSignedOut` is reset to 0 after a Full service**, location is recorded.

---
name: financial-spreading
description: Use this skill when spreading a company's P&L or balance sheet into a standardized account/category taxonomy for M&A due diligence, valuation, or CIM prep. Covers extraction, classification, and completeness verification.
---

# Financial Statement Spreading

## When to use this skill
Trigger this whenever the task involves extracting line items from a P&L or
balance sheet (accrual or tax-basis) and organizing them into a standardized
account/category taxonomy — the core recurring task in sell-side M&A due
diligence and valuation prep.

## Extraction rules

1. Extract **every raw line item**, excluding subtotals, in the exact order
   they appear on the statement.
2. Keep labels **verbatim** — including typos or inconsistent formatting from
   the source document. Do not "clean up" account names.
3. Do not assume account structure carries over from a prior year or a
   similar company. Rebuild the line structure fresh from each year's
   statement, since accounts frequently change year to year.

## Classification rules

- Tag **INCOME** for: revenue lines (including contra-revenue items like
  sales discounts) and Other Income lines.
- Tag **EXPENSE** for: everything else, including contra-expense items
  (e.g. reimbursed permit costs, purchase discounts, reimbursements) and
  Other Expense lines.

## Completeness verification (required before delivering any spread)

Verify completeness **two separate ways** — a subtotal tie alone is not
sufficient, since it will not catch an omitted zero-value line:

1. **Subtotal tie:** Sum the extracted values within each block (revenue,
   COGS, opex, etc.) and confirm the sum matches the statement's printed
   subtotal for that block.
2. **Line count check:** Count the number of extracted line items against
   the number of line items visible in the source statement for that block.

## Common errors to watch for
- Omitting major lines (e.g. depreciation expense) — easy to miss if it's
  formatted differently from surrounding lines.
- Digit transcription typos when copying values.
- Merging or skipping detail lines in long, granular sections (e.g. repair
  and maintenance, fuel).
- Dropping $0.00 lines — these are real accounts and must still appear in
  the spread even though a subtotal tie won't reveal their absence.

## Output format
Present the spread as a table with columns: Line Item (verbatim label),
Category (INCOME/EXPENSE), and Value. Include a completeness confirmation
statement at the end noting both checks were performed.
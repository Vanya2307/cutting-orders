# Cutting Orders

![Онлайн заявки за рязане и кантиране](docs/banner.svg)

**English** | [Български](README.bg.md)

Online cutting and edge-banding orders for a furniture workshop, with Excel export for cutting software.

**Author:** Vanya Videva  
**Course:** Python Web - Django Basics, SoftUni  
**Date:** October 2026

---

## About

Clients choose materials, enter parts with dimensions and edge banding, select additional processing and attach drawings. Before submission, they review the complete order. Submission assigns an order number, locks editing and generates an Excel file.

The project is based on practical work in a furniture workshop. The Excel export follows the workshop's table format. The user interface is in Bulgarian.

> The aim is to reduce manual retyping of dimensions from paper forms and make orders easier to check and prepare for production.

## Features

**Catalog**

- Materials with type, manufacturer, decor, thickness, board size and grain.
- Services with drawing requirements: not needed, recommended or required.
- Create, view, edit and delete pages for materials and services.
- Search by decor code or name from the navigation bar.
- Multiple-word search with support for common Cyrillic case variants.
- Protection against deleting materials and services used in orders.

**Orders**

- Orders start with the client's contact details.
- Phone numbers are normalized to `+359` and used to find existing client records.
- Materials are chosen from a list filtered by type, manufacturer and decor.
- The selected material is locked in the part form.
- Parts include dimensions, quantity, grain direction, four edges, processing, euro-joints and notes.
- Parts can be added, edited and deleted while the order is a draft.
- The order review groups parts by material in a compact table.
- Multiple drawings can be attached: PDF, JPG and PNG, up to 5 MB per file.

**Production checks**

- Parts must fit the usable board size after trimming.
- Size validation takes the selected grain direction into account.
- Materials with grain require a direction or an explicit “Без значение” selection.
- Standard euro-joints are allowed only for worktops with a part width of 600 mm.

**Submission**

- A confirmation page shows the order before submission.
- The client must confirm that dimensions, edges and processing have been checked.
- Submission is blocked if the order has no parts or a required drawing is missing.
- A warning is shown when a drawing is recommended but not attached.
- Submitted orders receive a number such as `A-2026-0001` and become read-only.
- An Excel file is generated and can be downloaded from the order page.

**Other pages**

- Home page with live material and service counts.
- “Моите поръчки” with drafts and submitted orders accessible in the browser session.
- Custom 404 page.

## Privacy and Access

- Clients enter their own contact details. There is no public client directory.
- Order access is limited to the browser session that created the order.
- Entering an existing phone number does not grant access to previous orders.
- Order pages, drawings and Excel downloads are checked against the session.
- Anyone sharing the same browser profile and session shares access to those orders.
- Clearing cookies or session expiry may remove access. The orders remain stored in the database.
- Submitted orders are read-only, with restrictions enforced in the views.

Authentication is excluded from this course project. Catalog editing is open in this version, which is intended for local demonstration. Accounts and staff-only management are planned for a later version.

Submission stores the order and creates its Excel file. Email delivery is planned for a later version.

## Tech Stack

- Python 3.12
- Django 6.1.2
- SQLite
- openpyxl for Excel export
- Bootstrap 5 and custom CSS

## Repository Structure

- `catalog/`  
  Materials and services: models, forms, filtering and CRUD views.
- `orders/`  
  Clients, orders, parts and drawings. Session access, submission and downloads.
- `orders/templatetags/order_extras.py`  
  Custom `edge` filter for displaying edge thickness.
- `production/excel.py`  
  Excel file generation with openpyxl.
- `templates/`  
  Base, home and 404 pages, and page templates grouped by app (`catalog/`, `orders/`).
- `templates/includes/`  
  Shared navigation and footer.
- `static/css/style.css`  
  Site styling, with colors defined through CSS variables.
- `docs/`  
  Images for this README.

## Setup

Python 3.12 and pip are required. Clone the repository with Git, or download and extract its ZIP archive.

1. Clone the repository:

   ```bash
   git clone https://github.com/Vanya2307/cutting-orders.git
   cd cutting-orders
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it using the command for your system.

   **Linux / macOS / WSL:**

   ```bash
   source .venv/bin/activate
   ```

   **Windows PowerShell:**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **Windows Command Prompt:**

   ```bat
   .venv\Scripts\activate.bat
   ```

4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Apply the migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the server:

   ```bash
   python manage.py runserver
   ```

7. Open <http://127.0.0.1:8000/>.

No environment variables or database credentials are required for local testing. SQLite creates the local database when migrations are applied. No prepopulated data is required.

Uploaded drawings and generated Excel files are stored in `media/`. These files and the local database are excluded from version control.

### First Use

1. Open **Материали** and add a material.
2. Open **Услуги** and add a service with its drawing requirement.
3. Choose **Нова поръчка** and enter contact details.
4. Select a material, add parts and attach drawings where needed.
5. Review the order, confirm the details and submit it.
6. Download the Excel file.

Use **Моите поръчки** to return to drafts and submitted orders while the browser session remains active.

All objects can be created through the site's navigation. Django admin and direct database editing are not required.

## Excel File

The export follows the working table used in the workshop.

| Column | Content |
| --- | --- |
| A | Reference number, restarting at 1 for each material |
| B | Material |
| C | Grain direction: `L`, `W` or empty |
| D | Part name |
| E, F | Length and width in mm |
| G | Quantity |
| H-K | Edges: L top, L bottom, W left, W right |
| L | Other notes |
| M | Material thickness in mm |
| N | Order number and contact name for labels |
| O | Processing and euro-joints |

Row 1 contains the order number, contact name, phone and submission date. Rows 2-3 contain headers. Two empty rows separate material groups.

Dimensions, quantities, edges and thicknesses are numeric. Unbanded edges are empty cells. Long material names and notes wrap within their cells.

## Future Work

- User accounts and persistent order history.
- Workshop area for managing orders, clients and production status.
- Staff-only catalog editing.
- Email notifications for submitted orders.
- Material photos in the catalog.
- Euro-joint illustrations in the part form.

## Course Materials

Kalaydzhiev, D. Python Web - Django Basics. SoftUni, 2026.

## Acknowledgments

This project was developed with the assistance of Claude (Anthropic).
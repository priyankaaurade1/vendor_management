Vendor Management System

Overview:
A Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics.

Setup Instructions
1. Clone the repository:
    git clone [vendor_management.git](https://github.com/priyankaaurade1/vendor_management.git)

2. Install dependencies:
    pip install -r requirements.txt

3. Apply migrations:
    python manage.py migrate

4. Run the development server:
    python manage.py runserver

5. Access the API:
    Visit http://localhost:8000/ in your web browser.


API Endpoints:

Vendor Profile Management

- Create a Vendor Profile:
    POST /api/vendors/: Create a new vendor profile.
- List Vendors:
    GET /api/vendors/list/: List all vendors.
- Get Vendor Details:
    GET /api/vendors/<vendor_id>/: Retrieve details of a specific vendor.
- Edit Vendor Profile:
    POST /edit_vendor/<vendor_id>/: Edit a vendor profile.
- Delete Vendor Profile:
    POST /vendor/<vendor_id>/delete/: Delete a vendor profile.

Purchase Order Tracking

- Create Purchase Order:
    POST /api/purchase_orders/: Create a new purchase order.
- List Purchase Orders:
    GET /api/purchase_orders/list/: List all purchase orders.
- Get Purchase Order Details:
    GET /api/purchase_orders/<po_id>/: Retrieve details of a specific purchase order.
- Update Purchase Order:
    POST /edit_orders/<po_id>/: Update a purchase order.
- Delete Purchase Order:
    POST /order/<po_id>/delete/: Delete a purchase order.

Performance Evaluation
- View Vendor Performance:
    GET /api/vendors/<vendor_id>/performance: View performance metrics of a vendor.
- View Historical Performance:
    GET /historical_details: View historical performance data.
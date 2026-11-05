from flask import Flask, render_template, request, redirect, url_for, Response

app = Flask(__name__)

# Persistent operational database state
inventory = {}
categories = ["Electronics", "Clothing", "Footwear", "Home Appliances"]
sizes = ["Small", "Medium", "Large", "XL", "N/A"]

@app.route("/", methods=["GET", "POST"])
def home():
    msg = None
    if request.method == "POST":
        brand = request.form.get("brand")
        category = request.form.get("category")
        item_type = request.form.get("item_type")
        color = request.form.get("color")
        size = request.form.get("size")
        
        # Streamlined Enterprise Architecture Logic for unique SKU tracking
        sku = f"{brand[:3].upper()}-{category[:2].upper()}-{item_type[:2].upper()}-{color[:2].upper()}"
        
        inventory[sku] = {
            "brand": brand,
            "category": category,
            "type": item_type,
            "color": color,
            "size": size
        }
        msg = f"Architecture String {sku} Generated Successfully!"
        
    return render_template("index.html", inventory=inventory, categories=categories, sizes=sizes, msg=msg)

# Feature: Purge/Delete records from real-time engine
@app.route("/delete/<sku>")
def delete_sku(sku):
    if sku in inventory:
        del inventory[sku]
    return redirect(url_for("home"))

# Feature: Data Mining Stream to Export Database to CSV/Excel
@app.route("/export")
def export_csv():
    csv_data = "SKU,Brand,Category,Product Type,Color,Size\n"
    for sku, details in inventory.items():
        csv_data += f"{sku},{details['brand']},{details['category']},{details['type']},{details['color']},{details['size']}\n"
    
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=sku_inventory_report.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True)

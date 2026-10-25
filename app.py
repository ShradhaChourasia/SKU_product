from flask import Flask, render_template, request

app = Flask(__name__)

# --- HAMARI PYTHON DATA STRUCTURES ---
# 1. TUPLE: Fixed options jo change nahi honge
CATEGORIES = ('Electronics', 'Clothing', 'Footwear', 'Home Appliances')
SIZES = ('Small', 'Medium', 'Large', 'Extra Large', 'Not Applicable')

# 2. DICTIONARY: Hamari tijori (Database) jahan saara data save hoga
inventory_db = {}

# 3. SET: Sirf unique SKUs track karne ke liye (Taaki duplicate na ho)
unique_skus = set()

# --- WEBPAGE ROUTE (Rasta) ---
@app.route('/', methods=['GET', 'POST'])
def home():
    message = None
    msg_type = None

    if request.method == 'POST':
        brand = request.form.get('brand').strip()
        category = request.form.get('category')
        item_type = request.form.get('item_type').strip()
        color = request.form.get('color').strip()
        size = request.form.get('size')

        if brand and item_type and color:
            # --- SKU GENERATION LOGIC (String Slicing) ---
            brand_code = brand[:3].upper()      # e.g., Nike -> NIK
            type_code = item_type[:3].upper()   # e.g., T-Shirt -> TSH
            color_code = color[:2].upper()      # e.g., Red -> RE
            size_code = "NA" if size == "Not Applicable" else size[:2].upper()

            sku = f"{brand_code}-{type_code}-{color_code}-{size_code}"

            # --- SET & DICT USE ---
            if sku in unique_skus:
                message = f"⚠️ SKU '{sku}' pehle se inventory me hai!"
                msg_type = "error"
            else:
                unique_skus.add(sku)
                inventory_db[sku] = {
                    'brand': brand,
                    'category': category,
                    'type': item_type,
                    'color': color,
                    'size': size
                }
                message = f"🎉 Success! Naya SKU bana: {sku}"
                msg_type = "success"
        else:
            message = "⚠️ Please saari fields fill karein!"
            msg_type = "error"

    return render_template('index.html', 
                           categories=CATEGORIES, 
                           sizes=SIZES, 
                           inventory=inventory_db,
                           msg=message,
                           m_type=msg_type)

if __name__ == '__main__':
    app.run(debug=True)

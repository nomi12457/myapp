from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "change_this_to_something_secure_change_later"

# SQLite database file
basedir = os.path.abspath(os.path.dirname(__file__))
db_filename = 'noman_rashid.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, db_filename)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model for entries (you can use entries to add people/items)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instagram = db.Column(db.String(200), nullable=True)
    whatsapp = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Item {self.id} {self.name}>"

# Home page / profile + list
@app.route('/')
def index():
    items = Item.query.order_by(Item.created_at.desc()).all()
    # Personal info shown separately
    profile = {
        "name": "Noman",
        "instagram": "nomestheticx",
        "whatsapp": "0322 9287452",
        "bio": "Welcome to my personal page. I use this small site to store contacts/items and link to my Instagram and WhatsApp."
    }
    return render_template('index.html', items=items, profile=profile)

# Add Item
@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name', '').strip()
    desc = request.form.get('description', '').strip()
    insta = request.form.get('instagram', '').strip()
    whts = request.form.get('whatsapp', '').strip()

    if not name:
        flash("Name is required.", "error")
        return redirect(url_for('index'))

    item = Item(name=name, description=desc, instagram=insta, whatsapp=whts)
    db.session.add(item)
    db.session.commit()
    flash("Item added successfully.", "success")
    return redirect(url_for('index'))

# Edit Item
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        desc = request.form.get('description', '').strip()
        insta = request.form.get('instagram', '').strip()
        whts = request.form.get('whatsapp', '').strip()

        if not name:
            flash("Name is required.", "error")
            return redirect(url_for('edit_item', item_id=item_id))

        item.name = name
        item.description = desc
        item.instagram = insta
        item.whatsapp = whts
        db.session.commit()
        flash("Item updated successfully.", "success")
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

# Delete Item
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully.", "success")
    return redirect(url_for('index'))

# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # debug=True for local development; set False if deploying
    app.run(debug=True)
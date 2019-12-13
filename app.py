from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.items


@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg="ash's phones")


@app.route('/collections')
def collections_index():
    """Show all collections"""
    return render_template('collections_index.html', items=items.find({}))


@app.route('/inventory', methods=['POST'])
def items_submit():
    """Submit a new collection of items."""
    item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('image')
    }
    print(item)
    items.insert_one(item)
    return redirect(url_for('items_show', item_id=item['_id']))


@app.route('/inventory/new')
def inventory_new():
    """Create a new item for the collection."""
    return render_template('collections_new.html', item={}, title='New Collection')


@app.route('/collections/<item_id>')
def items_show(item_id):
    """Show a single collection."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('items_show.html', item=item)


@app.route('/collections/<item_id>/edit')
def items_edit(item_id):
    """Show the edit form for an item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('items_edit.html', title='Edit Items', item=item)


@app.route('/collections/<item_id>/edited', methods=['POST'])
def items_update(item_id):
    """Submit an edited item."""
    updated_item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('images')
    }
    items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})

    item = items.find_one({'_id': ObjectId(item_id)})["_id"]
    return redirect(url_for('items_show', item_id=item))


@app.route('/collections/<item_id>/delete', methods=['POST'])
def items_delete(item_id):
    """Delete one item."""
    items.remove({'_id': ObjectId(item_id)})
    return redirect(url_for('collections_index'))


if __name__ == '__main__':
    app.run(debug=True)

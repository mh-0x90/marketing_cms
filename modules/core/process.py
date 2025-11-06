from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        # Get data from client
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        submitted_total = float(request.form['total_amount'])
        
        # Check if product exists FIRST
        product = products.get(product_id)
        if not product:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
        
        actual_price = product['price']
        
        # VULNERABLE: Only checks if total is positive, not if it matches actual price
        if submitted_total > 0:
            # Process order with whatever amount client sent
            order_result = process_order(product_id, quantity, submitted_total)
            return jsonify({
                'status': 'success', 
                'message': f'Order processed for ${submitted_total}',
                'product': product['name'],
                'quantity': quantity,
                'total_charged': submitted_total,
                'actual_should_be': f'${actual_price * quantity}'  # For demo purposes
            })
        else:
            return jsonify({'status': 'error', 'message': 'Total must be positive'}), 400
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# generate_sample_data.py
# Run this script to generate realistic sample CSV files

import csv
import random
from datetime import datetime, timedelta

# Sample data pools
FIRST_NAMES = [
    'Rahul', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anjali', 'Rohan', 'Neha',
    'Karan', 'Pooja', 'Arjun', 'Divya', 'Sanjay', 'Kavita', 'Rajesh', 'Meera',
    'Aditya', 'Riya', 'Manish', 'Shreya', 'Nikhil', 'Ananya', 'Suresh', 'Preeti',
    'Deepak', 'Sakshi', 'Anil', 'Swati', 'Harsh', 'Nikita'
]

LAST_NAMES = [
    'Sharma', 'Patel', 'Kumar', 'Reddy', 'Singh', 'Verma', 'Gupta', 'Agarwal',
    'Mehta', 'Joshi', 'Desai', 'Rao', 'Iyer', 'Nair', 'Malhotra', 'Kapoor',
    'Chauhan', 'Pandey', 'Mishra', 'Tripathi'
]

PRODUCTS = {
    'Electronics': [
        ('Dell Laptop', 55000, 65000),
        ('HP Laptop', 45000, 55000),
        ('MacBook Air', 95000, 120000),
        ('iPhone 15', 79900, 89900),
        ('Samsung Galaxy S24', 69999, 79999),
        ('iPad Pro', 89900, 99900),
        ('Samsung TV 55"', 45000, 55000),
        ('LG TV 43"', 30000, 35000),
        ('Sony Headphones', 8999, 12999),
        ('JBL Speaker', 5999, 8999),
        ('Canon Camera', 45000, 65000),
        ('Nikon Camera', 55000, 75000),
        ('Apple Watch', 42900, 49900),
        ('Fire TV Stick', 3999, 4999),
        ('Kindle', 8999, 10999),
        ('Gaming Console PS5', 49990, 54990),
        ('Wireless Mouse', 899, 1499),
        ('Mechanical Keyboard', 3999, 5999),
        ('Monitor 27"', 15000, 20000),
        ('Printer HP', 8999, 12999)
    ],
    'Clothing': [
        ('Nike Shoes', 4999, 7999),
        ('Adidas Sneakers', 5999, 8999),
        ('Levis Jeans', 2499, 3999),
        ('Formal Shirt', 999, 1999),
        ('T-Shirt Pack (3)', 899, 1499),
        ('Casual Dress', 1499, 2999),
        ('Winter Jacket', 3999, 5999),
        ('Sports Track Pants', 1299, 2499),
        ('Saree', 1999, 4999),
        ('Kurta Set', 1499, 2999),
        ('Leather Belt', 499, 999),
        ('Watch Fastrack', 1999, 3999),
        ('Sunglasses', 799, 1999),
        ('Handbag', 1999, 3999),
        ('Backpack', 1499, 2999)
    ],
    'Home': [
        ('Office Chair', 5999, 12000),
        ('Study Table', 4999, 8999),
        ('Bed Queen Size', 15000, 25000),
        ('Sofa 3-Seater', 20000, 35000),
        ('Dining Table Set', 18000, 30000),
        ('Mattress', 8999, 15999),
        ('Curtains', 1499, 2999),
        ('Bedsheet Set', 899, 1999),
        ('Table Lamp', 799, 1499),
        ('Wall Clock', 499, 999),
        ('Carpet 6x4', 2999, 4999),
        ('Bean Bag', 2499, 3999),
        ('Bookshelf', 3999, 6999),
        ('Mirror Large', 1999, 3499),
        ('Kitchen Utensil Set', 1499, 2499)
    ],
    'Stationery': [
        ('Python Programming Book', 499, 799),
        ('Data Science Book', 599, 899),
        ('Novel Set', 999, 1499),
        ('Notebook Pack (10)', 299, 499),
        ('Pen Set Premium', 499, 799),
        ('Art Supplies Kit', 1499, 2499),
        ('Calculator Scientific', 599, 999),
        ('File Folders (20)', 299, 599),
        ('Whiteboard', 1499, 2499),
        ('Pencil Box', 199, 399)
    ],
    'Sports': [
        ('Yoga Mat Premium', 999, 1999),
        ('Dumbbell Set 20kg', 2999, 4999),
        ('Resistance Bands', 799, 1299),
        ('Cricket Bat', 1999, 3999),
        ('Football', 799, 1499),
        ('Badminton Racket', 1499, 2999),
        ('Gym Bag', 999, 1999),
        ('Cycling Gloves', 499, 899),
        ('Running Shoes', 3999, 6999),
        ('Treadmill', 25000, 45000)
    ]
}

CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata',
    'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Indore',
    'Kochi', 'Visakhapatnam', 'Nagpur', 'Vadodara', 'Surat', 'Coimbatore'
]

PAYMENT_METHODS = [
    'Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash on Delivery', 'Wallet'
]

def generate_orders(num_orders=500, date=None):
    """Generate realistic order data"""
    if date is None:
        date = datetime.now().date()
    
    orders = []
    used_order_ids = set()
    
    for i in range(num_orders):
        # Generate unique order ID
        while True:
            order_id = f"ORD{date.strftime('%Y%m%d')}{random.randint(1000, 9999)}"
            if order_id not in used_order_ids:
                used_order_ids.add(order_id)
                break
        
        # Customer details
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        customer_name = f"{first_name} {last_name}"
        customer_email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"
        
        # Product details
        category = random.choice(list(PRODUCTS.keys()))
        product, min_price, max_price = random.choice(PRODUCTS[category])
        quantity = random.choices([1, 2, 3, 4, 5], weights=[60, 25, 10, 3, 2])[0]
        price = random.randint(int(min_price), int(max_price))
        
        # Other details
        payment_method = random.choice(PAYMENT_METHODS)
        shipping_city = random.choice(CITIES)
        
        # Add random hours to spread orders throughout the day
        order_time = datetime.combine(date, datetime.min.time()) + timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        order = {
            'order_id': order_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'product': product,
            'category': category,
            'quantity': quantity,
            'price': price,
            'order_date': date.strftime('%Y-%m-%d'),
            'order_time': order_time.strftime('%H:%M:%S'),
            'payment_method': payment_method,
            'shipping_city': shipping_city
        }
        
        orders.append(order)
    
    return orders

def save_to_csv(orders, filename):
    """Save orders to CSV file"""
    fieldnames = [
        'order_id', 'customer_name', 'customer_email', 'product', 'category',
        'quantity', 'price', 'order_date', 'order_time', 'payment_method', 'shipping_city'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)
    
    print(f"✅ Generated {len(orders)} orders in {filename}")
    
    # Print statistics
    total_revenue = sum(order['quantity'] * order['price'] for order in orders)
    print(f"📊 Total Revenue: ₹{total_revenue:,.2f}")
    print(f"📦 Total Orders: {len(orders)}")
    print(f"💰 Average Order Value: ₹{total_revenue/len(orders):,.2f}")

if __name__ == "__main__":
    # Generate orders for today
    today = datetime.now().date()
    orders = generate_orders(num_orders=500, date=today)
    filename = f"orders_{today.strftime('%Y%m%d')}.csv"
    save_to_csv(orders, filename)
    
    # Generate orders for yesterday (for testing report)
    yesterday = today - timedelta(days=1)
    orders_yesterday = generate_orders(num_orders=300, date=yesterday)
    filename_yesterday = f"orders_{yesterday.strftime('%Y%m%d')}.csv"
    save_to_csv(orders_yesterday, filename_yesterday)
    
    print("\n🎉 Sample datasets generated successfully!")
    print(f"📁 Files created: {filename}, {filename_yesterday}")
    print("\n📤 Upload these files to S3 bucket in 'incoming/' folder to test the pipeline")
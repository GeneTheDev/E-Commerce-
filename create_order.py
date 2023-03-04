from sqlalchemy.orm import sessionmaker
from models import Order, OrderProduct
from sqlalchemy import create_engine

# Replace <username>, <password>, <hostname>, <port>, and <database> with your own values
url = 'postgresql+psycopg2://gene:Gene21gene@127.0.0.1:5432/webstore_db'

engine = create_engine(url)


Session = sessionmaker(bind=engine)
session = Session()

try:
    # Start a transaction
    with session.begin():

        # Create an order
        order = Order(customer_email='owens.eugene@yahoo.com',
                      total_cost=10.0, order_date='2023-02-21')
        session.add(order)

        # Create an order product for the order
        order_product = OrderProduct(
            order=order, product_id=1, quantity=1, price=10.0)
        session.add(order_product)

    # Commit the transaction
    session.commit()

except Exception as e:
    # Roll back the transaction if an error occurred
    session.rollback()
    print('Error:', str(e))
finally:
    # Close the session
    session.close()

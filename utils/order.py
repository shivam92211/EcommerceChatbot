from utils.config import orders_collection

def get_order_status(order_id: str):
    """Fetch order status by order_id."""
    order = orders_collection.find_one({"_id": order_id})
    if not order:
        return {"error": "Order not found"}
    return {"order_id": order_id, "status": order.get("orderStatus")}

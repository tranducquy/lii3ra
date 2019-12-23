from lii3ra.orderstatus import OrderStatus


class Order:
    def __init__(self):
        self.create_time = None
        self.order_time = None
        self.exit_order_time = None
        self.order_type = None
        self.order_status = OrderStatus.BEFORE_ORDER
        self.price = None
        self.vol = None
        self.oco_order1 = None
        self.oco_order2 = None

    def set_order(self, create_time, order_type, price, vol):
        self.create_time = create_time
        self.order_time = None
        self.exit_order_time = None
        self.order_type = order_type
        self.order_status = OrderStatus.BEFORE_ORDER
        self.price = price
        self.vol = vol
        self.oco_order1 = None
        self.oco_order2 = None

    def order(self, order_time):
        self.order_time = order_time
        self.order_status = OrderStatus.ORDERING
        if self.oco_order1 is not None:
            self.oco_order1.order_time = order_time
            self.oco_order1.order_status = OrderStatus.ORDERING
        if self.oco_order2 is not None:
            self.oco_order2.order_time = order_time
            self.oco_order2.order_status = OrderStatus.ORDERING

    def execution_order(self, exit_order_time):
        self.exit_order_time = exit_order_time
        self.order_status = OrderStatus.EXECUTION
        if self.oco_order1 is not None:
            self.oco_order1.order_status = OrderStatus.EXECUTION
        if self.oco_order2 is not None:
            self.oco_order2.order_status = OrderStatus.EXECUTION

    def fail_order(self):
        self.exit_order_time = None
        self.order_status = OrderStatus.FAIL
        if self.oco_order1 is not None:
            self.oco_order1.order_status = OrderStatus.FAIL
        if self.oco_order2 is not None:
            self.oco_order2.order_status = OrderStatus.FAIL

    def set_oco_order(self, create_time, order_type, oco_order1, oco_order2):
        self.create_time = create_time
        self.order_type = order_type
        self.order_status = OrderStatus.BEFORE_ORDER
        self.oco_order1 = oco_order1  # 1から先に約定判定するため、損切り系を1にするのが望ましい
        self.oco_order2 = oco_order2
        self.order_time = None
        self.exit_order_time = None
        self.price = None
        self.vol = None

# You will use this code on your own risk
# I EXPRESSLY DISCLAIMS ALL REPRESENTATIONS AND WARRANTIES, EXPRESS OR IMPLIED, WITH RESPECT TO THE CODE,
# INCLUDING THE WARRANTIES OF MERCHANTABILITY AND OF FITNESS FOR A PARTICULAR PURPOSE.
# UNDER NO CIRCUMSTANCES INCLUDING NEGLIGENCE SHALL I BE LIABLE FOR ANY DAMAGES, INCIDENTAL, SPECIAL,
# CONSEQUENTIAL OR OTHERWISE (INCLUDING WITHOUT LIMITATION DAMAGES FOR LOSS OF PROFITS, BUSINESS INTERRUPTION,
# LOSS OF INFORMATION OR OTHER PECUNIARY LOSS) THAT MAY RESULT FROM THE USE OF OR INABILITY TO USE THE CODE,
# EVEN IF I HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.


import datetime, clr, sys, os

sys.path.append(os.path.dirname(__file__))
clr.AddReference('SterlingWrapper')
from SterlingWrapper import Connector


class PositionParsingException(Exception):
    pass


class StiPosition:
    __slots__ = ['symbol', 'size', 'price', 'closed_pnl', 'opg_size', 'n_slong', 'n_sshort']

    def __init__(self, symbol, size, price, closed_pnl, opg_size, n_slong, n_sshort):
        self.symbol = symbol
        self.size = int(size)
        self.price = float(price)
        self.closed_pnl = float(closed_pnl)
        self.opg_size = int(opg_size)
        self.n_slong = float(n_slong)
        self.n_sshort = float(n_sshort)

    @staticmethod
    def parse_from_sterling(pos_wrapper):
        pos_sti = pos_wrapper.split(' ')

        if len(pos_sti) <= 2:
            raise PositionParsingException(f'Wrong position format from wrapper: {pos_sti}')
        pos_sti = [x.replace(',', '').replace('\n', '') for x in pos_sti]

        return StiPosition(*pos_sti)

    def __str__(self):
        return f'|{self.symbol} pos: {self.size} open price: {self.price} opg size: {self.opg_size} ' \
               f'closed pnl: {self.closed_pnl} slong/short: {self.n_slong}/{self.n_sshort}|'

    def __repr__(self):
        return str(self)


class ConnectorSterling:
    __slots__ = ['conn', '_verbose']

    def __init__(self, verbose=True):
        self.conn = Connector()
        self._verbose = verbose

    def send_market(self, account, symbol, size, route, side, tif='D') -> tuple:
        """Place market order. Return orderID and status (check Sterling API docs)"""
        id_ = self.conn.Sendmarket(account, symbol, size, size, route, side, tif)
        id_, status = id_.split(';')
        return id_, status

    def send_limit(self, account, symbol, size, price, route, side, tif='D', disp=0) -> tuple:
        """Place limit order. Return orderID and status (check Sterling API docs)"""
        disp = size if disp > size else disp
        res = self.conn.Sendlimit(account, symbol, size, disp, route, price, side, tif)
        id_, status = res.split(';')
        return id_, int(status)

    def send_stop_limit(self, account, symbol, size, stop_price, limit_price, route, side, tif='D', disp=0) -> tuple:
        """Place stop limit order. Return orderID and status (check Sterling API docs)"""
        disp = size if disp > size else disp
        res = self.conn.Sendstoplimit(account, symbol, size, disp, route, stop_price, limit_price, side, tif)
        id_, status = res.split(';')
        return id_, int(status)

    def replace_limit_order(self, ordId, qty, price) -> tuple:
        """"Replace open limit order by given ID. You can change quantity and price of order but not destiantion
        Returns new orderID and replace status(see sterling API docs for status codes)
        """
        res = self.conn.ReplaceOrder(ordId, qty, price)
        new_id, status = res.split(';')
        return new_id, int(status)

    def get_open_shares(self, account: str, symbol: str) -> int:
        """"Return current open position in shares for given symbol and account"""
        pos = self.conn.Position(account, symbol)
        return 0 if not pos else int(pos)

    def get_all_account_positions(self, account: str) -> list:
        """Return list of all open and closed positions for given account"""
        positions = []
        positions_sti = self.conn.AllPositions(account).split(';')
        for pos_sti in positions_sti:
            try:
                positions.append(StiPosition.parse_from_sterling(pos_sti))
            except PositionParsingException:
                continue
        return positions

    def cancel_all_symbol_orders(self, account: str, symbol: str):
        """Send request to cancel all open orders for given account and stick symbol. It doesn't return anything.
        You probably have to check every order status to make sure there are no more open orders..."""
        if not symbol:
            raise Exception('cancel_all_symbol_orders symbol is empty')
        self.conn.CancellAllSymbol(symbol, account)
        if not self._verbose:
            print(f"Python: Candle all orders for {symbol}")

    def cancel_order_id(self, account: str, ordID: str):
        """"Send cancel request for open order by given order ID. After request you will get newID instead of old
        newID = oldID+'cancel'. If you want to make sure order was canceled: request status for newID. For oldID status
        will be same as before
        """
        if not self._verbose:
            print(f'Canceling order {ordID} for {account}')
        self.conn.CancelOrder(account, ordID)

    def cancel_all(self, account: str):
        """Cancel all open orders for given account. It doesn't return anything.
        You probably have to check every order status to make sure there are no more open orders..."""

        self.conn.CancellAll(account)
        if not self._verbose:
            print(f'Python: {account} All orders cancel request sent')

    def order_status(self, ordID):
        """Get order status (see sterling API docs for status description)"""
        return self.conn.OrderStatus(ordID)

    def orders_count(self):
        """Get total number of open orders"""
        return self.conn.GetOrders()

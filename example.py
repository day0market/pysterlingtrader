# You will use this code on your own risk
# I EXPRESSLY DISCLAIMS ALL REPRESENTATIONS AND WARRANTIES, EXPRESS OR IMPLIED, WITH RESPECT TO THE CODE,
# INCLUDING THE WARRANTIES OF MERCHANTABILITY AND OF FITNESS FOR A PARTICULAR PURPOSE.
# UNDER NO CIRCUMSTANCES INCLUDING NEGLIGENCE SHALL I BE LIABLE FOR ANY DAMAGES, INCIDENTAL, SPECIAL,
# CONSEQUENTIAL OR OTHERWISE (INCLUDING WITHOUT LIMITATION DAMAGES FOR LOSS OF PROFITS, BUSINESS INTERRUPTION,
# LOSS OF INFORMATION OR OTHER PECUNIARY LOSS) THAT MAY RESULT FROM THE USE OF OR INABILITY TO USE THE CODE,
# EVEN IF I HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

from connector import ConnectorSterling
import time

# IMPORTANT!!!!
# If you run this code it will place limit order on Sterling account you specified below
# Depending on price and symbol it can be filled immediately.
# You're bearing ALL RISKS and LOSSES! I strongly recommend you to do this only on DEMO account

if __name__ == '__main__':
    account = ""
    symbol = 'SPY'
    price = 262
    con = ConnectorSterling(verbose=False)

    ordId, status = con.send_limit(account, symbol, 100, price, "ARCA", "B")

    if status == 0:
        print(f'Cancel order {ordId}')
        time.sleep(1)
        con.cancel_order_id(account, ordId)
        time.sleep(1)
        status = con.order_status(ordId + 'cancel')
        print(f'Now order in status {status}')
    else:
        print(f"Order status: {status}")

    positions = con.get_all_account_positions(account)

    print('\n'.join([str(x) for x in positions]))

    for p in positions:
        symb_position = con.get_open_shares(account, p.symbol)
        print(f'{p.symbol} open shares is {symb_position}')

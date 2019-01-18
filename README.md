This a simple python binding to Sterling Trader API.
You can place, cancel and track status of your orders. 

Your python version should be >= 3.6

Clone this repo and install all requirements.

*********You will use this code on your own risk!*********

I EXPRESSLY DISCLAIMS ALL REPRESENTATIONS AND WARRANTIES, EXPRESS OR IMPLIED, WITH RESPECT TO THE CODE,
INCLUDING THE WARRANTIES OF MERCHANTABILITY AND OF FITNESS FOR A PARTICULAR PURPOSE.
UNDER NO CIRCUMSTANCES INCLUDING NEGLIGENCE SHALL I BE LIABLE FOR ANY DAMAGES, INCIDENTAL, SPECIAL,
CONSEQUENTIAL OR OTHERWISE (INCLUDING WITHOUT LIMITATION DAMAGES FOR LOSS OF PROFITS, BUSINESS INTERRUPTION,
LOSS OF INFORMATION OR OTHER PECUNIARY LOSS) THAT MAY RESULT FROM THE USE OF OR INABILITY TO USE THE CODE,
EVEN IF I HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

Unfortunately connector doesn't support ActiveX events. So if you plan to use it for trading
you should have endless loop and check positions and orders every second, minute...

pysterling requires SterlingWrapper.dll. It's wrapper around Sterling AcitveX API and you can build it from [sourse] (https://github.com/day0market/SterlingWrapper) 
or use SterlingWrapper.dll from this repo.

You can find example usage in example.py file. Please note if you run example.py it will place limit order that can be 
filled immediately. You should run it only on DEMO Sterling Trader Pro account. Otherwise you will bear all risk and losses.








 

import requests
import locale

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction



class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    # https://query1.finance.yahoo.com/v8/finance/chart/${symbol}.JK?range=1d

    def on_event(self, event, extension):
        items = []

        if event.get_keyword() == "istock":
            symbol      = event.get_argument()
            url         = "https://query1.finance.yahoo.com/v8/finance/chart/" + symbol + ".JK?range=1d"
            response    = requests.request("GET", url)
            data        = response.json()

            if data["chart"]["result"] is not None:
                meta = data["chart"]["result"][0]["meta"]
                symbol = meta["symbol"]
                price = int(meta["regularMarketPrice"])
                idr = idr_format(price)
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name='%s = IDR %s' %(symbol, idr),
                                                 description='The result is a aproximated',
                                                 on_enter=HideWindowAction()))

       
        return RenderResultListAction(items)

def idr_format(value, with_prefix=False, decimal=0):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format("%.*f", (decimal, value), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah

if __name__ == '__main__':
    DemoExtension().run()

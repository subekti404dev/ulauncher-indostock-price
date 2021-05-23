import requests
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
                symbol = meta["symbol"].replace(".JK", "")
                price = int(meta["regularMarketPrice"])
                idr = "{:,}".format(price).replace(",", ".")
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name='IDR %s' % idr,
                                                 description='Price of %s' % symbol,
                                                 on_enter=HideWindowAction()))

       
        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()

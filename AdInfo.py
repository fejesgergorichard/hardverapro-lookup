class AdInfo:
    def __init__(self, id, title, seller, url, price):
        self.id = id
        self.title = title
        self.seller = seller
        self.url = url
        self.price = price


def ad_info_factory(ad) -> AdInfo:
    ad_id = ad['data-uadid']
    ad_title = ad.find('h1').find('a').text.strip()
    ad_seller = ad.find('div', class_='uad-misc').find('div', class_='uad-light').text.strip()
    ad_url = ad.find('a', class_='uad-image')['href']
    ad_price = ad.find('div', class_='uad-info').find('div', class_='uad-price').text.strip()
    ad_info = AdInfo(ad_id, ad_title, ad_seller, ad_url, ad_price)

    return ad_info

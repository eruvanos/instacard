from urllib.parse import urlencode

import arrow
import lob
from flask import render_template

from instacard.model import Userinfo, Address, Postinfo


def init(api_key):
    lob.api_key = api_key


def _location_pic(location):
    if location:
        lat, lng = location['lat'], location['lng']
        query = urlencode(dict(
            center=f"{lat},{lng}",
            markers=f"color:red|{lat},{lng}",
            zoom=7,
            size="500x500"
        ))
        return f"https://maps.googleapis.com/maps/api/staticmap?{query}"
    else:
        return 'https://instagram-brand.com/wp-content/uploads/2016/11/app-icon2.png'


def send_postcard(user: Userinfo, post: Postinfo, address: Address):
    utc = arrow.get(post.taken_at)
    local = utc.to('Europe/Berlin')
    time_str = local.format(fmt='dddd, DD.MM.YYYY', locale='de_de')

    front = render_template('postcard/front.html',
                            image1=post.image,
                            image2=_location_pic(post.location),
                            image3=user.image,
                            )

    back = render_template('postcard/back.html',
                           name=user.fullname,
                           code=post.code,
                           timestamp=time_str,
                           )

    lob.Postcard.create(
        to_address={
            'name': address.name,
            'address_line1': address.streetno,
            'address_city': address.city,
            'address_state': address.state,
            'address_zip': address.zip,
            'address_country': address.country
        },
        front=front,
        back=back,
        merge_variables=dict()
    )

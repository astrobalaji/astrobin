from django.utils.translation import ugettext as _

import subscription.signals

from .utils import (
    rawdata_user_used_bytes,
    rawdata_subscription_byte_limit,
)

def impossible_downgrade(sender, subscription, **kwargs):
    before = sender.subscription
    after = subscription

    used = rawdata_user_used_bytes(sender.user)
    limit = rawdata_subscription_byte_limit(subscription)

    if used > limit:
        return _("You cannot downgrade to this plan because your files would not fit in the allocated space. Please delete some files first.")

    return None


__installed = False
def install():
    global __installed
    if not __installed:
        subscription.signals.change_check.connect(impossible_downgrade)
        __installed = True

# Python
from datetime import date, timedelta

# Django
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.views.generic.edit import FormView

# Third party
from subscription.models import Transaction, Subscription, UserSubscription

# AstroBin
from astrobin_apps_donations import utils as donation_utils

# This app
from forms import MigrateDonationsForm
import utils as premium_utils


class MigrateDonationsView(FormView):
    template_name = "astrobin_apps_premium/migrate_donations.html"
    form_class = MigrateDonationsForm
    premium_sub = Subscription.objects.get(name = "AstroBin Premium")

    def get_success_url(self):
        return reverse("astrobin_apps_premium.migrate_donations_success")

    def get_migration_data(self):
        amount = 0
        first_payment = None
        days_paid = 0
        expiration = None
        migration_impossible = False
        migration_impossible_reason = None

        try:
            us = UserSubscription.objects.get(
                user = self.request.user,
                subscription__name__in = premium_utils.SUBSCRIPTION_NAMES)
        except UserSubscription.DoesNotExist:
            us = None

        transactions = Transaction.objects.filter(
            user = self.request.user,
            subscription__name__in = donation_utils.SUBSCRIPTION_NAMES,
            event = "subscription payment",
            timestamp__year = date.today().year - 1).order_by('-timestamp')

        for t in transactions:
            first_payment = t.timestamp
            amount += t.amount

        if amount > 0:
            days_paid = int(float(amount)/float(self.premium_sub.price) * 365.25)
            expiration = (first_payment + timedelta(days_paid)).date()

        if us is not None:
            migration_impossible = True
            migration_impossible_reason = "ALREADY_PREMIUM"
        elif transactions.count() == 0:
            migration_impossible = True
            migration_impossible_reason = "NO_PAYMENTS"
        elif expiration < date.today():
            migration_impossible = True
            migration_impossible_reason = "PAST_EXPIRATION"

        return {
            "migration_impossible": migration_impossible,
            "migration_impossible_reason": migration_impossible_reason,
            "transactions": transactions,
            "amount_donated": amount,
            "first_payment": first_payment,
            "price": self.premium_sub.price,
            "days_paid": days_paid,
            "expiration": expiration,
        }
 
    def get_context_data(self, **kwargs):
        context = super(MigrateDonationsView, self).get_context_data(**kwargs)
        context["migration_data"] = self.get_migration_data()
        return context

    def form_valid(self, form):
        migration_data = self.get_migration_data()
        if migration_data["migration_impossible"]:
            return HttpResponseForbidden()

        us, created = UserSubscription.objects.get_or_create(
            user = self.request.user,
            subscription = self.premium_sub,
            expires = migration_data["expiration"],
            cancelled = False)
        us.fix()

        return super(MigrateDonationsView, self).form_valid(form)

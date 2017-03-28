from coreExtend.models import Account
from replica import settings as r_settings
from .models import Topic, Entry

class PulseViewMixin(object):
    date_field = 'pub_date'
    paginate_by = r_settings.PAGINATE
    month_format = "%m"

    def get_allow_future(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            return Entry.objects.posts()
        else:
            return Entry.objects.published()

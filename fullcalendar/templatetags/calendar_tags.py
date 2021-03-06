from django import template
from fullcalendar.models import PublicEvent, GameAppointmentEvent, AvailableEvent
from django.utils import timezone
import pytz
register = template.Library()


@register.simple_tag(takes_context=True)
def public_events(context):
    request = context['request']
    user = request.user
    if user.is_authenticated and user.is_league_admin():
        my_games = list(GameAppointmentEvent.get_future_games(user))
        public_events = list(PublicEvent.objects.order_by('-start').all()[:5])
        cal_events = my_games + public_events
        cal_events = sorted(cal_events, key=lambda k: k.start, reverse=True)[:5]
        return cal_events
    else:
        public_events = PublicEvent.objects.all().order_by('-start')[:5]
        return public_events


@register.simple_tag()
def get_now():
    return timezone.now()


@register.simple_tag()
def tz_offset():
    tz = timezone.get_current_timezone()
    return timezone.localtime(timezone.now(), tz).utcoffset().total_seconds()

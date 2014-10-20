"""Handles converting seconds remaining into time stamps or other formats."""

from math import ceil


def eta_hms(seconds, always_show_hours=False, always_show_minutes=False, hours_leading_zero=False):
    """Converts seconds remaining into a human readable timestamp (e.g. hh:mm:ss, h:mm:ss, mm:ss, or ss).

    Positional arguments:
    seconds -- integer/float indicating seconds remaining.

    Keyword arguments:
    always_show_hours -- don't hide the 0 hours.
    always_show_minutes -- don't hide the 0 minutes.
    hours_leading_zero -- show 01:00:00 instead of 1:00:00.

    Returns:
    Human readable string.
    """
    # Convert seconds to other units.
    final_hours, final_minutes, final_seconds = 0, 0, seconds
    if final_seconds >= 3600:
        final_hours = int(final_seconds / 3600.0)
        final_seconds -= final_hours * 3600
    if final_seconds >= 60:
        final_minutes = int(final_seconds / 60.0)
        final_seconds -= final_minutes * 60
    final_seconds = int(ceil(final_seconds))

    # Determine which string template to use.
    if final_hours or always_show_hours:
        if hours_leading_zero:
            template = '{hour:02.0f}:{minute:02.0f}:{second:02.0f}'
        else:
            template = '{hour}:{minute:02.0f}:{second:02.0f}'
    elif final_minutes or always_show_minutes:
        template = '{minute:02.0f}:{second:02.0f}'
    else:
        template = '{second:02.0f}'

    return template.format(hour=final_hours, minute=final_minutes, second=final_seconds)


def eta_letters(seconds, shortest=False, leading_zero=False):
    """Converts seconds remaining into human readable strings (e.g. '1s' or '5h 22m 2s').

    Positional arguments:
    seconds -- integer/float indicating seconds remaining.

    Keyword arguments:
    shortest -- show the shortest possible string length by only showing the biggest unit.
    leading_zero -- always show a leading zero for the minutes and seconds.

    Returns:
    Human readable string.
    """
    if not seconds:
        return '00s' if leading_zero else '0s'

    # Split up seconds into other units.
    values = dict(week=0, day=0, hour=0, minute=0, second=0)
    if seconds >= 604800:
        values['week'] = int(seconds / 604800.0)
        seconds -= values['week'] * 604800
    if seconds >= 86400:
        values['day'] = int(seconds / 86400.0)
        seconds -= values['day'] * 86400
    if seconds >= 3600:
        values['hour'] = int(seconds / 3600.0)
        seconds -= values['hour'] * 3600
    if seconds >= 60:
        values['minute'] = int(seconds / 60.0)
        seconds -= values['minute'] * 60
    values['second'] = int(ceil(seconds))

    # Map to characters.
    leading = lambda x: ('{0:02.0f}' if leading_zero else '{0}').format(x)
    mapped = (
        ('w', str(values['week'] or '')),
        ('d', str(values['day'] or '')),
        ('h', str(values['hour'] or '')),
        ('m', leading(values['minute']) if values['minute'] else ''),
        ('s', leading(values['second']) if values['second'] else ''),
    )
    trimmed = [(k, v) for k, v in mapped if v]
    formatted = ['{0}{1}'.format(v, k) for k, v in trimmed]

    return formatted[0] if shortest else ' '.join(formatted)

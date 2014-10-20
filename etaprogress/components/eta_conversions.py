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

    # Convert seconds to other units.
    final_weeks, final_days, final_hours, final_minutes, final_seconds = 0, 0, 0, 0, seconds
    if final_seconds >= 604800:
        final_weeks = int(final_seconds / 604800.0)
        final_seconds -= final_weeks * 604800
    if final_seconds >= 86400:
        final_days = int(final_seconds / 86400.0)
        final_seconds -= final_days * 86400
    if final_seconds >= 3600:
        final_hours = int(final_seconds / 3600.0)
        final_seconds -= final_hours * 3600
    if final_seconds >= 60:
        final_minutes = int(final_seconds / 60.0)
        final_seconds -= final_minutes * 60
    final_seconds = int(ceil(final_seconds))

    # Handle shortest:
    if shortest:
        if final_weeks:
            formatted = str(final_weeks) + 'w'
        elif final_days:
            formatted = str(final_days) + 'd'
        elif final_hours:
            formatted = str(final_hours) + 'h'
        elif final_minutes:
            formatted = '{0:0{1}d}m'.format(final_minutes, 2 if leading_zero else 1)
        else:
            formatted = '{0:0{1}d}s'.format(final_seconds, 2 if leading_zero else 1)
        return formatted

    # Determine which string template to use.
    if final_weeks:
        template = '{0:d}w {1:d}d {2:d}h {3:02d}m {4:02d}s' if leading_zero else '{0}w {1}d {2}h {3}m {4}s'
    elif final_days:
        template = '{1:d}d {2:d}h {3:02d}m {4:02d}s' if leading_zero else '{1}d {2}h {3}m {4}s'
    elif final_hours:
        template = '{2:d}h {3:02d}m {4:02d}s' if leading_zero else '{2}h {3}m {4}s'
    elif final_minutes:
        template = '{3:02d}m {4:02d}s' if leading_zero else '{3}m {4}s'
    else:
        template = '{4:02d}s' if leading_zero else '{4}s'

    return template.format(final_weeks, final_days, final_hours, final_minutes, final_seconds)

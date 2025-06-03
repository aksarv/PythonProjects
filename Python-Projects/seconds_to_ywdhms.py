"""
Made this for showing the time taken to run scripts in a more readable format
"""

def seconds_to_ywdhms(s):
    years = s // 31536000
    weeks = (s % 31536000) // 604800
    days = (s % 604800) // 86400
    hours = (s % 86400) // 3600
    minutes = (s % 3600) // 60
    seconds = s % 60
    milliseconds = round((s % 1) * 1000, 3) if isinstance(s, float) else 0
    final = []
    if years == 1:
        final.append('1 year')
    elif years != 0:
        final.append(f'{int(years)} years')
    if weeks == 1:
        final.append('1 week')
    elif weeks != 0:
        final.append(f'{int(weeks)} weeks')
    if days == 1:
        final.append('1 day')
    elif days != 0:
        final.append(f'{int(days)} days')
    if hours == 1:
        final.append('1 hour')
    elif hours != 0:
        final.append(f'{int(hours)} hours')
    if minutes == 1:
        final.append('1 minute')
    elif minutes != 0:
        final.append(f'{int(minutes)} minutes')
    if seconds == 1:
        final.append('1 second')
    elif seconds > 1:
        final.append(f'{int(seconds)} seconds')
    final.append(f'{milliseconds} ms')
    if len(final) == 1:
        return final[0]
    return ', '.join(final)

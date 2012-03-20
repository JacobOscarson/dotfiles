import sys
import datetime

times = open(sys.argv[1])

def dot_times(dotted):
    try:
        hrs, mins = dotted.split('.')
        return int(hrs), int(mins)
    except Exception, e:
        print(e)
        sys.exit(1)

def units(tim):
    if tim.endswith('min'):
        return int(tim[0:1])
    elif tim.endswith('h'):
        return 60 * int(tim[0:1])
    else:
        return 0

def minutes(timing):
    mins = 0
    for tim in timing.strip().split(' '):
        if tim.endswith('min'):
            mins += int(tim.replace('min', ''))
        elif tim.endswith('h'):
            mins += int(tim.replace('h', '')) * 60

    return mins

def parse_line(line):
    desc, timing = line.split(':')
    desc = desc.split(',')
    if len(desc) == 1:
        project = desc[0]
        label = 'unknown'
    elif len(desc) == 2:
        project, label = desc
    else:
        project, label = 'unknown'
        pass
    return project, label.strip(), minutes(timing)

days = {}

isoday = False
for line in (l.strip() for l in times.readlines()):
    if line.startswith('20'):
        isoday = line
        days[isoday] = {'day': isoday, 'pause': 0}
        year, month, day = [int(part) for part in isoday.split('-')]
    elif line.startswith('Kom') and 'gick' in line:
        line = line.strip()
        line = line.replace(',', '')
        segs = line.split(' ')
        if len(segs) >= 4:
            arrive = datetime.datetime(year, month, day, *dot_times(segs[1]) )
            went = datetime.datetime(year, month, day, *dot_times(segs[3]))
            worktime = went - arrive
            hrs, secs = divmod(worktime.seconds, 60*60)
            mins, secs = divmod(secs, 60)
            days[isoday]['time'] = (hrs, mins)
    elif line:
        try:
            print ', '.join(str(part) for part in (parse_line(line)+(isoday,)))
        except Exception, e:
            pass

    if line.startswith('Paus') or line.startswith('Lunch'):
        _, _, pause = parse_line(line)
        if isoday:
            days[isoday]['pause'] += pause

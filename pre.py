"""
Test program for pre-processing schedule
"""
import arrow

base = arrow.now()

def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.
    """
    field = None
    entry = { }
    cooked = [ ]
    for line in raw:
        line = line.rstrip()
        if len(line) == 0:
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line + " "
            continue
        if len(parts) == 2:
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) +
                "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:
                global base
                base = arrow.Arrow.strptime(content, "  %m/%d/%Y", tzinfo=None)

            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = { }
            entry['topic'] = ""
            entry['project'] = ""
            entry['week'] = content

            week_num = int(content)
            num_days = week_num*7
            new_week = base.replace(days=+num_days)

            entry['date'] = arrow.Arrow.isoformat(new_week)

        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    if entry:
        cooked.append(entry)

    return cooked


def main():
    f = open("static/schedule.txt")
    print("in main before parsed base is: ")
    print(base)
    parsed = process(f)
    print("in main after parsed base is: ")
    print(base)

    print(parsed)

if __name__ == "__main__":
    main()

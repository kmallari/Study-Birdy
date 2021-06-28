import csv
import os

def get_line_at_pos(fin, pos):
    fin.seek(pos)
    skip = fin.readline()
    npos = fin.tell()
    assert pos + len(skip) == npos
    line = fin.readline()
    return npos, line

def bisect_seek(fname, field_func, field_val):
    size = os.path.getsize(fname)
    minpos, maxpos, cur = 0, size, int(size / 2)

    with open(fname) as fin:
        prev_pos = -1
        while True:  # find first id smaller than the one we search
            realpos, line = get_line_at_pos(fin, cur)
            val = field_func(line)
            if val >= field_val:
                state = ">"
                maxpos = cur
                cur = int((minpos + cur) / 2)
            else:
                state = "<"
                minpos = cur
                cur = int((cur + maxpos) / 2)
            if prev_pos == cur:
                break
            prev_pos = cur
    return realpos


def getser(line):
    return line.split(",")[0]


def find_subject(filename, class_code, section):
    found = False
    # find position from which we should start searching
    pos = bisect_seek(filename, getser, class_code)
    with open(filename, 'r', encoding='utf_8_sig') as csvfile:
        csvfile.seek(pos)
        reader = csv.reader(csvfile, delimiter=',')
        try:
            for row in reader:
                if row[0] == class_code and row[1] == section:
                    found = True
                    break
                elif row[0] > class_code:
                    # as file is sorted we know we can abort now
                    break
        except Exception as e:
            print(e)
    if found:
        return row
    else:
        return False
import ffmpeg
from sys import argv
import os

""" split_wav `audio file` `time listing`

    `audio file` is any file known by local FFmpeg
    `time listing` is a file containing multiple lines of format:
        `start time` `end time` output name 

    times can be either MM:SS or S*
"""

_in_file = argv[1]

def make_time(elem):
    # allow user to enter times on CLI
    t = elem.split(':')
    try:
        # will fail if no ':' in time, otherwise add together for total seconds
        return int(t[0]) * 60 + float(t[1])
    except:
        # assuming everything is in :, this must be the last clip.
        # just fill in time.
        return 10000

def collect_from_file():
    """user can save times in a file, with start and end time on a line"""

    time_pairs = []
    fn = argv[2]
    f = open(fn,'r')
    if len(f.readline().split(sep=':')) < 3:
        # need to fix timestamps to have end time for each track.
        fn = fill_timestamps(fn)
    f.close()
    with open(fn) as in_times:
        for l, line in enumerate(in_times):
            tp = line.split()
            tp[0] = make_time(tp[0])
            tp[1] = make_time(tp[1]) - tp[0]
            time_pairs.append(tp)
    return time_pairs

def fill_timestamps(fn):
    """
    make new file with timestamps of start and end for each track,
    instead of just start.
    """
    f = open(fn,'r+')
    write_fn = '.'.join(fn.split(sep='.')[:-1]) + '_corrected.txt'
    w = open(write_fn,'w')
    prev_line = f.readline().split()
    for cur_line in f.readlines():
        print(f'curline: {cur_line}')
        split_line = cur_line.split()
        prev_line = ' '.join([prev_line[0], split_line[0], *prev_line[1:]])
        w.write(prev_line+'\n')
        prev_line = split_line
    w.write(cur_line+'\n')
    f.close()
    w.close()
    return write_fn

def main():
    file_split = _in_file.split(sep='.')
    postfix = file_split[-1]
    album_name = '.'.join(file_split[:-1])+' album'
    if not os.path.isdir(album_name):
        os.mkdir(album_name)
    for i, tp in enumerate(collect_from_file()):
        # open a file, from `ss`, for duration `t`
        
        stream = ffmpeg.input(_in_file, ss=tp[0], t=tp[1])
        # output to named file
        title = ' '.join(tp[2:]) + '.' + postfix
        pref = str(i+1) + '. '
        stream = ffmpeg.output(stream, 
                                os.path.join(album_name, pref + title), 
                                **{ 'metadata':'title='+title, 
                                'metadata:':'track='+str(i+1)})
        # this was to make trial and error easier
        stream = ffmpeg.overwrite_output(stream)

        # and actually run
        ffmpeg.run(stream)

if __name__ == '__main__':
    main()
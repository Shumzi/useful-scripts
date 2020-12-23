#shebang is what goes here
import subprocess
import sys

def main():
    """split a music track into specified sub-tracks by calling ffmpeg from the shell"""

    # check command line for original file and track list file
    if len(sys.argv) != 3:
        print('usage: split <original_track> <track_list>')
        exit(1)

    # record command line args
    original_track = sys.argv[1]
    fileExt = '.'+original_track.split('.')[-1]
    track_list = sys.argv[2]
    # create a template of the ffmpeg call in advance
    cmd_string = 'ffmpeg -i {tr} -ss {st} -to {en} {nm}'

    # read each line of the track list and split into start, end, name
    with open(track_list, encoding='utf-8') as f:
        for line in f:
            # skip comment and empty lines
            if line.startswith('#') or len(line) <= 1:
                continue
            # create command string for a given track
            splitted = line.strip().split()
            start, end = splitted[0:2]
            name = '"' + ' '.join(splitted[2:]) + fileExt + '"'
            command = cmd_string.format(tr=original_track, st=start, en=end, nm=name)
            print(command)
            # use subprocess to execute the command in the shell
            subprocess.call(command, shell=True)

    return None


if __name__ == '__main__':
    main()
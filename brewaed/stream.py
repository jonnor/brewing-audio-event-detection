

import argparse
import queue
import sys
import datetime

import matplotlib.pyplot as plt
import numpy
import sounddevice

#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("tensorflow").addHandler(logging.NullHandler(logging.ERROR))

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def detect_forever(audio_queue, window_length,
            overlap=0.1,
            on_threshold=0.6, off_threshold=0.4
            ):

    n_samples = window_length
    hop_length = n_samples * (1-overlap)

    new_samples = 0
    audio_buffer = numpy.zeros(shape=(n_samples,))

    #model = yamnet.Model()

    inside_event = False

    while True:
        data = audio_queue.get()
        data = numpy.squeeze(data)

        # move existing data over
        audio_buffer = numpy.roll(audio_buffer, len(data), axis=0)
        # add the new data
        audio_buffer[len(audio_buffer)-len(data):len(audio_buffer)] = data
        new_samples += len(data)
        # check if we have received enough new data to do new classification
        if new_samples >= hop_length:
            t = datetime.datetime.now()

            new_samples = 0
            waveform = audio_buffer

            #x = numpy.reshape(waveform, [1, -1])
            x = numpy.expand_dims(waveform, 0)
            #x = numpy.expand_dims(x, -1)

            # FIXME: run model

            probability = numpy.random.random()

            if not inside_event and probability >= on_threshold:
                inside_event = True
                print('EVENT on', t, probability)
            if inside_event and probability <= off_threshold:
                inside_event = False
                print('EVENT off', t, probability)



def parse():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
        help='input channels to use (default: the first)')
    parser.add_argument(
        '-r', '--samplerate', type=float, help='sampling rate of audio device')

    parser.add_argument(
        '--overlap', type=float, default=0.5,
        help='how much overlap between consequctive windows to classify')

    args = parser.parse_args()
    if any(c < 1 for c in args.channels):
        parser.error('argument CHANNEL: must be >= 1')

    return parser, args


def main():
    parser, args = parse()

    if args.list_devices:
        print(sounddevice.query_devices())
        parser.exit(0)

    if args.samplerate is None:
        device_info = sounddevice.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']


    mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)

        # Fancy indexing with mapping creates a (necessary!) copy:
        audio_queue.put(indata[:, mapping])
        #print(indata.shape)

    stream = sounddevice.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)

    print('stream open', args.device, stream)


    with stream:
        detect_forever(audio_queue, window_length=1024)

    print('stopped')

if __name__ == '__main__':
    main()

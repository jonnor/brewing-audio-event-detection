
import pandas

import os
import subprocess

def download_audio(identifier,
        out_dir,
        template="%(id)s.%(ext)s",
        format='opus',
        extra_args=[],
        quality=5):

    args = [
        'yt-dlp',
        '--extract-audio',
        '--audio-format', format,
        '--audio-quality', str(quality),
        '-o', os.path.join(out_dir, template),
        identifier,
    ]
    args += extra_args
    cmd = ' '.join(args)
    print(cmd)
    subprocess.check_output(args)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():

    files = pandas.read_csv('data/files.csv')
    
    print(files.head(5))
    #download_audio

    # limit to only the first minutes. To avoid the few very long videos to dominate
    args = ['--download-sections', "*00:00:00-00:02:00"]

    out_dir = 'data/audio'
    ensure_dir(out_dir)

    existing = [ f.replace('.opus', '') for f in os.listdir(out_dir) ]

    print(existing)

    missing = files[~files.id.isin(existing)]

    print(f'Downloading {len(missing)} files')

    for idx, file in missing.iterrows():  
        try:
            download_audio(file['id'], out_dir=out_dir, extra_args=args)
        except Exception as e:
            print(idx, e)

if __name__ == '__main__':
    main()

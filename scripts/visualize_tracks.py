import argparse
import json
import time
from typing import List

import cv2
import numpy as np
from PIL import Image
from sortedcontainers import SortedKeyList

from frater.core import Frame, BoundingBox
from frater.io import json_to_frater
from frater.visualization.bounding_box import draw_bounding_box


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('tracks', help='tracks to visualize')
    parser.add_argument('video', help='video to process')
    parser.add_argument('output_video')
    return parser.parse_args()


def visualize_bounding_boxes_for_frame(frame: Frame, bounding_boxes: List[BoundingBox]):
    for bounding_box in bounding_boxes:
        if bounding_box.area() > 0:
            frame = draw_bounding_box(bounding_box, frame)
    return frame


def get_tracks(filename) -> SortedKeyList:
    return SortedKeyList([json_to_frater(proposal) for proposal in json.load(open(filename))],
                         key=lambda x: x.start_frame)


class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()

    @property
    def interval(self):
        return self.end - self.start


def main():
    args = parse_args()
    tracks = get_tracks(args.tracks)
    video_reader = cv2.VideoCapture(args.video)
    dimensions = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_reader.get(cv2.CAP_PROP_FPS)
    total_frames = video_reader.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f'Video: {args.video}')
    print(f'Dimensions: {dimensions} - FPS: {fps}')
    print(f'Total Frames: {int(total_frames)}')

    video_writer = cv2.VideoWriter(args.output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, dimensions)
    current_frame_index = 1
    current_tracks = list()
    current_track_index = 0

    with Timer() as t:
        while video_reader.isOpened():
            ret, img = video_reader.read()
            if not ret:
                break

            current_tracks = [track for track in current_tracks if
                              current_frame_index in track.temporal_range]

            for i, track in enumerate(tracks[current_track_index:]):
                if current_frame_index in track.temporal_range:
                    current_tracks.append(track)
                else:
                    current_track_index += i
                    break

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(img)
            frame = Frame(image)

            current_bounding_boxes = [track.trajectory[current_frame_index] for track in current_tracks]
            current_frame_index += 1
            annotated_frame = visualize_bounding_boxes_for_frame(frame, current_bounding_boxes)
            converted_frame = np.array(annotated_frame.image)[:, :, ::-1].copy()
            if current_frame_index % 100 == 0:
                print(f'Writing frame {current_frame_index}')
            video_writer.write(converted_frame)

        video_writer.release()

    print(f'Video took {t.interval} seconds to process')


if __name__ == '__main__':
    main()

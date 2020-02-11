import argparse
import datetime
import json
import os
import random
import time
from typing import List

import cv2
from sortedcontainers import SortedKeyList

from diva.core import Frame, BoundingBox, ActivityProposal
from diva.visualization.bounding_box import draw_bounding_box
from frater.io import json_to_frater


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('proposals', help='Proposals to visualize')
    parser.add_argument('video', help='video to process')
    parser.add_argument('output_video')
    return parser.parse_args()


def visualize_proposals_for_frame(frame: Frame, bounding_boxes: List[BoundingBox]):
    for bounding_box in bounding_boxes:
        if bounding_box.area() > 0:
            frame = draw_bounding_box(bounding_box, frame)
    return frame


def get_proposals(filename) -> SortedKeyList:
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


extension_video_codec_map = {
    '.mp4': 'mp4v',
    '.avi': 'h264'
}


def get_video_codec(output_filename):
    _, ext = os.path.splitext(output_filename)
    if ext in extension_video_codec_map:
        return extension_video_codec_map[ext]
    else:
        return '    '


def get_random_color(brightness=0.8):
    red = int(255 * random.random() * brightness)
    green = int(255 * random.random() * brightness)
    blue = int(255 * random.random() * brightness)
    return red, green, blue


def visualize_proposals(proposals: List[ActivityProposal], source_filename: str, output_filename: str,
                        start_frame: int = 0):
    video_reader = cv2.VideoCapture(source_filename)
    dimensions = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_reader.get(cv2.CAP_PROP_FPS)
    total_frames = video_reader.get(cv2.CAP_PROP_FRAME_COUNT)
    codec = get_video_codec(output_filename)

    video_writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*codec), fps, dimensions)

    current_frame_index = start_frame

    print(f'Video: {output_filename}')
    print(f'Dimensions: {dimensions} - FPS: {fps}')
    print(f'Total Frames: int({total_frames})')

    print('separating bounding boxes')

    boxes_by_index = [[] for _ in range(int(total_frames))]
    for proposal in proposals:
        color = get_random_color()
        for box in proposal.trajectory.bounding_boxes:
            boxes_by_index[box.frame_index - 1].append((box, color))

    while video_reader.isOpened():
        ret, img = video_reader.read()
        if not ret:
            break

        current_bounding_boxes = boxes_by_index[current_frame_index]
        for box, color in current_bounding_boxes:
            cv2.rectangle(img, (int(box.x_0), int(box.y_0)), (int(box.x_1), int(box.y_1)), color, 2)

        if current_frame_index % 100 == 0:
            print(f'Writing frame {current_frame_index}')
            print(f'Total boxes: {len(current_bounding_boxes)}')

        video_writer.write(img)
        current_frame_index += 1

    video_writer.release()


def main():
    args = parse_args()
    proposals = get_proposals(args.proposals)
    with Timer() as t:
        visualize_proposals(proposals, args.video, args.output_video)

    print('Total time: ' + str(datetime.timedelta(seconds=int(t.interval))))


if __name__ == '__main__':
    main()

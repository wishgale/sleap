import os
import pytest

from sleap.instance import Instance, Point
from sleap.io.dataset import LabeledFrame, Labels

@pytest.fixture
def multi_skel_vid_labels(hdf5_vid, small_robot_mp4_vid, skeleton, stickman):
    """
    Build a big list of LabeledFrame objects and wrap it in Labels class.

    Args:
        hdf5_vid: An HDF5 video fixture
        small_robot_mp4_vid: An MP4 video fixture
        skeleton: A fly skeleton.
        stickman: A stickman skeleton

    Returns:
        The Labels object containing all the labeled frames
    """
    labels = []
    for f in range(500):
        vid = [hdf5_vid, small_robot_mp4_vid][f % 2]
        label = LabeledFrame(video=vid, frame_idx=f % vid.frames)

        fly_instances = []
        for i in range(6):
            fly_instances.append(Instance(skeleton=skeleton))
            for node in skeleton.node_names:
                fly_instances[i][node] = Point(x=i % vid.width, y=i % vid.height)

        stickman_instances = []
        for i in range(6):
            stickman_instances.append(Instance(skeleton=stickman))
            for node in stickman.node_names:
                stickman_instances[i][node] = Point(x=i % vid.width, y=i % vid.height)

        label.instances = stickman_instances + fly_instances
        labels.append(label)

    labels = Labels(labels)

    return labels
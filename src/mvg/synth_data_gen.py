import matplotlib.pyplot as plt
import numpy as np

def make_4sq_img(
        im_w=100,
        rect_w=40,
        bg_clr=60,
        rect_clr=180,
        scale_by=1.0):
    if scale_by != 1.0:
        im_w = int(np.round(im_w * scale_by))
        rect_w = int(np.round(rect_w * scale_by))
    im_w2 = im_w // 2
    padding = (im_w2 - rect_w) // 2

    img = np.ones((im_w, im_w), dtype=np.uint8) * bg_clr
    rect_pts = []
    for i in range(4):
        sr, sc = (i // 2) * im_w2 + padding, (i % 2) * im_w2 + padding
        rect_pts.append([
            [sr, sc],
            [sr, sc + rect_w],
            [sr + rect_w, sc + rect_w],
            [sr + rect_w, sc]
        ])
        img[sr:(sr + rect_w), sc:(sc + rect_w)] = rect_clr
    return img, rect_pts


def transform_rect_pts(M, rect_pts):
    m = np.array(M[:2, :])
    return [[list(np.matmul(m, pt + [1])) for pt in pts] for pts in rect_pts]


def plot_rect_pts(ax, rect_pts, *args, **kwargs):
    for rect, clr in zip(rect_pts, 'cmky'):
        pts = np.array(rect)
        ax.plot(pts[:, 0], pts[:, 1], clr + 'x', *args, **kwargs)

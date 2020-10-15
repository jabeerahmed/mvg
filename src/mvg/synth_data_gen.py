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
    edges = []
    for i in range(4):
        sr, sc = (i // 2) * im_w2 + padding, (i % 2) * im_w2 + padding
        rect_pts.append([sr, sc, 1.0])
        rect_pts.append([sr, sc + rect_w, 1.0])
        rect_pts.append([sr + rect_w, sc + rect_w, 1.0])
        rect_pts.append([sr + rect_w, sc, 1.0])
        edges.append([(4*i + e) for e in range(4)])
        img[sr:(sr + rect_w), sc:(sc + rect_w)] = rect_clr
    return img, np.array(rect_pts), edges


def transform_rect_pts(M, rect_pts):
    return np.array((M * rect_pts.transpose()).transpose())


def plot_rect_pts(ax, rect_pts, edges, *args, **kwargs):
    loop = [0, 1, 2, 3, 0]
    for edge, clr in zip(edges, 'cmky'):
        pts = rect_pts[np.array(edge)[loop]]
        ax.plot(pts[:, 0], pts[:, 1], clr + 'x--', *args, **kwargs)


def mult_img_pts(H, pts):
    if pts.shape[1] == 2:
        pts = cv2.convertPointsToHomogeneous(pts).reshape(len(pts), 3)
    w_pts = np.array(np.matmul(H, pts.transpose()).transpose())
    return np.array([[x/z, y/z, 1] for x, y, z in w_pts])

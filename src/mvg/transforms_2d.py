import numpy as np
from random import uniform as rand

class MakeTf2d:

    @staticmethod
    def rotation(theta):
        return np.matrix([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta),  np.cos(theta), 0],
            [            0,              0, 1]
        ])

    @staticmethod
    def translation(t_x, t_y):
        return np.matrix([
            [ 1, 0, t_x],
            [ 0, 1, t_y],
            [ 0, 0,   1],
        ])

    @staticmethod
    def similarity(theta, t_x, t_y, scale=1):
        rot = MakeTf2d.rotation(theta)
        rot[:2, :2] *= scale
        trans = MakeTf2d.translation(t_x, t_y)
        return rot * trans

    @staticmethod
    def affine(theta, phi, t_x, t_y, scale_x, scale_y):
        D = np.matrix([
                [scale_x,       0, 0],
                [      0, scale_y, 0],
                [      0,       0, 1]])
        R_theta = MakeTf2d.rotation(theta)
        R_phi = MakeTf2d.rotation(phi)
        R_phi_inv = MakeTf2d.rotation(-phi)
        T_mat = MakeTf2d.translation(t_x=t_x, t_y=t_y)
        A = R_theta * R_phi_inv * D * R_phi
        return T_mat * A

    @staticmethod
    def projective(theta, phi, t_x, t_y, scale_x, scale_y, v_x, v_y):
        M = MakeTf2d.affine(theta, phi, t_x, t_y, scale_x, scale_y)
        M[2, :2] = np.array([v_x, v_y])
        return M


class RandTf2d:
    @staticmethod
    def rotation(rng=(0, np.pi)):
        return MakeTf2d.rotation(rand(*rng))

    @staticmethod
    def translation(tx_rng=(0, 0), ty_rng=(0, 0)):
        return MakeTf2d.translation(t_x=rand(*tx_rng), t_y=rand(*ty_rng))

    @staticmethod
    def euclidean(rot_rng=(0, np.pi), t_x_rng=(0, 0), t_y_rng=(0, 0)):
        return MakeTf2d.similarity(
                theta=rand(*rot_rng),
                t_x=rand(*t_x_rng),
                t_y=rand(*t_y_rng),
                scale=1.0)

    @staticmethod
    def similarity(rot_rng=(0, np.pi), t_x_rng=(0, 0), t_y_rng=(0, 0), scale_rng=(0.1, 2)):
        return MakeTf2d.similarity(
                theta=rand(*rot_rng),
                t_x=rand(*t_x_rng),
                t_y=rand(*t_y_rng),
                scale=rand(*scale_rng))

    @staticmethod
    def affine(
            theta_rng=(0, np.pi),
            phi_rng=(0, np.pi),
            t_x_rng=(0, 1),
            t_y_rng=(0, 1),
            scale_x_rng=(0.1, 2),
            scale_y_rng=(0.1, 2)):
        return MakeTf2d.affine(
                theta=rand(*theta_rng),
                phi=rand(*phi_rng),
                t_x=rand(*t_x_rng),
                t_y=rand(*t_y_rng),
                scale_x=rand(*scale_x_rng),
                scale_y=rand(*scale_y_rng))

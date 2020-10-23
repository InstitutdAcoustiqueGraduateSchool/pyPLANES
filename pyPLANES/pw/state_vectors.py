#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# state_vectors.py
#
# This file is part of pymls, a software distributed under the MIT license.
# For any question, please contact one of the authors cited below.
#
# Copyright (c) 2020
# 	Olivier Dazel <olivier.dazel@univ-lemans.fr>
# 	Mathieu Gaborit <gaborit@kth.se>
# 	Peter Göransson <pege@kth.se>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#

import numpy as np

def PEM_SV(mat,ky):
    ''' S={0:\hat{\sigma}_{xy}, 1:u_y^s, 2:u_y^t, 3:\hat{\sigma}_{yy}, 4:p, 5:u_x^s}'''
    kx_1 = np.sqrt(mat.delta_1**2-ky**2)
    kx_2 = np.sqrt(mat.delta_2**2-ky**2)
    kx_3 = np.sqrt(mat.delta_3**2-ky**2)

    kx = np.array([kx_1, kx_2, kx_3])
    delta = np.array([mat.delta_1, mat.delta_2, mat.delta_3])

    alpha_1 = -1j*mat.A_hat*mat.delta_1**2-1j*2*mat.N*kx[0]**2
    alpha_2 = -1j*mat.A_hat*mat.delta_2**2-1j*2*mat.N*kx[1]**2
    alpha_3 = -2*1j*mat.N*kx[2]*ky

    SV = np.zeros((6,6), dtype=complex)
    SV[0:6, 0] = np.array([-2*1j*mat.N*kx[0]*ky, kx[0], mat.mu_1*kx[0], alpha_1, 1j*delta[0]**2*mat.K_eq_til*mat.mu_1, ky])
    SV[0:6, 3] = np.array([ 2*1j*mat.N*kx[0]*ky,-kx[0],-mat.mu_1*kx[0], alpha_1, 1j*delta[0]**2*mat.K_eq_til*mat.mu_1, ky])

    SV[0:6, 1] = np.array([-2*1j*mat.N*kx[1]*ky, kx[1], mat.mu_2*kx[1],alpha_2, 1j*delta[1]**2*mat.K_eq_til*mat.mu_2, ky])
    SV[0:6, 4] = np.array([ 2*1j*mat.N*kx[1]*ky,-kx[1],-mat.mu_2*kx[1],alpha_2, 1j*delta[1]**2*mat.K_eq_til*mat.mu_2, ky])

    SV[0:6, 2] = np.array([1j*mat.N*(kx[2]**2-ky**2), ky, mat.mu_3*ky, alpha_3, 0., -kx[2]])
    SV[0:6, 5] = np.array([1j*mat.N*(kx[2]**2-ky**2), ky, mat.mu_3*ky, -alpha_3, 0., kx[2]])
    return SV, kx

def elastic_SV(mat,ky, omega):
    ''' S={0:\sigma_{xy}, 1: u_y, 2 \sigma_{yy}, 3 u_x}'''

    P_mat = mat.lambda_ + 2.*mat.mu
    delta_p = omega*np.sqrt(mat.rho/P_mat)
    delta_s = omega*np.sqrt(mat.rho/mat.mu)

    kx_p = np.sqrt(delta_p**2-ky**2)
    kx_s = np.sqrt(delta_s**2-ky**2)

    kx = np.array([kx_p, kx_s])

    alpha_p = -1j*mat.lambda_*delta_p**2 - 2j*mat.mu*kx[0]**2
    alpha_s = 2j*mat.mu*kx[1]*ky

    SV = np.zeros((4, 4), dtype=np.complex)
    SV[0:4, 0] = np.array([-2.*1j*mat.mu*kx[0]*ky,  kx[0], alpha_p, ky])
    SV[0:4, 2] = np.array([ 2.*1j*mat.mu*kx[0]*ky, -kx[0], alpha_p, ky])

    SV[0:4, 1] = np.array([1j*mat.mu*(kx[1]**2-ky**2), ky,-alpha_s, -kx[1]])
    SV[0:4, 3] = np.array([1j*mat.mu*(kx[1]**2-ky**2), ky, alpha_s, kx[1]])

    return SV, kx

def fluid_SV(mat, kx, k):
    ''' S={0:u_y , 1:p}'''
    ky = np.sqrt(k**2-kx**2)
    SV = np.zeros((2, 2), dtype=complex)
    SV[0, 0:2] = np.array([ky/(1j*mat.K*k**2), -ky/(1j*mat.K*k**2)])
    SV[1, 0:2] = np.array([1, 1])
    return SV, ky


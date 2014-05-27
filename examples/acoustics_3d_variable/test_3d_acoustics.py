import os
from itertools import chain

import numpy as np

from clawpack.pyclaw.util import gen_variants
from clawpack.pyclaw.util import check_diff

import acoustics_3d_interface


def test_3d_acoustics():
    """ Tests for homogeneous and heterogeneous 3D acoustics"""

    def acoustics_verify_homogeneous(claw):
        """ Regression test for 3D homogeneous acoustics equations.
        """

        pinitial = claw.frames[0].state.get_q_global()
        pfinal = claw.frames[claw.num_output_times].state.get_q_global()

        if pinitial is not None and pfinal is not None:
            pinitial = pinitial[0, :, :, :].reshape(-1)
            pfinal = pfinal[0, :, :, :].reshape(-1)
            grid = claw.solution.state.grid
            final_difference = np.prod(grid.delta)*np.linalg.norm(pfinal-pinitial, ord=1)
            return check_diff(0., final_difference, abstol=1e-1)
        else:
            return

    def acoustics_verify_heterogeneous(claw):
        """ Regression test for 3D heterogeneous acoustics equations
        """

        pinitial = claw.frames[0].state.get_q_global()
        pfinal = claw.frames[claw.num_output_times].state.get_q_global()

        if pinitial is not None and pfinal is not None:
            pfinal = pfinal[0, :, :, :].reshape(-1)
            thisdir = os.path.dirname(__file__)
            verify_pfinal = np.loadtxt(os.path.join(thisdir, 'verify_classic_heterogeneous.txt'))
            norm_err = np.linalg.norm(pfinal-verify_pfinal)
            return check_diff(0, norm_err, abstol=10.)
        else:
            return

    classic_homogeneous_tests = gen_variants(acoustics_3d_interface.setup, acoustics_verify_homogeneous,
                                             kernel_languages=('Fortran',),
                                             solver_type='classic', test='homogeneous',
                                             disable_output=True)

    classic_heterogeneous_tests = gen_variants(acoustics_3d_interface.setup, acoustics_verify_heterogeneous,
                                               kernel_languages=('Fortran',),
                                               solver_type='classic', test='heterogeneous',
                                               disable_output=True)

    sharp_homogeneous_tests = gen_variants(acoustics_3d_interface.setup, acoustics_verify_homogeneous,
                                           kernel_languages=('Fortran',),
                                           solver_type='sharpclaw', test='homogeneous',
                                           disable_output=True)

    sharp_heterogeneous_tests = gen_variants(acoustics_3d_interface.setup, acoustics_verify_heterogeneous,
                                             kernel_languages=('Fortran',),
                                             solver_type='sharpclaw', test='heterogeneous',
                                             disable_output=True)

    for test in chain(classic_homogeneous_tests, classic_heterogeneous_tests, sharp_homogeneous_tests,
                      sharp_heterogeneous_tests):
        yield test

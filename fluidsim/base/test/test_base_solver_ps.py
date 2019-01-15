import unittest
from glob import glob
import os

import numpy as np

import fluiddyn as fld
import fluiddyn.util.mpi as mpi

# to get fld.show
import fluiddyn.output

from fluidsim.base.solvers.pseudo_spect import SimulBasePseudoSpectral
from fluidsim import modif_resolution_from_dir, load_params_simul

from fluidsim.base.params import load_info_solver

from fluidsim.util.testing import TestSimul


class TestBaseSolverPS(TestSimul):

    Simul = SimulBasePseudoSpectral

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cwd = os.getcwd()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        os.chdir(cls.cwd)

    @classmethod
    def init_params(cls):
        params = cls.params = cls.Simul.create_default_params()
        params.output.periods_plot.phys_fields = 0.2
        params.output.periods_print.print_stdout = 0.2
        params.short_name_type_run = "test_base_solver_ps"

        nh = 8
        Lh = 2 * np.pi
        params.oper.nx = nh
        params.oper.ny = nh
        params.oper.Lx = Lh
        params.oper.Ly = Lh

        params.nu_2 = 1.0

        params.time_stepping.t_end = 0.4

    def test_simul(self):
        """Should be able to run a base experiment."""
        self.sim.time_stepping.start()
        load_params_simul(
            self.sim.output.path_run + "/params_simul.xml",
            only_mpi_rank0=False,
        )

        fld.show()

        if mpi.nb_proc > 1:
            return

        modif_resolution_from_dir(
            self.sim.output.path_run, coef_modif_resol=3.0 / 2, PLOT=False
        )
        path_new = os.path.join(self.sim.output.path_run, "State_phys_12x12")
        os.chdir(path_new)
        load_params_simul()
        path = glob("state_*")[0]
        load_params_simul(path)
        load_info_solver()


if __name__ == "__main__":
    unittest.main()

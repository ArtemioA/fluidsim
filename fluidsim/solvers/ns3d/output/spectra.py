import h5py

import numpy as np

from fluidsim.base.output.spectra3d import Spectra


class SpectraNS3D(Spectra):
    """Save and plot spectra."""

    def compute(self):
        """compute the values at one time."""
        nrj_vx_fft, nrj_vy_fft, nrj_vz_fft = self.output.compute_energies_fft()

        s_vx_kx, s_vx_ky, s_vx_kz = self.oper.compute_1dspectra(nrj_vx_fft)
        s_vy_kx, s_vy_ky, s_vy_kz = self.oper.compute_1dspectra(nrj_vy_fft)
        s_vz_kx, s_vz_ky, s_vz_kz = self.oper.compute_1dspectra(nrj_vz_fft)

        s_kx = s_vx_kx + s_vy_kx + s_vz_kx
        s_ky = s_vx_ky + s_vy_ky + s_vz_ky
        s_kz = s_vx_kz + s_vy_kz + s_vz_kz

        dict_spectra1d = {
            "vx_kx": s_vx_kx,
            "vx_ky": s_vx_ky,
            "vx_kz": s_vx_kz,
            "vy_kx": s_vy_kx,
            "vy_ky": s_vy_ky,
            "vy_kz": s_vy_kz,
            "vz_kx": s_vz_kx,
            "vz_ky": s_vz_ky,
            "vz_kz": s_vz_kz,
            "E_kx": s_kx,
            "E_ky": s_ky,
            "E_kz": s_kz,
        }
        dict_spectra1d = {"spectra_" + k: v for k, v in dict_spectra1d.items()}

        s_vx = self.oper.compute_3dspectrum(nrj_vx_fft)
        s_vy = self.oper.compute_3dspectrum(nrj_vy_fft)
        s_vz = self.oper.compute_3dspectrum(nrj_vz_fft)

        dict_spectra3d = {
            "vx": s_vx,
            "vy": s_vy,
            "vz": s_vz,
            "E": s_vx + s_vy + s_vy,
        }
        dict_spectra3d = {"spectra_" + k: v for k, v in dict_spectra3d.items()}

        if self.has_to_save_kzkh():
            dict_kzkh = {
                "K": self.oper.compute_spectrum_kzkh(
                    nrj_vx_fft + nrj_vy_fft + nrj_vz_fft
                )
            }
        else:
            dict_kzkh = None

        return dict_spectra1d, dict_spectra3d, dict_kzkh

    def plot1d_times(
        self,
        tmin=0,
        tmax=None,
        delta_t=None,
        coef_compensate=0,
        key="E",
        key_k="kx",
        coef_plot_k3=None,
        coef_plot_k53=None,
        xlim=None,
        ylim=None,
        only_time_average=False,
    ):

        self._plot_times(
            tmin=tmin,
            tmax=tmax,
            delta_t=delta_t,
            coef_compensate=coef_compensate,
            key=key,
            key_k=key_k,
            coef_plot_k3=coef_plot_k3,
            coef_plot_k53=coef_plot_k53,
            xlim=xlim,
            ylim=ylim,
            ndim=1,
            only_time_average=only_time_average,
        )

    def plot3d_times(
        self,
        tmin=0,
        tmax=None,
        delta_t=None,
        coef_compensate=0,
        key="E",
        coef_plot_k3=None,
        coef_plot_k53=None,
        xlim=None,
        ylim=None,
        only_time_average=False,
    ):

        self._plot_times(
            tmin=tmin,
            tmax=tmax,
            delta_t=delta_t,
            coef_compensate=coef_compensate,
            key=key,
            coef_plot_k3=coef_plot_k3,
            coef_plot_k53=coef_plot_k53,
            xlim=xlim,
            ylim=ylim,
            ndim=3,
            only_time_average=only_time_average,
        )

    def _plot_times(
        self,
        tmin=0,
        tmax=None,
        delta_t=None,
        coef_compensate=0,
        key="E",
        key_k="kx",
        coef_plot_k3=None,
        coef_plot_k53=None,
        xlim=None,
        ylim=None,
        only_time_average=False,
        ndim=1,
    ):

        if ndim not in [1, 3]:
            raise ValueError

        path_file = getattr(self, f"path_file{ndim}d")

        if ndim == 1:
            key_spectra = "spectra_" + key + "_" + key_k
            key_k_label = "k_" + key_k[-1]
        else:
            key_spectra = "spectra_" + key
            key_k = "k_spectra3d"
            key_k_label = "k"

        with h5py.File(path_file, "r") as h5file:
            times = h5file["times"][...]

            if tmax is None:
                tmax = times.max()

            ks = h5file[key_k][...]

        ks_no0 = ks.copy()
        ks_no0[ks == 0] = np.nan

        delta_t_save = np.diff(times).mean()

        if delta_t is None:
            nb_curves = 20
            delta_t = (times[-1] - times[0]) / nb_curves

        delta_i_plot = int(np.round(delta_t / delta_t_save))
        if delta_i_plot == 0:
            delta_i_plot = 1
        delta_t = delta_t_save * delta_i_plot

        imin_plot = np.argmin(abs(times - tmin))
        imax_plot = np.argmin(abs(times - tmax))

        tmin_plot = times[imin_plot]
        tmax_plot = times[imax_plot]

        print(
            f"plot{ndim}d_times(tmin={tmin:8.6g}, tmax={tmax:8.6g}, delta_t={delta_t:8.6g},"
            f" coef_compensate={coef_compensate:.3f})\n"
            f"""plot {ndim}D spectra
tmin = {tmin_plot:8.6g} ; tmax = {tmax_plot:8.6g} ; delta_t = {delta_t:8.6g}
imin = {imin_plot:8d} ; imax = {imax_plot:8d} ; delta_i = {delta_i_plot}"""
        )

        fig, ax = self.output.figure_axe()
        ax.set_xlabel(f"${key_k_label}$")
        ax.set_ylabel("spectra " + key)
        ax.set_title(
            f"{ndim}D spectra, solver "
            + self.output.name_solver
            + f", nx = {self.nx:5d}"
        )
        ax.set_xscale("log")
        ax.set_yscale("log")

        with h5py.File(path_file, "r") as h5file:
            dset_spectra = h5file[key_spectra]
            coef_norm = ks_no0 ** (coef_compensate)
            if not only_time_average:
                for it in range(imin_plot, imax_plot + 1, delta_i_plot):
                    spectrum = dset_spectra[it]
                    spectrum[spectrum < 10e-16] = 0.0
                    ax.plot(ks, spectrum * coef_norm)

            spectra = dset_spectra[imin_plot : imax_plot + 1]
        spectrum = spectra.mean(0)
        spectrum[spectrum < 10e-16] = 0.0
        ax.plot(ks, spectrum * coef_norm, "k", linewidth=2)

        if coef_plot_k3 is not None:
            to_plot = coef_plot_k3 * ks_no0 ** (-3) * coef_norm
            ax.plot(ks[1:], to_plot[1:], "k--")

        if coef_plot_k53 is not None:
            to_plot = coef_plot_k53 * ks_no0 ** (-5.0 / 3) * coef_norm
            ax.plot(ks[1:], to_plot[1:], "k-.")

        if xlim is not None:
            ax.set_xlim(xlim)

        if ylim is not None:
            ax.set_ylim(ylim)

    def plot_kzkh(self, tmin=0, tmax=None, key="K", ax=None):
        data = self.load_kzkh_mean(tmin, tmax, key)
        spectrum = np.log10(data[key])
        kz = data["kz"]
        kh = data["kh_spectra"]

        if ax is None:
            fig, ax = self.output.figure_axe()

        ax.set_xlabel(r"$\kappa_h$")
        ax.set_ylabel("$k_z$")
        ax.set_title(
            "log 3D spectra, solver "
            + self.output.name_solver
            + f", nx = {self.nx:5d}"
        )

        ax.pcolormesh(kh, kz, spectrum)

    def plot1d(
        self,
        tmin=0,
        tmax=None,
        coef_compensate=0,
        coef_plot_k3=None,
        coef_plot_k53=None,
        xlim=None,
        ylim=None,
    ):
        print("TODO: implement this function plot1d!")

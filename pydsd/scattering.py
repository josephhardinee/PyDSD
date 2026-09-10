"""
Scattering backend selection for PyDSD.

PyDSD performs T-matrix scattering simulations through the API originally
provided by ``pytmatrix``. ``rustmatrix`` is a Rust-backed, drop-in
replacement for that API which is actively maintained and considerably
faster. This module selects ``rustmatrix`` when it is installed and
transparently falls back to ``pytmatrix`` otherwise, re-exporting the
handful of names PyDSD relies on so the rest of the code base is agnostic
to which backend is in use.

The active backend name is available as :data:`BACKEND`.
"""

try:
    import rustmatrix as _backend
    from rustmatrix import psd, orientation, radar, scatter, tmatrix_aux, refractive
    from rustmatrix import Scatterer  # top-level in rustmatrix, not a submodule
    from rustmatrix.psd import PSDIntegrator, GammaPSD, BinnedPSD

    BACKEND = "rustmatrix"
except ImportError:  # pragma: no cover - exercised only without rustmatrix
    import pytmatrix as _backend
    from pytmatrix import psd, orientation, radar, scatter, tmatrix_aux, refractive
    from pytmatrix.tmatrix import Scatterer
    from pytmatrix.psd import PSDIntegrator, GammaPSD, BinnedPSD

    BACKEND = "pytmatrix"

# The linear depolarization ratio lives in the ``scatter`` module of both
# backends. pytmatrix additionally re-exports it through ``radar``; rustmatrix
# does not, so we source it from ``scatter`` for a backend-agnostic handle.
ldr = scatter.ldr

__all__ = [
    "BACKEND",
    "psd",
    "orientation",
    "radar",
    "scatter",
    "tmatrix_aux",
    "refractive",
    "Scatterer",
    "PSDIntegrator",
    "GammaPSD",
    "BinnedPSD",
    "ldr",
]

import numpy as np
import copy


def filter_spectrum_with_parsivel_matrix(
    dsd, over_fall_speed=0.5, under_fall_speed=0.5, replace=True
):
    """ Filter a drop spectrum using fall speed matrix for Parsivels.  This requires that velocity is set on the object
    for both raw spectra and calculated terminal fall speed. If terminal fall speed is not available, this can be calculated
    using pydsd.
    Parameters
    ----------
    over_fall_speed: float, default 0.5
        Filter out drops more than this factor of terminal fall speed.
    under_fall_speed: float, default 0.5
        Filter out drops more than this factor under terminal fall speed.


    Returns
    -------
    filtered_spectrum_data_array: np.ndarray
        Filtered Drop Spectrum Array

    Example
    -------
    filter_spectrum_with_parsivel_matrix(dsd, over_fall_speed=.5, under_fall_speed=.5, replace=True)
    """
    # TODO: This can be easily generalized for other disdrometers.
    terminal_fall_speed = dsd.velocity["data"]
    spectra_velocity = dsd.spectrum_fall_velocity["data"]

    pcm_matrix = np.zeros((32, 32))
    for idx in np.arange(0, 32):
        pcm_matrix[idx] = np.logical_and(
            spectra_velocity > (terminal_fall_speed[idx] * (1 - under_fall_speed)),
            spectra_velocity < (terminal_fall_speed[idx] * (1 + over_fall_speed)),
        )

    pcm_matrix = pcm_matrix.T.astype(int)

    if replace:
        dsd.fields["drop_spectrum"]["data"] = dsd.fields["drop_spectrum"][
            "data"
        ] * pcm_matrix
        dsd.fields["drop_spectrum"]["history"] = dsd.fields["drop_spectrum"].get(
            "history", ""
        ) + "Filtered for speeds above {over_fall_speed} of Vt and below {under_fall_speed} of Vt"
    else:
        return dsd.fields["drop_spectrum"]["data"] * pcm_matrix


def filter_nd_on_dropsize(dsd, drop_min=None, drop_max=None, replace=True):
    """ Filter Nd field based on a min and/or max dropsize.
    
    Parameters
    ----------
    dsd: `DropSizeDistribution` object
        DSD object to base filtering on
    drop_min: float
        Filter drops under drop_min (mm) in size.
    drop_max: float
        Filter drops larger than drop_max (mm) in size.
    replace: boolean
        Whether to overwrite the Nd in fields. If replacing, no value is returned.

    Returns
    -------
    Nd: dictionary
        Updated Nd dictionary. Data and a history field.
    """
    diameter = dsd.diameter["data"]

    if drop_min is None:
        drop_min = 0
    if drop_max is None:
        drop_max = diameter[-1] + 100

    mask = np.logical_and(diameter > drop_min, diameter < drop_max)

    if replace:
        dsd.fields['Nd']["data"] = dsd.fields['Nd']["data"] * mask
        dsd.fields['Nd']["history"] = dsd.fields['Nd'].get(
            "history", ""
        ) + f"\nFiltered between {drop_min} and {drop_max}"
    else:
        Nd = copy.deepcopy(dsd.fields['Nd'])
        Nd["data"] = Nd["data"] * mask
        Nd["history"] = dsd.fields['Nd'].get(
            "history", ""
        ) + f"Filtered between {drop_min} and {drop_max}\n"
        return Nd


def filter_spectrum_on_dropsize(dsd, drop_min=None, drop_max=None, replace=True):
    """ Filter Nd field based on a min and/or max dropsize.
    
    Parameters
    ----------
    dsd: `DropSizeDistribution` object
        DSD object to base filtering on
    drop_min: float
        Filter drops under drop_min (mm) in size.
    drop_max: float
        Filter drops larger than drop_max (mm) in size.
    replace: boolean
        Whether to replace the spectrum stored on dsd object. If set, no data is returned.

    Returns
    -------
    Nd: dictionary
        Updated Nd dictionary. Data and a history field.
    """
    diameter = dsd.diameter["data"]

    if drop_min is None:
        drop_min = 0
    if drop_max is None:
        drop_max = diameter[-1] + 100

    mask = np.logical_and(diameter > drop_min, diameter < drop_max)

    if replace:
        dsd.Nd["data"] = dsd.Nd["data"] * mask
        dsd.Nd["history"] = dsd.Nd.get(
            "history", ""
        ) + f"\nFiltered between {drop_min} and {drop_max}"
    else:
        Nd = copy.deepcopy(dsd.Nd)
        Nd["data"] = Nd["data"] * mask
        Nd["history"] = dsd.Nd.get(
            "history", ""
        ) + f"Filtered between {drop_min} and {drop_max}\n"
        return Nd


def parsivel_sampling_area(diameter):
    """ Calculate effective sampling area for Parsivels
    
    Parameters
    ----------
    diameter: np.ndarray or float
        Drop Diameter
    
    Returns
    -------
    Aeff: np.ndarray or float
        Effective Sampling Area
    """
    return 180 * (30 - 0.5 * diameter)


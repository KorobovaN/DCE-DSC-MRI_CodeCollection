import os
import pytest
import numpy as np
from time import perf_counter
from ..helpers import osipi_parametrize, log_init, log_results
import osipi_code_collection.original.MB_QBI_UoManchesterUK.QbiPy.dce_models.dce_aif as dce_aif
from . import popAIF_data


# All tests will use the same arguments and same data...
arg_names = 'label, time, cb_ref_values, delay, a_tol, r_tol'
test_data = (
        popAIF_data.ParkerAIF_refdata() +
        popAIF_data.ParkerAIF_refdata_delay())

filename_prefix = ''

def setup_module(module):
    # initialize the logfiles
    global filename_prefix # we want to change the global variable
    filename_prefix = 'PopulationAIF_DCE/TestResults_PopAIF'
    log_init(filename_prefix, '_Parker_AIF_MB_QBI_UoManchesterUK', ['label', 'aif_ref', 'cb_measured', 'time (us)'])

# Use the test data to generate a parametrize decorator. This causes the following
# test to be run for every test case listed in test_data...
# In the following test, we specify 5 cases that are expected to fail as this function expects the delay to be specified according to the temp resolution
@osipi_parametrize(arg_names, test_data, xf_labels=[])
def test_Parker_AIF_MB_QBI_UoManchesterUK(label, time, cb_ref_values, delay, a_tol, r_tol):

    # prepare input data
    # time array is expected in minutes, so no changes needed.
    hct = 0  # for now ignore hematocrit correction to obtain Cb values
    #time = time*60  # put in seconds
    # Create the AIF object
    tic = perf_counter()
    aif = dce_aif.Aif(times=time, hct=hct, prebolus=1) # default setting for prebolus = 8;
    #aif_values = aif.base_aif_[0,] # this is the population aif without prebolus
    aif_delay = dce_aif.Aif.compute_population_AIF(aif, offset=delay/60) # an additional delay is modulated with an additional offset parameter. aif_values and aif_delay are the same when offset is set to 0.
    exc_time = 1e6 * (perf_counter() - tic)  # measure execution time
    log_results(filename_prefix, '_Parker_AIF_MB_QBI_UoManchesterUK', [label, cb_ref_values, aif_delay[0,], f"{exc_time:.0f}"])

    np.testing.assert_allclose([aif_delay[0,]], [cb_ref_values], rtol=r_tol, atol=a_tol)

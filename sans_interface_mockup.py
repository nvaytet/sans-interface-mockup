import ipywidgets as w
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import IPython.display as disp


def run_numbers_tab():
    user_file = w.Text(description='User file:',
                       layout={'width': "700px"},
                       value='/home/user/work/experiments/SANS/some_file.txt')
    reload_but = w.Button(description='Reload')

    data_dir = w.Text(description='Data directory:',
                      layout={'width': "700px"},
                      value='/home/user/work/experiments/SANS/')
    manage_but = w.Button(description='Manage Directories')

    single_batch_run = w.RadioButtons(
        options=['Single run mode', 'Batch mode'])
    multip_check = w.Checkbox(description='Multi-period')
    instr_dropdn = w.Dropdown(options=['LOQ', 'SANS2D', 'Larmor', 'Zoom'],
                              description='Instrument')
    hrule = w.HTML(value='<hr>')

    # Scattering box
    scat_sam = w.HBox([
        w.Text(value='68997', description='Sample', layout={'width': "170px"}),
        w.FileUpload(description='', layout={'width': "70px"})
    ])
    scat_can = w.HBox([
        w.Text(value='68998', description='Can', layout={'width': "170px"}),
        w.FileUpload(description='', layout={'width': "70px"})
    ])
    scat = w.VBox(children=[w.Label(value='Scattering'), scat_sam, scat_can],
                  layout={'border': 'solid 1px lightgrey'})

    # Transmission box
    trans_sam = w.HBox([
        w.Text(value='68999', description='Sample', layout={'width': "170px"}),
        w.FileUpload(description='', layout={'width': "70px"})
    ])
    trans_can = w.HBox([
        w.Text(value='69000', description='Can', layout={'width': "170px"}),
        w.FileUpload(description='', layout={'width': "70px"})
    ])
    trans = w.VBox(
        children=[w.Label(value='Transmission'), trans_sam, trans_can],
        layout={'border': 'solid 1px lightgrey'})

    # Direct box
    dir_sam = w.HBox([
        w.Text(value='69001', description='Sample', layout={'width': "170px"}),
        w.FileUpload(description='', layout={'width': "70px"})
    ])
    dir_can = w.HBox([
        w.Text(value='69002', description='Can', layout={'width': "170px"}),
        w.FileUpload(description='', layout={'width': "70px"})
    ])
    direct = w.VBox(children=[w.Label(value='Direct'), dir_sam, dir_can],
                    layout={'border': 'solid 1px lightgrey'})

    # Options box
    opts = w.HBox([
        w.Checkbox(description='Plot result', indent=False),
        w.Checkbox(description='Verbose', indent=False),
        w.Checkbox(description='Log Colette cmds', indent=False)
    ])
    options = w.VBox(children=[w.Label(value='Options'), opts],
                     layout={'border': 'solid 1px lightgrey'})

    # Reduce box
    red_buts = w.HBox([
        w.Button(description='Load Data'),
        w.Button(description='1D Reduce'),
        w.Button(description='2D Reduce')
    ])
    red = w.VBox(children=[w.Label(value='Reduce'), red_buts],
                 layout={'border': 'solid 1px lightgrey'})

    # Save box
    filename = w.Text(description='Filename:')
    browse_but = w.Button(description='Browse')
    save_row1 = w.HBox([filename, browse_but])
    formats = w.HBox([
        w.Label(value='Formats:', layout={'width': '200px'}),
        w.Checkbox(description='Nexus', indent=False),
        w.Checkbox(description='CanSAS', indent=False),
        w.Checkbox(description='RKH', value=True, indent=False),
        w.Checkbox(description='CSV', indent=False)
    ])
    save_buts = w.HBox([
        w.Button(description='Save Result', disabled=True),
        w.Button(description='Save Other')
    ])
    save_box = w.VBox([w.Label(value='Save'), save_row1, formats, save_buts],
                      layout={'border': 'solid 1px lightgrey'})

    children = [
        w.HBox([user_file, reload_but]),
        w.HBox([data_dir, manage_but]),
        w.HBox([single_batch_run, multip_check, instr_dropdn]), hrule,
        w.GridBox([scat, trans, direct],
                  layout=w.Layout(grid_template_columns="repeat(3, 250px)",
                                  grid_gap='20px')), hrule,
        w.GridBox([
            w.GridBox([options, red],
                      layout=w.Layout(grid_template_columns="repeat(1, 450px)",
                                      grid_gap='10px')), save_box
        ],
                  layout=w.Layout(grid_template_columns="repeat(2, 450px)",
                                  grid_gap='20px'))
    ]
    return children


def analysis_details_tab():
    column_width = "130px"

    grav = w.Checkbox(description='Account for gravity', indent=False)
    lims = w.HTML(value='<b>Limits</b>')

    blank = w.Label(value='')

    grid_box = w.GridBox(
        [
            # Row 1
            blank,
            w.Label(value='Min', layout={'width': column_width}),
            w.Label(value='Max', layout={'width': column_width}),
            blank,
            blank,
            blank,
            # Row 2
            w.Label(value='Radius (mm)', layout={'width': column_width}),
            w.FloatText(value=35, layout={'width': column_width}),
            w.FloatText(value=750, layout={'width': column_width}),
            blank,
            blank,
            blank,
            # Row 3
            w.Label(value='Wavelength (A)', layout={'width': column_width}),
            w.FloatText(value=2.2, layout={'width': column_width}),
            w.FloatText(value=10.0, layout={'width': column_width}),
            w.Label(value='dW / W', layout={'width': column_width}),
            w.FloatText(value=0.035, layout={'width': column_width}),
            w.Dropdown(options=['Logarithmic', 'Linear'],
                       layout={'width': column_width}),
            # Row 4
            w.Label(value='Qx (A^-1)', layout={'width': column_width}),
            w.FloatText(value=0.008, layout={'width': column_width}),
            w.FloatText(value=1.5, layout={'width': column_width}),
            w.Label(value='dQ / Q', layout={'width': column_width}),
            w.FloatText(value=0.06, layout={'width': column_width}),
            w.Dropdown(options=['Logarithmic', 'Linear'],
                       layout={'width': column_width}),
            # Row 5
            w.Label(value='Qxy (A^-1)', layout={'width': column_width}),
            w.FloatText(value=0.1, layout={'width': column_width}),
            blank,
            w.Label(value='step', layout={'width': column_width}),
            w.FloatText(value=0.002, layout={'width': column_width}),
            w.Dropdown(options=['Logarithmic', 'Linear'],
                       layout={'width': column_width}),
            # Row 6
            w.Dropdown(options=['Sample', 'Background'],
                       layout={'width': column_width}),
            w.Checkbox(description='Trans Fit (A)',
                       indent=False,
                       layout={'width': column_width}),
            w.Checkbox(description='Use',
                       indent=False,
                       layout={'width': column_width}),
            w.FloatText(value=0, disabled=True, layout={'width': column_width
                                                        }),
            w.FloatText(value=0, disabled=True, layout={'width': column_width
                                                        }),
            w.Dropdown(options=['Polynomial3', 'Logarithmic', 'Linear'],
                       layout={'width': column_width}),
            # Row 7
            w.Label(value='Can', layout={'width': column_width}),
            w.Checkbox(description='Trans Fit (A)',
                       indent=False,
                       value=True,
                       layout={'width': column_width}),
            w.Checkbox(description='Use',
                       indent=False,
                       value=True,
                       layout={'width': column_width}),
            w.FloatText(value=2.2, layout={'width': column_width}),
            w.FloatText(value=10.0, layout={'width': column_width}),
            w.Dropdown(options=['Polynomial3', 'Logarithmic', 'Linear'],
                       layout={'width': column_width})
        ],
        layout=w.Layout(
            grid_template_columns="repeat(6, {})".format(column_width),
            grid_gap='5px'))
    return [grav, lims, grid_box]


def fitting_tab():
    def lorentzian(xx, scale=1.0, center=1.0, hwhm=3.0):
        if hwhm == 0:
            raise ValueError('hwhm of the lorentzian is equal to zero.')
        return scale * hwhm / ((xx - center)**2 + hwhm**2) / np.pi

    xx = np.linspace(-10, 10, 500)
    lorentzian_noisy_exo = lorentzian(xx, 3, 4, 0.5) * (
        1. + 0.1 * np.random.normal(0, 1, 500)) + 0.01 * np.random.normal(
            0, 1, 500)

    initial_params = [5.5, 0.0, 0.55]

    fig8 = plt.figure()
    gs = fig8.add_gridspec(3, 1)
    f8_ax1 = fig8.add_subplot(gs[0:2, :])
    f8_ax2 = fig8.add_subplot(gs[2, :])
    f8_ax1.plot(xx, lorentzian_noisy_exo, label="reference data for exercise")
    lines = f8_ax1.plot(xx,
                        lorentzian(xx, *initial_params),
                        label='model to be fitted')
    fit_lines = f8_ax1.plot(xx, np.zeros_like(xx), '--', label='fit')
    res_lines = f8_ax2.plot(xx, np.zeros_like(xx), label='residuals')
    f8_ax1.set_ylabel('lorentzian(x,{},{},{})'.format(*initial_params))
    f8_ax1.set_xlabel('x')
    f8_ax1.grid()
    f8_ax1.legend()
    f8_ax2.set_xlabel('x')
    f8_ax2.grid()
    f8_ax2.legend()

    def interactive_plot_exo(scale, center, hwhm):
        lines[0].set_ydata(lorentzian(xx, scale, center, hwhm))
        plt.ylabel('lorentzian(x,{scale},{center},{hwhm})'.format(
            scale=scale, center=center, hwhm=hwhm))

    interactive_plot_exo = w.interactive(interactive_plot_exo,
                                         scale=(1.0, 10.0),
                                         center=(-5.0, 5.0),
                                         hwhm=(0.1, 1.0))

    # Define function to reset all parameters' values to the initial ones
    def reset_values(b):
        for i, p in enumerate(initial_params):
            interactive_plot_exo.children[i].value = p

    # Define reset button and occurring action when clicking on it
    reset_button_exo = w.Button(description="Reset")
    reset_button_exo.on_click(reset_values)

    params_exo = [0, 0, 0]
    pcov_exo = [0, 0, 0]

    # Capture fit results output
    fit_results = w.Output()

    chosen_method_optim = w.RadioButtons(
        options=['lm', 'trf', 'dogbox'],
        value='lm',  # Defaults to 'lm'
        description='Method for optimization',
        style={'description_width': 'initial'},
        disabled=False)

    # Define reset button and occurring action when clicking on it
    run_fit_button = w.Button(description="Fit!")

    def run_fit(button):
        params_exo, pcov_exo = curve_fit(lorentzian,
                                         xx,
                                         lorentzian_noisy_exo,
                                         method=chosen_method_optim.value,
                                         p0=initial_params)
        fit_results.clear_output()
        with fit_results:
            params_error = np.sqrt(np.diag(pcov_exo))
            print('Values of refined parameters:')
            print('scale:', params_exo[0], '+/-', params_error[0])
            print('center :', params_exo[1], '+/-', params_error[1])
            print('HWHM', params_exo[2], '+/-', params_error[2])
        fit_lines[0].set_ydata(lorentzian(xx, *params_exo))
        res_lines[0].set_ydata(lorentzian_noisy_exo - fit_lines[0].get_ydata())

    run_fit_button.on_click(run_fit)

    disp.display(
        w.VBox([
            interactive_plot_exo, reset_button_exo,
            w.HBox([chosen_method_optim, run_fit_button, fit_results])
        ]))
    return


def SANS_interface():
    """
    Usage:
        from sans_interface_mockup import SANS_interface
        %matplotlib notebook # optional
        SANS_interface()
    """

    tab_height = '800px'

    # Handling of matplotlib figures is ugly: an output widget has to be
    # created AND displayed (!!) before any plotting takes place, if not the
    # figure is not captured in the output.
    out = w.Output(layout={'height': tab_height})

    tab_list = {
        'Run Numbers': w.VBox(layout={'height': tab_height}),
        'Analysis Details': w.VBox(layout={'height': tab_height}),
        'Fitting': out,
        'Masking': w.VBox(layout={'height': tab_height}),
        'Logging - WARNINGS': w.VBox(layout={'height': tab_height}),
        'Add Runs': w.VBox(layout={'height': tab_height}),
        'Diagnostics': w.VBox(layout={'height': tab_height}),
        'Display': w.VBox(layout={'height': tab_height})
    }

    tabs = w.Tab()
    tabs.children = list(tab_list.values())
    for i, t in enumerate(tab_list):
        tabs.set_title(i, t)

    tab_list['Run Numbers'].children = run_numbers_tab()
    tab_list['Analysis Details'].children = analysis_details_tab()

    disp.display(tabs)

    with out:
        fitting_tab()

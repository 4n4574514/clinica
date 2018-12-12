# coding: utf8

import clinica.engine as ce

class fMRIPreprocessingCLI(ce.CmdParser):
    """
    """

    def define_name(self):
        """Define the sub-command name to run this pipelines.
        """
        self._name = 'fmri-preprocessing'


    def define_description(self):
        """Define a description of this pipeline.
        """
        self._description = 'Preprocessing of raw fMRI datasets:\nhttp://clinica.run/doc/Pipelines/fMRI_Preprocessing/'

    def define_options(self):
        """Define the sub-command arguments
        """

        from clinica.engine.cmdparser import PIPELINE_CATEGORIES

        clinica_comp = self._args.add_argument_group(
                PIPELINE_CATEGORIES['CLINICA_COMPULSORY'])
        clinica_comp.add_argument("bids_directory",
                                help='Path to the BIDS directory.')
        clinica_comp.add_argument("caps_directory",
                                help='Path to the CAPS directory.')

        clinica_opt = self._args.add_argument_group(
                PIPELINE_CATEGORIES['CLINICA_OPTIONAL'])
        clinica_opt.add_argument("-tsv", "--subjects_sessions_tsv",
                                help='TSV file containing a list of subjects with their sessions.')
        clinica_opt.add_argument("-wd", "--working_directory",
                                help='Temporary directory to store pipelines intermediate results.')
        clinica_opt.add_argument("-np", "--n_procs", type=int,
                                help='Number of processors to run in parallel.')
        clinica_opt.add_argument("-sl", "--slurm", action='store_true',
                                help='Run the pipelines using SLURM.')
        clinica_opt.add_argument("-sa", "--sbatch_args",
                                help='SLURM\'s sbatch tool arguments.')

        optional = self._args.add_argument_group(
                PIPELINE_CATEGORIES['OPTIONAL'])
        optional.add_argument("-fwhm", "--full_width_at_half_maximum",
                                nargs=3, type=int, default=[8, 8, 8],
                                help="Size of the FWHM filter in milimeters to smooth the image (default: --full_width_at_half_maximum 8 8 8).")
        optional.add_argument("-t1s", "--t1_native_space", action='store_true',
                                help="Also return images in T1 native space.")
        optional.add_argument("-fsbm", "--freesurfer_brain_mask",
                                action='store_true',
                                help="Use FreeSurfer's pre-computed brain mask from the CAPS folder instead of running FSL bet.")
        optional.add_argument("-u", "--unwarping",
                                action='store_true',
                                help="Add SPM's Unwarping to the Realign step (magnitude and phasediff files are necessary in the BIDS directory).")


    def run_command(self, args):
        """
        """

        from .fmri_preprocessing_pipeline import fMRIPreprocessing

        pipeline = fMRIPreprocessing(bids_directory=self.absolute_path(args.bids_directory),
                                     caps_directory=self.absolute_path(args.caps_directory),
                                     tsv_file=self.absolute_path(args.subjects_sessions_tsv))
        pipeline.parameters = {
            'full_width_at_half_maximum' : args.full_width_at_half_maximum,
            't1_native_space'            : args.t1_native_space,
            'freesurfer_brain_mask'      : args.freesurfer_brain_mask,
            'unwarping'                  : args.unwarping
        }
        pipeline.base_dir = self.absolute_path(args.working_directory)
        if args.n_procs:
            pipeline.run(plugin='MultiProc', plugin_args={'n_procs': args.n_procs})
        elif args.slurm:
            pipeline.run(plugin='SLURMGraph', plugin_args = {
                'dont_resubmit_completed_jobs': True, 'sbatch_args':
                    args.sbatch_args})
        else:
            pipeline.run()

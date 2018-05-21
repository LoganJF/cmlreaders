import os
import pytest
import functools
from pkg_resources import resource_filename
from cmlreaders import CMLReader

datafile = functools.partial(resource_filename, 'cmlreaders.test.data')


class TestCMLReader:
    @pytest.mark.rhino
    @pytest.mark.parametrize("file_type", [
        'voxel_coordinates', 'classifier_excluded_leads', 'jacksheet',
        'good_leads', 'leads', 'electrode_coordinates', 'prior_stim_results',
        'target_selection_table', 'electrode_categories', 'classifier_summary',
        'math_summary', 'session_summary', 'pairs', 'contacts', 'localization'
    ])
    def test_load_from_rhino(self, file_type, rhino_root):
        subject = "R1405E"
        experiment = "FR1"
        session = 1
        localization = 0

        if file_type in ["electrode_categories", "classifier_summary",
                         "math_summary", "session_summary"]:
            subject = "R1111M"
            experiment = "FR2"
            session = 0

        reader = CMLReader(subject=subject, localization=localization,
                           experiment=experiment, session=session,
                           rootdir=rhino_root)

    @pytest.mark.parametrize("file_type", [
        'voxel_coordinates.txt', 'classifier_excluded_leads.txt',
        'jacksheet.txt', 'good_leads.txt', 'leads.txt',
        'electrode_coordinates.csv', 'prior_stim_results.csv',
        'target_selection_table.csv', 'classifier_summary.h5',
        'math_summary.h5', 'session_summary.h5', 'pairs.json', 'contacts.json',
        'localization.json'
    ])
    def test_load(self, file_type):
        data_type = os.path.splitext(file_type)[0]
        reader = CMLReader(subject="R1405E", localization=0, experiment="FR5",
                           session=1)
        reader.load(data_type=data_type, file_path=datafile(file_type))

    @pytest.mark.parametrize("file_type", [
        'voxel_coordinates', 'classifier_excluded_leads', 'jacksheet',
        'good_leads', 'leads', 'electrode_coordinates', 'prior_stim_results',
        'target_selection_table', 'classifier_summary', 'math_summary',
        'session_summary', 'pairs', 'contacts', 'localization'
    ])
    def test_get_reader(self, file_type):
        reader = CMLReader(subject='R1405E', localization=0, experiment='FR1',
                           session=0, montage=0)
        reader_obj = reader.get_reader(file_type, file_path=datafile(file_type))
        assert type(reader_obj) == reader.readers[file_type]

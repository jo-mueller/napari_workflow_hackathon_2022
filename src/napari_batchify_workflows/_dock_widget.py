"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton
from magicgui import magic_factory

from skimage import io

import os
import pickle
import glob

from qtpy import QtWidgets

class WorkflowDispatcher(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn_load_workflow = QPushButton("Load workflow")
        btn_find_files = QPushButton("Detect files")
        btn_run_workflow = QPushButton("Run workflow")

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn_load_workflow)
        self.layout().addWidget(btn_find_files)
        self.layout().addWidget(btn_run_workflow)

        btn_load_workflow.clicked.connect(self._load_workflow)
        btn_find_files.clicked.connect(self._select_data)
        btn_run_workflow.clicked.connect(self._run_workflow)

    def _select_data(self):
        self.dirname = QtWidgets.QFileDialog.getExistingDirectory()
        self.filenames = []

        for f in glob.glob(os.path.join(self.dirname, '**/*.tif'), recursive=True):
            self.filenames.append(f)

            print('Detected ', f)

    def _load_workflow(self):

        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        with open(filename, "rb") as p:
            self.workflow = pickle.load(p)
            print('Loaded: ', self.workflow)

    def _run_workflow(self):

        for img in self.filenames:

            directory = os.path.dirname(img)
            print('processing ', img)

            outfile = os.path.join(directory,
                                   os.path.basename(img).split('.')[0] + '_processed.tif')
            print(outfile)

            image = io.imread(img)
            print(image)
            self.workflow.set("input", image)
            result = self.workflow.get("blurred")

            io.imsave(outfile, result)

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [WorkflowDispatcher]

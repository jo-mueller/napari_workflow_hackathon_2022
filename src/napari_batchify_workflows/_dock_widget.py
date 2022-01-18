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
        btn_find_files = QPushButton("Load workflow")
        btn_load_workflow.clicked.connect(self._load_workflow)
        btn_find_files.clicked.connect(self._select_data)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn_load_workflow)
        self.layout().addWidget(btn_find_files)

    def _select_data(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory()
        import glob
        for f in glob.glob('/Users/fernandesm/Downloads/Wormhole P92eZ/211229/P2/CS1/*.tif', recursive=True):
            print(f)

    def _load_workflow(self):

        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        with open(filename, "rb") as p:
            self.workflow = pickle.load(p)

    def _run_workflow(self, list_of_images: list):

        for img in list_of_images:

            image = io.imread(img)
            directory = os.path.dirname(image)

            outfile = os.path.join(directory,
                                   os.path.basename(image).split('.')[0] + 'processed.tif')

            self.workflow.set("Input", image)
            result = self.workflow.get("labeled")

            io.imwrite(result)

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [WorkflowDispatcher]

from os import path, mkdir
from pyPLANES.classes.entity_classes import IncidentPwFem, TransmissionPwFem


def initialisation_out_files(self, p):
    # Creation of the directory if it .oes not exists
    if hasattr(p,"outfiles_directory"):
        if p.outfiles_directory != "":
            directory = p.outfiles_directory
            if not path.exists(directory):
                mkdir(directory)
            self.outfile = open(directory + "/pyPLANES.out", "w")
            self.resfile = open(directory + "/pyPLANES.res", "w")
        else:
            self.outfile = open("pyPLANES.out", "w")
            self.resfile = open("pyPLANES.res", "w")
    else :
        self.outfile = open("pyPLANES.out", "w")
        self.resfile = open("pyPLANES.res", "w")


    self.resfile.write("Frequency [Hz]\n")
    if [isinstance(_ent, (IncidentPwFem, TransmissionPwFem)) for _ent in self.model_entities]:
            self.resfile.write("absorption [no unity]\n")
    if [isinstance(_ent, (IncidentPwFem)) for _ent in self.model_entities]:
            self.resfile.write("|R| [no unity]\n")
    if [isinstance(_ent, (TransmissionPwFem)) for _ent in self.model_entities]:
            self.resfile.write("|T| [no unity]\n")

def write_out_files(self):

    self.outfile.write("{:.12e}\t".format(self.current_frequency))
    if [isinstance(_ent, (IncidentPwFem, TransmissionPwFem)) for _ent in self.model_entities]:
        self.outfile.write("{:.12e}\t".format(self.abs))
    if [isinstance(_ent, (IncidentPwFem)) for _ent in self.model_entities]:
        self.outfile.write("{:.12e}\t".format(self.modulus_reflex))
    if [isinstance(_ent, (TransmissionPwFem)) for _ent in self.model_entities]:
        self.outfile.write("{:.12e}\t".format(self.modulus_reflex))
    self.outfile.write("\n")


'''
Created on 26. nov. 2014
@author: PPAR
'''
import time, statistics, os
import errno
import excel_manager
import tempfile

class OutputManager(object):
    def __init__(self, working_folder=tempfile.gettempdir() + "/inclinometer/",
                 working_filename="inclinometer_data",
                 working_excel_sheet="data"):
        try:
            os.mkdir(working_folder)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(working_folder):
                pass
            else:
                raise
        self.working_folder = working_folder
        self.working_filename = working_filename
        self.working_excel_sheet = working_excel_sheet

        self.filename_raw_output = working_folder + working_filename + "_" + \
                                   time.strftime("%Y%m%d", time.localtime()) + "_RAW.txt"
        self.filename_output = working_folder + working_filename + "_" + \
                               time.strftime("%Y%m%d", time.localtime()) + ".txt"
        self.excel_manager = excel_manager.ExcelManager(working_folder, working_filename, working_excel_sheet)

    def _processData(self, data):
        result = {}

        for key in data.keys():
            if key != "timestamp":
                result[str(key)] = {"mean": statistics.mean(data[str(key)]), "median": statistics.median(data[str(key)]), "stdev": statistics.stdev(data[str(key)])}
        return result

    def saveData(self, acc_data, ang_data, mag_data, data_type):
        timestamp = acc_data["timestamp"]
        proc_acc_data = self._processData(acc_data)
        proc_ang_data = self._processData(ang_data)
        proc_mag_data = self._processData(mag_data)


        # Save processed data as txt file
        # 1. Open the file
        # 2. Append the new data
        # 3. Close the file
        does_file_exist =  os.path.isfile(self.filename_output)
        self.output_file = open(self.filename_output, mode='a+')

        if(not does_file_exist):
            self.output_file.write("|---------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|\n")
            self.output_file.write("|-     Timestamp     -|-       Data      -|-       AccX      -|-       AccY      -|-       AccZ      -|-       AngX      -|-       AngY      -|-       AngZ      -|-       MagX      -|-       MagY      -|-       MagZ      -|\n")
            self.output_file.write("|-  yymmdd_hhmmss    -|-     (h), (m)    -|-        (g)      -|-        (g)      -|-        (g)      -|-(Degrees per sec)-|-(Degrees per sec)-|-(Degrees per sec)-|-      (Gauss)    -|-      (Gauss)    -|-      (Gauss)    -|\n")
            self.output_file.write("|---------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|\n")

        self.output_file.write("|- %15s -|- %15s -|" % (timestamp, data_type)) #time stamp & data type(measurement or horizon)
        self.output_file.write("- %15f -|- %15f -|- %15f -|" % (proc_acc_data["acc_X"]["mean"], proc_acc_data["acc_Y"]["mean"], proc_acc_data["acc_Z"]["mean"])) #Accelerometer data
        self.output_file.write("- %15f -|- %15f -|- %15f -|" % (proc_ang_data["ang_X"]["mean"], proc_ang_data["ang_Y"]["mean"], proc_ang_data["ang_Z"]["mean"])) #Gyroscope data
        self.output_file.write("- %15f -|- %15f -|- %15f -|\n" % (proc_mag_data["X"]["mean"], proc_mag_data["Y"]["mean"], proc_mag_data["Z"]["mean"])) #Magnetic field data

        self.output_file.close()
        # End

        # Save processed data as excel file
        self.excel_manager.write_data(timestamp, data_type,
                                      acc_data = [proc_acc_data["acc_X"]["mean"], proc_acc_data["acc_Y"]["mean"], proc_acc_data["acc_Z"]["mean"]],
                                      gyro_data = [proc_ang_data["ang_X"]["mean"], proc_ang_data["ang_Y"]["mean"], proc_ang_data["ang_Z"]["mean"]],
                                      magn_data = [proc_mag_data["X"]["mean"], proc_mag_data["Y"]["mean"], proc_mag_data["Z"]["mean"]])


        # Save raw data as txt file
        # 1. Open the file
        # 2. Append the new data
        # 3. Close the file

        self.raw_output_file = open(self.filename_raw_output, mode='a+')

        self.raw_output_file.write("---------------------------------------------------------------------------------------------------------------------------------------------")
        self.raw_output_file.write(timestamp + ", " + data_type + ", [acc_X(" + str(len(acc_data["acc_X"])) + "): " + ", ".join(map(lambda x: str(x), acc_data["acc_X"])) + "]\n")
        self.raw_output_file.write(timestamp + ", " + data_type + ", [acc_Y(" + str(len(acc_data["acc_Y"])) + "): " + ", ".join(map(lambda x: str(x), acc_data["acc_Y"])) + "]\n")
        self.raw_output_file.write(timestamp + ", " + data_type + ", [acc_Z(" + str(len(acc_data["acc_Z"])) + "): " + ", ".join(map(lambda x: str(x), acc_data["acc_Z"])) + "]\n")
        self.raw_output_file.write("[acc_X(mean, median, stdev): (%f, %f, %f)]\n" % (proc_acc_data["acc_X"]["mean"], proc_acc_data["acc_X"]["median"], proc_acc_data["acc_X"]["stdev"]))
        self.raw_output_file.write("[acc_Y(mean, median, stdev): (%f, %f, %f)]\n" % (proc_acc_data["acc_Y"]["mean"], proc_acc_data["acc_Y"]["median"], proc_acc_data["acc_Y"]["stdev"]))
        self.raw_output_file.write("[acc_Z(mean, median, stdev): (%f, %f, %f)]\n" % (proc_acc_data["acc_Z"]["mean"], proc_acc_data["acc_Z"]["median"], proc_acc_data["acc_Z"]["stdev"]))
        self.raw_output_file.write("\n")

        self.raw_output_file.write(timestamp + ", " + data_type + ", [ang_X(" + str(len(ang_data["ang_X"])) + "): " + ", ".join(map(lambda x: str(x), ang_data["ang_X"])) + "]\n")
        self.raw_output_file.write(timestamp + ", " + data_type + ", [ang_Y(" + str(len(ang_data["ang_Y"])) + "): " + ", ".join(map(lambda x: str(x), ang_data["ang_Y"])) + "]\n")
        self.raw_output_file.write(timestamp + ", " + data_type + ", [ang_Z(" + str(len(ang_data["ang_Z"])) + "): " + ", ".join(map(lambda x: str(x), ang_data["ang_Z"])) + "]\n")
        self.raw_output_file.write("[ang_X(mean, median, stdev): (%f, %f, %f)]\n" % (proc_ang_data["ang_X"]["mean"], proc_ang_data["ang_X"]["median"], proc_ang_data["ang_X"]["stdev"]))
        self.raw_output_file.write("[ang_Y(mean, median, stdev): (%f, %f, %f)]\n" % (proc_ang_data["ang_Y"]["mean"], proc_ang_data["ang_Y"]["median"], proc_ang_data["ang_Y"]["stdev"]))
        self.raw_output_file.write("[ang_Z(mean, median, stdev): (%f, %f, %f)]\n" % (proc_ang_data["ang_Z"]["mean"], proc_ang_data["ang_Z"]["median"], proc_ang_data["ang_Z"]["stdev"]))
        self.raw_output_file.write("\n")

        self.raw_output_file.write(timestamp + ", " + data_type + ", [mag_X(" + str(len(mag_data["X"])) + "): " + ", ".join(map(lambda x: str(x), mag_data["X"])) + "]\n")
        self.raw_output_file.write(timestamp + ", " + data_type + ", [mag_Y(" + str(len(mag_data["Y"])) + "): " + ", ".join(map(lambda x: str(x), mag_data["Y"])) + "]\n")
        self.raw_output_file.write(timestamp + ", " + data_type + ", [mag_Z(" + str(len(mag_data["Z"])) + "): " + ", ".join(map(lambda x: str(x), mag_data["Z"])) + "]\n")
        self.raw_output_file.write("[mag_X(mean, median, stdev): (%f, %f, %f)]\n" % (proc_mag_data["X"]["mean"], proc_mag_data["X"]["median"], proc_mag_data["X"]["stdev"]))
        self.raw_output_file.write("[mag_Y(mean, median, stdev): (%f, %f, %f)]\n" % (proc_mag_data["Y"]["mean"], proc_mag_data["Y"]["median"], proc_mag_data["Y"]["stdev"]))
        self.raw_output_file.write("[mag_Z(mean, median, stdev): (%f, %f, %f)]\n" % (proc_mag_data["Z"]["mean"], proc_mag_data["Z"]["median"], proc_mag_data["Z"]["stdev"]))
        self.raw_output_file.write("---------------------------------------------------------------------------------------------------------------------------------------------\n\n")

        self.raw_output_file.close()
        # End

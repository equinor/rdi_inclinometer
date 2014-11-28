'''
Created on 26. nov. 2014
@author: PPAR
'''
import time, statistics

class OutputManager(object):
    filename_root = "inclinometer_data"
    def __init__(self):
        self.filename_raw_output = self.filename_root + "_" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + "_RAW.txt"
        self.filename_output = self.filename_root + "_" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".txt"
        self.raw_output_file = open(self.filename_raw_output, mode='w+')
        
        
        self.output_file = open(self.filename_output, mode='w+')
        self.output_file.write("|---------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|\n")
        self.output_file.write("|-     Timestamp     -|-       AccX      -|-       AccY      -|-       AccZ      -|-       AngX      -|-       AngY      -|-       AngZ      -|\n\n")
        self.output_file.write("|---------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|\n")
    
    def _processData(self, data):
        result = {}
        
        for key in data.keys():
            if key != "timestamp":
                result[str(key)] = {"mean": statistics.mean(data[str(key)]), "median": statistics.median(data[str(key)]), "stdev": statistics.stdev(data[str(key)])}        
        return result
        
    
    def saveData(self, acc_data, ang_data):
        timestamp = acc_data["timestamp"]
        proc_acc_data = self._processData(acc_data)
        proc_ang_data = self._processData(ang_data)
        
        # Save acc_data
        self.output_file.write("|- %15s -|- %15f -|- %15f -|- %15f -|" % (timestamp, proc_acc_data["acc_X"]["mean"], proc_acc_data["acc_Y"]["mean"], proc_acc_data["acc_Z"]["mean"]))
        self.output_file.write("- %15f -|- %15f -|- %15f -|\n" % (proc_ang_data["ang_X"]["mean"], proc_ang_data["ang_Y"]["mean"], proc_ang_data["ang_Z"]["mean"]))
        
        # Save the raw acc_data
        self.raw_output_file.write(timestamp + ", " + "[acc_X(" + str(len(acc_data["acc_X"])) + "): " + ", ".join(map(lambda x: str(x), acc_data["acc_X"])) + "]\n")
        self.raw_output_file.write(timestamp + ", " + "[acc_Y(" + str(len(acc_data["acc_Y"])) + "): " + ", ".join(map(lambda x: str(x), acc_data["acc_Y"])) + "]\n")
        self.raw_output_file.write(timestamp + ", " + "[acc_Z(" + str(len(acc_data["acc_Z"])) + "): " + ", ".join(map(lambda x: str(x), acc_data["acc_Z"])) + "]\n")
        self.raw_output_file.write("[acc_X(mean, median, stdev): (%f, %f, %f)]\n" % (proc_acc_data["acc_X"]["mean"], proc_acc_data["acc_X"]["median"], proc_acc_data["acc_X"]["stdev"]))
        self.raw_output_file.write("[acc_Y(mean, median, stdev): (%f, %f, %f)]\n" % (proc_acc_data["acc_Y"]["mean"], proc_acc_data["acc_Y"]["median"], proc_acc_data["acc_Y"]["stdev"]))
        self.raw_output_file.write("[acc_Z(mean, median, stdev): (%f, %f, %f)]\n" % (proc_acc_data["acc_Z"]["mean"], proc_acc_data["acc_Z"]["median"], proc_acc_data["acc_Z"]["stdev"]))
        self.raw_output_file.write("\n")
        
        
        
    
    def closeOutputFiles(self):
        self.raw_output_file.close()
        self.output_file.close()
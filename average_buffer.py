from __future__ import division

import os
from os import listdir
from os.path import isfile, join
from numpy import matrix


class SAXS_subtractor(object):

    def __init__(self, file_buffer):

        self.file_buffer = file_buffer
        self.q_buffer = []
        self.intensity_buffer = []
        self.Error_buffer = []


    def file_name_dissector(self,*args):

        if len(args) == 1:
            self.file_buffer = args[0]

        if self.file_buffer.split('img_'):    # files collected at EMBL e.g. img_0008_00001.dat

            self.ID_of_buffer = self.file_buffer.split("img_")[1].split("_")[0]
            self.name_and_ID_buffer = 'img_%s'%self.ID_of_buffer
            self.number_of_buffer = self.file_buffer.split('.dat')[0].split('_')[-1]
            test_name = 'img_%s_%s.dat'%(self.ID_of_buffer,self.number_of_buffer)

            if test_name != self.file_buffer:
                print 'file name: %s but constructed name: %s instead'%(test_name,self.file_buffer)

        return self.name_and_ID_buffer

    def count_files(self,*args):

        if len(args) == 0:
            self.file_name_dissector()

        if len(args) == 1:
            self.file_buffer = args[0]
            self.file_name_dissector(self.file_buffer)

        mypath = os.getcwd()
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        self.list_of_files = []
        for element in onlyfiles:
            if len(element.split(self.name_and_ID_buffer)) > 1:
                self.list_of_files.append(element)

        self.number_of_files = len(self.list_of_files)

        return self.list_of_files

    def file_reader(self,*args):

        if len(args) == 1:

            self.name_of_buffer = args[0].split("img_")[1].split("_")[0]
            self.lines_buffer = open(args[0]).readlines()
            return self.lines_buffer


        if len(args) == 0:

            self.name_of_buffer = self.file_buffer.split("img_")[1].split("_")[0]
            self.lines_buffer = open(self.file_buffer).readlines()

    def columns_extractor(self,*args):

        if len(args) == 1:
            self.lines_buffer = self.file_reader(args[0])

        for i,line in enumerate(self.lines_buffer):

            if "Sample:" in self.lines_buffer[i]:
                start = i

            if "creator: radaver" in self.lines_buffer[i]:
                end = i
                break

        self.lines_buffer = self.lines_buffer[start+1:end]

    def buffer_column_arranger(self,*args):

        if len(args) == 1:
            self.file_reader(args[0])
            self.columns_extractor(args[0])

        if len(args) == 0:

            self.file_reader()
            self.columns_extractor()

        for i,line in enumerate(self.lines_buffer):

            self.q_buffer.append(self.lines_buffer[i].split("  ")[1])
            self.intensity_buffer.append(float(self.lines_buffer[i].split("  ")[2]))
            self.Error_buffer.append(self.lines_buffer[i].split("  ")[3].split("\n")[0])

        return self.q_buffer, self.intensity_buffer, self.Error_buffer

    def main(self):

        self.file_reader()
        self.columns_extractor()
        self.buffer_column_arranger()
        self.file_name_dissector()
        self.count_files()



class another_class():

    def __init__(self, file_buffer):
            self.file_buffer = file_buffer

    def print_files(self,file_buffer):

        self.file_buffer = file_buffer

        for number in range(5):
                if number < 100:
                    index_file = '000'+str(number)
                if number > 100:
                    index_file = '00' + str(number)
                if len(index_file) == 4:
                    index_file = '0'+index_file

                name_of_sample_template = self.file_buffer.split(".dat")[0].split("_000")[0]+"_"
                name_sample = name_of_sample_template+index_file+".dat"

                SAXS_subtractor(name_sample).main()

    def average_intensities(self):

        first_buffer_file = self.file_buffer
        list = SAXS_subtractor(first_buffer_file).count_files()
        list_all_intensities = []
        for content in list:
            intensities = SAXS_subtractor(content).buffer_column_arranger()[1]
            list_all_intensities.append(intensities)

        list_not_usable = []
        first_event = 0

        length_columns_buffer = len(list_all_intensities[0])

        for i,it in enumerate(list_all_intensities):

            if len(it) != length_columns_buffer:
                if first_event == 0:
                    end_index = i

                list_not_usable.append(list[i])

        print 'Not usable files: %s'%list_not_usable

        #print list_all_intensities
        avg = [float(sum(col)/len(col)) for col in zip(*list_all_intensities[0:end_index-1])]

        if len(avg) != length_columns_buffer:
            print 'Error: Length of average is %i and should be %i'%(len(avg),length_columns_buffer)

        return avg

#average = another_class('img_0008_00001.dat').average_intensities()


class sample_average_subtractor(object):

    def __init__(self, file_sample):
        self.file_sample = file_sample

    def count_files_sample(self):

        self.name_and_ID_buffer = SAXS_subtractor('').file_name_dissector(self.file_sample)
        mypath = os.getcwd()
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        self.list_of_files = []
        for element in onlyfiles:
            if len(element.split(self.name_and_ID_buffer)) > 1:
                self.list_of_files.append(element)

        self.number_of_files = len(self.list_of_files)

        return self.list_of_files

    def get_intensities(self,*args):

        file_name = self.file_sample
        self.intensities = SAXS_subtractor('').buffer_column_arranger(file_name)
        return self.intensities


    def buffer_namer(self, three_digits_sample):


        #print three_digits_sample
        three_digits_buffer = int(three_digits_sample)-1
        #print three_digits_buffer
        #print 'here'

        if len(str(three_digits_buffer)) == 1:
            three_digits_buffer = '00%i'%three_digits_buffer
        if len(str(three_digits_buffer)) == 2:
            three_digits_buffer = '00%i'%three_digits_buffer

        name_of_buffer = 'img_0%s_00001.dat'%three_digits_buffer
        return name_of_buffer


    def create_directory(self):
        #reference_sample_number = 'xxxxx'
        reference_sample_number = SAXS_subtractor(self.file_sample).file_name_dissector()
        self.one_path = "%s/Rg_%s"%(os.getcwd(),reference_sample_number)
        if not os.path.exists(self.one_path):
            os.system('mkdir Rg_%s'%(reference_sample_number))   # work with the problem of space

    def subtract_sample_minus_buffer(self,*args):

        list_files_sample = SAXS_subtractor('').count_files(self.file_sample)
        self.create_directory()

        #print self.file_sample

        first = 0
        for item in list_files_sample:
            print item


            q_sample, intensity_sample, error_sample = sample_average_subtractor(item).get_intensities()

            #q_sample = sample_average_subtractor(item).get_intensities()[0]
            #intensity_sample = sample_average_subtractor(item).get_intensities()[1]
            #error_sample = sample_average_subtractor(item).get_intensities()[2]

            name_of_buffer = self.buffer_namer(args[0])

            if first == 0:
                average = another_class(name_of_buffer).average_intensities()
                first = 1

            a = matrix(intensity_sample)
            b = matrix(average)

            if a.shape == b.shape:
                self.c = (a - b)

            subtracted_file = open("%s/subtracted_%s_minus_average.dat"%(self.one_path,item),"w")

            k = 0

            c_list = self.c.tolist()


            for i in c_list:
                for order, element in enumerate(i):
                    #print element

                    #print i

                    if k == 0:
                        subtracted_file.write("# file buffer: s subtracted from file sample: s\n")#%(file_buffer,file_mostra))
                        subtracted_file.write("# q(1/A)      \tColumn      \tError       \t\n")

                    try:
                        subtracted_file.write("%s\t%s  \t%s\n"%(q_sample[order],element,error_sample[order]))
                        k = k + 1

                    except:

                        pass
            subtracted_file.close()


    def create_directory(self):
        #reference_sample_number = 'xxxxx'
        reference_sample_number = SAXS_subtractor(self.file_sample).file_name_dissector()
        self.one_path = "%s/Rg_%s"%(os.getcwd(),reference_sample_number)
        if not os.path.exists(self.one_path):
            os.system('mkdir Rg_%s'%(reference_sample_number))   # work with the problem of space



    def average_subtracted_writer(self):
        pass







if __name__ == '__main__':

    three_digits_sample = (raw_input('Introduce three digits of a sample e.g. 009 for img_0009_00001.dat\n'))
    name_of_sample = 'img_0%s_00001.dat'%three_digits_sample

    name_of_buffer = sample_average_subtractor(name_of_sample).buffer_namer(three_digits_sample)

    list_files_sample = sample_average_subtractor(name_of_sample).subtract_sample_minus_buffer(three_digits_sample)
    average = another_class(name_of_buffer).average_intensities()

    sample_average_subtractor(name_of_sample).create_directory()
    sample_average_subtractor(name_of_sample).average_subtracted_writer()


    #print average

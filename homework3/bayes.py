import sys
from types import *

diseaseName = []
diseaseFeatureNumber = []
diseaseP = []
diseaseFeature = []
diseaseP_T = []
diseaseP_F = []
patientList = []


inputFile = open(sys.argv[2], "r")
slash = sys.argv[2].rfind('/')
str = sys.argv[2][slash+1:]
insert = str.rfind('.txt')
str = str[:insert]+"_inference"+'.txt'
ouputFile = open(str, "w")

diseaseNumber, patientNumber = [int(x) for x in inputFile.readline().split()]

for diseaseIndex in range(0, diseaseNumber, 1):
    line1 = inputFile.readline().split()
    diseaseName.append(line1[0])
    diseaseFeatureNumber.append(int(line1[1]))
    diseaseP.append(float(line1[2]))
    diseaseFeature.append(eval(inputFile.readline()))
    diseaseP_T.append(eval(inputFile.readline()))
    diseaseP_F.append(eval(inputFile.readline()))


def q1(patientFeatureList, diseaseIndex):
    p_f_d = 1.0
    p_f = 1.0
    for featureIndex in range(0, diseaseFeatureNumber[diseaseIndex], 1):
        if patientFeatureList[featureIndex] == "T":
            p_f_d = p_f_d*diseaseP_T[diseaseIndex][featureIndex]
            p_f = p_f*diseaseP_F[diseaseIndex][featureIndex]
        elif patientFeatureList[featureIndex] == "F":
            p_f_d = p_f_d*(1-diseaseP_T[diseaseIndex][featureIndex])
            p_f = p_f*(1-diseaseP_F[diseaseIndex][featureIndex])

    return (p_f_d*diseaseP[diseaseIndex]/(p_f_d*diseaseP[diseaseIndex]+p_f*(1-diseaseP[diseaseIndex])), p_f_d, p_f)


def q2(start, diseaseIndex, patientFeatureList, p_f_d, p_f):
    for index in range(start, diseaseFeatureNumber[diseaseIndex], 1):
        if patientFeatureList[index] == "U":
            result = []
            T_temp = q2(index+1, diseaseIndex, patientFeatureList, p_f_d*diseaseP_T[diseaseIndex][index], p_f*diseaseP_F[diseaseIndex][index])
            F_temp = q2(index+1, diseaseIndex, patientFeatureList, p_f_d*(1-diseaseP_T[diseaseIndex][index]), p_f*(1-diseaseP_F[diseaseIndex][index]))
            if T_temp[0] < F_temp[0]:
                result.append(T_temp[0])
            else:
                result.append(F_temp[0])
            if T_temp[1] > F_temp[1]:
                result.append(T_temp[1])
            else:
                result.append(F_temp[1])
            return result
    return [p_f_d*diseaseP[diseaseIndex]/(p_f_d*diseaseP[diseaseIndex]+p_f*(1-diseaseP[diseaseIndex])),p_f_d*diseaseP[diseaseIndex]/(p_f_d*diseaseP[diseaseIndex]+p_f*(1-diseaseP[diseaseIndex]))]


def q3(diseaseIndex, patientFeatureList, p_f_d, p_f):
    standard = p_f_d*diseaseP[diseaseIndex]/(p_f_d*diseaseP[diseaseIndex]+p_f*(1-diseaseP[diseaseIndex]))
    resultTemp = ["", 0.0, "", 0.0]
    result = ["none", "N", "none", "N"]
    for index in range(0, diseaseFeatureNumber[diseaseIndex], 1):
        if patientFeatureList[index] == "U":
            T_temp = p_f_d*diseaseP_T[diseaseIndex][index]*diseaseP[diseaseIndex]/(p_f_d*diseaseP_T[diseaseIndex][index]*diseaseP[diseaseIndex]+p_f*diseaseP_F[diseaseIndex][index]*(1-diseaseP[diseaseIndex])) - standard
            F_temp = p_f_d*(1-diseaseP_T[diseaseIndex][index])*diseaseP[diseaseIndex]/(p_f_d*(1-diseaseP_T[diseaseIndex][index])*diseaseP[diseaseIndex]+p_f*(1-diseaseP_F[diseaseIndex][index])*(1-diseaseP[diseaseIndex])) - standard
            if T_temp <= F_temp:
                if T_temp < resultTemp[3]:
                    resultTemp[2] = diseaseFeature[diseaseIndex][index]
                    resultTemp[3] = T_temp
                    result[2] = diseaseFeature[diseaseIndex][index]
                    result[3] = "T"
                elif (T_temp == resultTemp[3])and(resultTemp[2] != ""):
                    if diseaseFeature[diseaseIndex][index] < resultTemp[2]:
                        resultTemp[2] = diseaseFeature[diseaseIndex][index]
                        resultTemp[3] = T_temp
                        result[2] = diseaseFeature[diseaseIndex][index]
                        result[3] = "T"
                if F_temp > resultTemp[1]:
                    resultTemp[0] = diseaseFeature[diseaseIndex][index]
                    resultTemp[1] = F_temp
                    result[0] = diseaseFeature[diseaseIndex][index]
                    result[1] = "F"
                elif (F_temp == resultTemp[1])and(resultTemp[0] != ""):
                    if diseaseFeature[diseaseIndex][index] < resultTemp[0]:
                        resultTemp[0] = diseaseFeature[diseaseIndex][index]
                        resultTemp[1] = F_temp
                        result[0] = diseaseFeature[diseaseIndex][index]
                        result[1] = "F"
            else:
                if T_temp > resultTemp[1]:
                    resultTemp[0] = diseaseFeature[diseaseIndex][index]
                    resultTemp[1] = T_temp
                    result[0] = diseaseFeature[diseaseIndex][index]
                    result[1] = "T"
                elif (T_temp == resultTemp[1])and(resultTemp[0] != ""):
                    if diseaseFeature[diseaseIndex][index] < resultTemp[0]:
                        resultTemp[0] = diseaseFeature[diseaseIndex][index]
                        resultTemp[1] = T_temp
                        result[0] = diseaseFeature[diseaseIndex][index]
                        result[1] = "T"
                if F_temp < resultTemp[3]:
                    resultTemp[2] = diseaseFeature[diseaseIndex][index]
                    resultTemp[3] = F_temp
                    result[2] = diseaseFeature[diseaseIndex][index]
                    result[3] = "F"
                elif (F_temp == resultTemp[3])and(resultTemp[2] != ""):
                    if diseaseFeature[diseaseIndex][index] < resultTemp[2]:
                        resultTemp[2] = diseaseFeature[diseaseIndex][index]
                        resultTemp[3] = F_temp
                        result[2] = diseaseFeature[diseaseIndex][index]
                        result[3] = "F"
    return result

for patientIndex in range(0, patientNumber, 1):
    Q1_Result = {}
    Q2_Result = {}
    Q3_Result = {}
    for diseaseIndex in range(0, diseaseNumber, 1):
        patientFeatureList = eval(inputFile.readline())
        Q1_result_temp, p_f_d, p_f = q1(patientFeatureList, diseaseIndex)
        Q1_Result[diseaseName[diseaseIndex]] = "{0:.4f}".format(round(Q1_result_temp, 4))
        #q2
        Q2_result_temp = q2(0, diseaseIndex, patientFeatureList, p_f_d, p_f)
        Q2_Result[diseaseName[diseaseIndex]] = ["{0:.4f}".format(round(Q2_result_temp[0], 4)), "{0:.4f}".format(round(Q2_result_temp[1], 4))]
        #q3
        Q3_Result[diseaseName[diseaseIndex]] = q3(diseaseIndex,patientFeatureList,p_f_d,p_f)
    ouputFile.write("Patient-"+repr(patientIndex+1)+":"+"\n")
    ouputFile.write(repr(Q1_Result)+"\n")
    ouputFile.write(repr(Q2_Result)+"\n")
    ouputFile.write(repr(Q3_Result)+"\n")


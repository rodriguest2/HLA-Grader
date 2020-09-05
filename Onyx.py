#import sys
#sys.setrecursionlimit(10**10)
import numpy as np
import pandas as pd
from tkinter import *
#from PIL import ImageTk, Image
from tkinter import filedialog



#A cregs
creg_a1 = ['A36','A1','A3','A80','A11','A30','A31','A29']
creg_a2 = ['A30','A31','A29','A43','A33','A32','A74','A19']
creg_a3 = ['A11','A26','A66','A34','A25','A69','A68','A28','A33','A32','A19','A74']
creg_a4 = ['A23','A24','A2403','A9','A210','A203','A2','A69','A68','A28','B57','B58','B17']
creg_a5 = ['A26','A66','A34','A25','A10']

#B cregs
creg_b1 = ['B5','B51','B52','B5102','B5103','B0802','B0803','B13','B17','B57','B58','B1809','B27','B37','B38','B16','B4412','B47','B49','B21','B53','B5607','B59','B63','B15','B67','B77','A9','A23','A24','A25','A10','A32','A19']
creg_b2 = ['B7','B703','B8','B1309','B18','B2706','B2717','B2718','B35','B39','B16','B3901','B3902','B4005','B41','B42','B4406','B4409','B44','B45','B12','B46','B4702','B48','B50','B21','B54','B22','B55','B56','B60','B40','B61','B62','B15','B64','B14','B65','B67','B71','B70','B72','B73','B75','B78','B81','B82']

#all cregs
all_cregs = creg_a1+creg_a2+creg_a3+creg_a4+creg_a5+creg_b1+creg_b2

#A relational antigens
aby_A9 = ['A2403','A9']
aby_A10 = ['A25','A10']
aby_A19 = ['A32','A19']
aby_A28 = ['A69','A68','A28']

#B relational antigens
aby_B5 = ['B5','B51','B52','B5102','B5103']
aby_B12 = ['B44','B12','B45']
aby_B14 = ['B14','B64','B65']
aby_B15 = ['B15','B63','B77']
aby_B16 = ['B38','B16','B39']
aby_B17 = ['B17','B57','B58']
aby_B21 = ['B49','B21','B50']
aby_B22 = ['B22','B55','B56','B54']
aby_B40 = ['B40','B60','B61']
aby_B70 = ['B70','B71','B72']

#HLA Platelet Grades
grades = {
    'A':['match','match','match','match'],
    'B1U':['match','match','match','unknown'],
    'B1X':['cross','match','match','match'],
    'B2U':['match','match','unknown','unknown'],
    'B1U1X':['cross','match','match','unknown'],
    'B2X':['cross','cross','match','match'],
    'B2U1X':['cross','match','unknown','unknown'],
    'B1U2X':['cross','cross','match','unknown'],
    'B3X':['cross','cross','cross','match'],
    'B2U2X':['cross','cross','unknown','unknown'],
    'B1U3X':['cross','cross','cross','unknown'],
    'B4X':['cross','cross','cross','cross']
}


def daily_report_reader(HLA_report_file):
    '''
    Opens the HLA daily report excel file and cleans it.
    '''
    df = pd.read_excel(HLA_report_file, usecols = [1,3,6,7,8,9], skiprows = 4)
    df.columns = ['ABORh', 'Unit', 'HLA_A1', 'HLA_A2', 'HLA_B1', 'HLA_B2']
    df['Grade'] = np.nan
    df['Rank'] = np.nan
    df = df.dropna(thresh=4)
    return df


def donor_pool_reader(HLA_donor_pool_file):
    '''
    Opens the HLA donor pool excel file and cleans it.
    '''
    df = pd.read_excel(HLA_donor_pool_file, usecols = [1,2,11], skiprows = 30, skipfooter = 7)
    df.columns = ['Donor', 'Name', 'Type']
    df['HLA_A1'] = np.nan
    df['HLA_A2'] = np.nan
    df['HLA_B1'] = np.nan
    df['HLA_B2'] = np.nan
    df['Grade'] = np.nan
    df['Rank'] = np.nan
    for index, row in df.iterrows():
        fullrow = row[2].split()
        HLA_list = []
        for element in fullrow:
            if element in all_cregs:
                HLA_list.append(element)
        if len(HLA_list) == 4:
            df.loc[index,['HLA_A1']] = HLA_list[0]
            df.loc[index,['HLA_A2']] = HLA_list[1]
            df.loc[index,['HLA_B1']] = HLA_list[2]
            df.loc[index,['HLA_B2']] = HLA_list[3]
        elif len(HLA_list) == 3:
            if HLA_list[0][0] == HLA_list[1][0]:
                df.loc[index,['HLA_A1']] = HLA_list[0]
                df.loc[index,['HLA_A2']] = HLA_list[1]
                df.loc[index,['HLA_B1']] = HLA_list[2]
                df.loc[index,['HLA_B2']] = 'U'
            elif HLA_list[1][0] == HLA_list[2][0]:
                df.loc[index,['HLA_A1']] = HLA_list[0]
                df.loc[index,['HLA_A2']] = 'U'
                df.loc[index,['HLA_B1']] = HLA_list[1]
                df.loc[index,['HLA_B2']] = HLA_list[2]     
        elif len(HLA_list) == 2:
            if HLA_list[0][0] != HLA_list[1][0]:
                df.loc[index,['HLA_A1']] = HLA_list[0]
                df.loc[index,['HLA_A2']] = 'U'
                df.loc[index,['HLA_B1']] = HLA_list[1]
                df.loc[index,['HLA_B2']] = 'U'
            elif HLA_list[0][0] == 'A':
                df.loc[index,['HLA_A1']] = HLA_list[0]
                df.loc[index,['HLA_A2']] = HLA_list[1]
                df.loc[index,['HLA_B1']] = 'U'
                df.loc[index,['HLA_B2']] = 'U'
            elif HLA_list[0][0] == 'B':
                df.loc[index,['HLA_A1']] = 'U'
                df.loc[index,['HLA_A2']] = 'U'
                df.loc[index,['HLA_B1']] = HLA_list[1]
                df.loc[index,['HLA_B2']] = HLA_list[2] 
    df = df.drop(columns=['Type'])
    return df


def patient_HLA(ptA1, ptA2, ptB1, ptB2):
    '''
    Proccesses patient HLA type
    '''   
    A1 = ptA1
    A2 = ptA2
    B1 = ptB1
    B2 = ptB2
    
    #Pt A processing
    if A1 == '':
        A1 = 'U'
    else:
        A1 = 'A' + A1   
    if A2 == '':
        A2 = 'U'
    else:
        A2 = 'A' + A2
    if A1 == A2:
        A2 = 'U' 
        
    #Pt B processing    
    if B1 == '':
        B1 = 'U'
    else:
        B1 = 'B' + B1   
    if B2 == '':
        B2 = 'U'
    else:
        B2 = 'B' + B2    
    if B1 == B2:
        B2 = 'U'
      
    return A1,A2,B1,B2


def donor_HLA(donor_type):
    '''
    Process individual donor HLA types
    '''
    A1 = donor_type[0]
    A2 = donor_type[1]
    B1 = donor_type[2]
    B2 = donor_type[3]
    if A1 == A2:
        A2 = 'U'
    if B1 == B2:
        B2 = 'U' 
    return A1,A2,B1,B2


def cross_reactive_list(patient_type, antibodies):
    '''
    Generate list of cross reactive antigens for A and B alleles
    '''
    A1 = patient_type[0]
    A2 = patient_type[1]
    B1 = patient_type[2]
    B2 = patient_type[3]
    a_cross = []
    b_cross = []
    
    #Cross reactive A type
    if A1 in creg_a1 or A2 in creg_a1:
        a_cross += creg_a1
    if A1 in creg_a2 or A2 in creg_a2:
        a_cross += creg_a2
    if A1 in creg_a3 or A2 in creg_a3:
        a_cross += creg_a3
    if A1 in creg_a4 or A2 in creg_a4 or B1 in creg_a4 or B2 in creg_a4:
        a_cross += creg_a4
    if A1 in creg_a5 or A2 in creg_a5:
        a_cross += creg_a5
        
    #Cross reactive B type
    if A1 in creg_b1 or A2 in creg_b1 or B1 in creg_b1 or B2 in creg_b1:
        b_cross += creg_b1
    if B1 in creg_b2 or B2 in creg_b2:
        b_cross += creg_b2
        
    cregs = set(a_cross+b_cross)
    
    for ab in antibodies:
        if ab in aby_A9:
            for x in aby_A9:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_A10:
            for x in aby_A10:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_A19:
            for x in aby_A19:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_A28:
            for x in aby_A28:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_B5:
            for x in aby_B5:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_B12:
            for x in aby_B12:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_B14:
            for x in aby_B14:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_B15:
            for x in aby_B15:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_B16:
            for x in aby_B16:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_B17:
            for x in aby_B17:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_B21:
            for x in aby_B21:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_B22:
            for x in aby_B22:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_B40:
            for x in aby_B40:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in aby_B70:
            for x in aby_B70:
                try:
                    cregs.remove(x)
                except:
                    pass
        elif ab in cregs:
            try:
                cregs.remove(ab)
            except:
                pass
            
        for pt_allele in patient_type:
            if pt_allele not in cregs:
                cregs.add(pt_allele)
                
    return cregs

def allele_analysis(donor_type, patient_type, cregs):
    '''
    Analyze each individual donor allele to patient's HLA type.
    '''
    graded_type = []
    
    for index,each_type in enumerate(donor_type):
        if each_type == 'U':
            graded_type.append('unknown')
        elif index == 0 or index == 1:
            if each_type == patient_type[0] or each_type == patient_type[1]:
                graded_type.append('match')
            elif each_type in cregs:
                graded_type.append('cross')
            else:
                graded_type.append('no match')
        elif index == 2 or index == 3:
            if each_type == patient_type[2] or each_type == patient_type[3]:
                graded_type.append('match')
            elif each_type in cregs:
                graded_type.append('cross')
            else:
                graded_type.append('no match')
    
    graded_type.sort()
    return graded_type


def HLA_grade(graded_type):
    '''
    Grade each donor based on allele analysis
    '''
    hla_plt_grade = []

    for grade,alleles in grades.items():
        if graded_type == alleles:
            hla_plt_grade.append(grade)
            if grade == 'A':
                hla_plt_grade.append(1)
            elif grade == 'B1U':
                hla_plt_grade.append(2)  
            elif grade == 'B1X':
                hla_plt_grade.append(3) 
            elif grade == 'B2U':
                hla_plt_grade.append(4)
            elif grade == 'B1U1X':
                hla_plt_grade.append(5)
            elif grade == 'B2X':
                hla_plt_grade.append(6)
            elif grade == 'B2U1X':
                hla_plt_grade.append(7)
            elif grade == 'B1U2X':
                hla_plt_grade.append(8)
            elif grade == 'B3X':
                hla_plt_grade.append(9)
            elif grade == 'B2U2X':
                hla_plt_grade.append(10)
            elif grade == 'B1U3X':
                hla_plt_grade.append(11)
            elif grade == 'B4X':
                hla_plt_grade.append(12)
            return hla_plt_grade
    else:
        hla_plt_grade.append('Poor')
        hla_plt_grade.append(13)
        return hla_plt_grade


def daily_grader(file, ptA1, ptA2, ptB1, ptB2, antibodies):
    '''
    Analyze the daily HLA PLT report and produce an excel file with a graded list sorted by HLA grade rank
    '''
    df = daily_report_reader(file)
    excel_df = df
    patient_type = patient_HLA(ptA1, ptA2, ptB1, ptB2)
    cregs = cross_reactive_list(patient_type, antibodies)
    for index, row in df.iterrows():
        donor_type = []
        graded_type = []
        donor_type = (row['HLA_A1'], row['HLA_A2'], row['HLA_B1'], row['HLA_B2'])
        donor_type = donor_HLA(donor_type)
        graded_type = allele_analysis(donor_type, patient_type, cregs)
        hla_plt_grade = HLA_grade(graded_type)
        excel_df.loc[index,['Grade']] = hla_plt_grade[0]
        excel_df.loc[index,['Rank']] = hla_plt_grade[1]
    excel_df = excel_df.sort_values('Rank', ascending = True)
    return excel_df


def donor_pool_grader(file, ptA1, ptA2, ptB1, ptB2, antibodies):
    '''
    Analyze the HLA donor pool and produce an excel file with a graded list sorted by HLA grade rank
    '''
    df = donor_pool_reader(file)
    excel_df = df
    patient_type = patient_HLA(ptA1, ptA2, ptB1, ptB2)
    cregs = cross_reactive_list(patient_type, antibodies)
    for index, row in df.iterrows():
        donor_type = []
        graded_type = []
        donor_type = (row['HLA_A1'], row['HLA_A2'], row['HLA_B1'], row['HLA_B2'])
        donor_type = donor_HLA(donor_type)
        graded_type = allele_analysis(donor_type, patient_type, cregs)
        hla_plt_grade = HLA_grade(graded_type)
        excel_df.loc[index,['Grade']] = hla_plt_grade[0]
        excel_df.loc[index,['Rank']] = hla_plt_grade[1]
    excel_df = excel_df.sort_values('Rank', ascending = True)
    return excel_df





'''
#####################################GUI#####################################
'''

onyx = Tk()
onyx.title("Onyx")
onyx.resizable(width = False, height = False)
onyx.iconbitmap('Doberman_icon.ico')

fr1 = Frame(
        onyx,
        bg = '#0f0f0f',
        )
fr1.pack(padx = 3, pady = 3)

'''
################################HLA Grader################################
'''
def HLA_grader():
    HLA_window = Toplevel(onyx)
    HLA_window.title("HLA Grader")
    HLA_window.resizable(width = False, height = False)
    HLA_window.iconbitmap('Doberman_icon.ico')
    
    fr1 = Frame(
            HLA_window,
            bg = '#0f0f0f',
            )
    lab1 = Label(
            master = fr1,
            text = 'HLA-A:',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'e',
            width = 10
            )
    lab2 = Label(
            master = fr1,
            text = 'HLA-A:',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'e',
            width = 10
            )
    lab3 = Label(
            master = fr1,
            text = 'HLA-B:',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'e',
            width = 10
            )
    lab4 = Label(
            master = fr1,
            text = 'HLA-B:',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'e',
            width = 10
            )
    lab5 = Label(
            master = fr1,
            text = 'Patient HLA Antibodies',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            width = 20
            )
    lab6 = Label(
            master = fr1,
            text = 'Daily HLA:',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'e',
            width = 15
            )
    '''lab7 = Label(
            master = fr1,
            text = 'Donor Pool Report:',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'e',
            width = 15
            )'''
    ent1 = Entry(
            master = fr1,
            font = ('Abadi', 12),
            fg = '#0f0f0f',
            bg = '#b87333',
            width = 5,
            )
    ent2 = Entry(
            master = fr1,
            font = ('Abadi', 12),
            fg = '#0f0f0f',
            bg = '#b87333',
            width = 5
            )
    ent3 = Entry(
            master = fr1,
            font = ('Abadi', 12),
            fg = '#0f0f0f',
            bg = '#b87333',
            width = 5
            )
    ent4 = Entry(
            master = fr1,
            font = ('Abadi', 12),
            fg = '#0f0f0f',
            bg = '#b87333',
            width = 5
            )
    var1 = StringVar()
    cb1 = Checkbutton(
            master = fr1,
            text = 'A1',
            variable = var1,
            onvalue = 'A1',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var2 = StringVar()
    cb2 = Checkbutton(
            master = fr1,
            text = 'A2',
            variable = var2,
            onvalue = 'A2',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var3 = StringVar()
    cb3 = Checkbutton(
            master = fr1,
            text = 'A3',
            variable = var3,
            onvalue = 'A3',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var4 = StringVar()
    cb4 = Checkbutton(
            master = fr1,
            text = 'A9',
            variable = var4,
            onvalue = 'A9',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var5 = StringVar()
    cb5 = Checkbutton(
            master = fr1,
            text = 'A10',
            variable = var5,
            onvalue = 'A10',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var6 = StringVar()
    cb6 = Checkbutton(
            master = fr1,
            text = 'A11',
            variable = var6,
            onvalue = 'A11',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var7 = StringVar()
    cb7 = Checkbutton(
            master = fr1,
            text = 'A19',
            variable = var7,
            onvalue = 'A19',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var8 = StringVar()
    cb8 = Checkbutton(
            master = fr1,
            text = 'A23',
            variable = var8,
            onvalue = 'A23',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var9 = StringVar()
    cb9 = Checkbutton(
            master = fr1,
            text = 'A24',
            variable = var9,
            onvalue = 'A24',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var10 = StringVar()
    cb10 = Checkbutton(
            master = fr1,
            text = 'A25',
            variable = var10,
            onvalue = 'A25',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var11 = StringVar()
    cb11 = Checkbutton(
            master = fr1,
            text = 'A26',
            variable = var11,
            onvalue = 'A26',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var12 = StringVar()
    cb12 = Checkbutton(
            master = fr1,
            text = 'A28',
            variable = var12,
            onvalue = 'A28',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var13 = StringVar()
    cb13 = Checkbutton(
            master = fr1,
            text = 'A29',
            variable = var13,
            onvalue = 'A29',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var14 = StringVar()
    cb14 = Checkbutton(
            master = fr1,
            text = 'A30',
            variable = var14,
            onvalue = 'A30',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var15 = StringVar()
    cb15 = Checkbutton(
            master = fr1,
            text = 'A31',
            variable = var15,
            onvalue = 'A31',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var16 = StringVar()
    cb16 = Checkbutton(
            master = fr1,
            text = 'A32',
            variable = var16,
            onvalue = 'A32',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var17 = StringVar()
    cb17 = Checkbutton(
            master = fr1,
            text = 'A33',
            variable = var17,
            onvalue = 'A33',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var18 = StringVar()
    cb18 = Checkbutton(
            master = fr1,
            text = 'A34',
            variable = var18,
            onvalue = 'A34',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var19 = StringVar()
    cb19 = Checkbutton(
            master = fr1,
            text = 'A36',
            variable = var19,
            onvalue = 'A36',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var20 = StringVar()
    cb20 = Checkbutton(
            master = fr1,
            text = 'A43',
            variable = var20,
            onvalue = 'A43',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var21 = StringVar()
    cb21 = Checkbutton(
            master = fr1,
            text = 'A66',
            variable = var21,
            onvalue = 'A66',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var22 = StringVar()
    cb22 = Checkbutton(
            master = fr1,
            text = 'A68',
            variable = var22,
            onvalue = 'A68',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var23 = StringVar()
    cb23 = Checkbutton(
            master = fr1,
            text = 'A69',
            variable = var23,
            onvalue = 'A69',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var24 = StringVar()
    cb24 = Checkbutton(
            master = fr1,
            text = 'A74',
            variable = var24,
            onvalue = 'A74',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var25 = StringVar()
    cb25 = Checkbutton(
            master = fr1,
            text = 'A80',
            variable = var25,
            onvalue = 'A80',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var26 = StringVar()
    cb26 = Checkbutton(
            master = fr1,
            text = 'A203',
            variable = var26,
            onvalue = 'A203',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var27 = StringVar()
    cb27 = Checkbutton(
            master = fr1,
            text = 'A210',
            variable = var27,
            onvalue = 'A210',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var28 = StringVar()
    cb28 = Checkbutton(
            master = fr1,
            text = 'A2403',
            variable = var28,
            onvalue = 'A2403',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var29 = StringVar()
    cb29 = Checkbutton(
            master = fr1,
            text = 'B5',
            variable = var29,
            onvalue = 'B5',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var30 = StringVar()
    cb30 = Checkbutton(
            master = fr1,
            text = 'B7',
            variable = var30,
            onvalue = 'B7',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var31 = StringVar()
    cb31 = Checkbutton(
            master = fr1,
            text = 'B8',
            variable = var31,
            onvalue = 'B8',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var32 = StringVar()
    cb32 = Checkbutton(
            master = fr1,
            text = 'B12',
            variable = var32,
            onvalue = 'B12',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var33 = StringVar()
    cb33 = Checkbutton(
            master = fr1,
            text = 'B13',
            variable = var33,
            onvalue = 'B13',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var34 = StringVar()
    cb34 = Checkbutton(
            master = fr1,
            text = 'B14',
            variable = var34,
            onvalue = 'B14',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var35 = StringVar()
    cb35 = Checkbutton(
            master = fr1,
            text = 'B15',
            variable = var35,
            onvalue = 'B15',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var36 = StringVar()
    cb36 = Checkbutton(
            master = fr1,
            text = 'B16',
            variable = var36,
            onvalue = 'B16',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var37 = StringVar()
    cb37 = Checkbutton(
            master = fr1,
            text = 'B17',
            variable = var37,
            onvalue = 'B17',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var38 = StringVar()
    cb38 = Checkbutton(
            master = fr1,
            text = 'B18',
            variable = var38,
            onvalue = 'B18',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var39 = StringVar()
    cb39 = Checkbutton(
            master = fr1,
            text = 'B21',
            variable = var39,
            onvalue = 'B21',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var40 = StringVar()
    cb40 = Checkbutton(
            master = fr1,
            text = 'B22',
            variable = var40,
            onvalue = 'B22',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var41 = StringVar()
    cb41 = Checkbutton(
            master = fr1,
            text = 'B27',
            variable = var41,
            onvalue = 'B27',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var42 = StringVar()
    cb42 = Checkbutton(
            master = fr1,
            text = 'B35',
            variable = var42,
            onvalue = 'B35',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var43 = StringVar()
    cb43 = Checkbutton(
            master = fr1,
            text = 'B37',
            variable = var43,
            onvalue = 'B37',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var44 = StringVar()
    cb44 = Checkbutton(
            master = fr1,
            text = 'B38',
            variable = var44,
            onvalue = 'B38',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var45 = StringVar()
    cb45 = Checkbutton(
            master = fr1,
            text = 'B39',
            variable = var45,
            onvalue = 'B39',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var46 = StringVar()
    cb46 = Checkbutton(
            master = fr1,
            text = 'B40',
            variable = var46,
            onvalue = 'B40',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var47 = StringVar()
    cb47 = Checkbutton(
            master = fr1,
            text = 'B41',
            variable = var47,
            onvalue = 'B41',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var48 = StringVar()
    cb48 = Checkbutton(
            master = fr1,
            text = 'B42',
            variable = var48,
            onvalue = 'B42',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var49 = StringVar()
    cb49 = Checkbutton(
            master = fr1,
            text = 'B44',
            variable = var49,
            onvalue = 'B44',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var50 = StringVar()
    cb50 = Checkbutton(
            master = fr1,
            text = 'B45',
            variable = var50,
            onvalue = 'B45',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var51 = StringVar()
    cb51 = Checkbutton(
            master = fr1,
            text = 'B46',
            variable = var51,
            onvalue = 'B46',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var52 = StringVar()
    cb52 = Checkbutton(
            master = fr1,
            text = 'B47',
            variable = var52,
            onvalue = 'B47',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var53 = StringVar()
    cb53 = Checkbutton(
            master = fr1,
            text = 'B48',
            variable = var53,
            onvalue = 'B48',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var54 = StringVar()
    cb54 = Checkbutton(
            master = fr1,
            text = 'B49',
            variable = var54,
            onvalue = 'B49',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var55 = StringVar()
    cb55 = Checkbutton(
            master = fr1,
            text = 'B50',
            variable = var55,
            onvalue = 'B50',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var56 = StringVar()
    cb56 = Checkbutton(
            master = fr1,
            text = 'B51',
            variable = var56,
            onvalue = 'B51',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var57 = StringVar()
    cb57 = Checkbutton(
            master = fr1,
            text = 'B52',
            variable = var57,
            onvalue = 'B52',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var58 = StringVar()
    cb58 = Checkbutton(
            master = fr1,
            text = 'B53',
            variable = var58,
            onvalue = 'B53',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var59 = StringVar()
    cb59 = Checkbutton(
            master = fr1,
            text = 'B54',
            variable = var59,
            onvalue = 'B54',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var60 = StringVar()
    cb60 = Checkbutton(
            master = fr1,
            text = 'B55',
            variable = var60,
            onvalue = 'B55',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var61 = StringVar()
    cb61 = Checkbutton(
            master = fr1,
            text = 'B56',
            variable = var61,
            onvalue = 'B56',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var62 = StringVar()
    cb62 = Checkbutton(
            master = fr1,
            text = 'B57',
            variable = var62,
            onvalue = 'B57',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var63 = StringVar()
    cb63 = Checkbutton(
            master = fr1,
            text = 'B58',
            variable = var63,
            onvalue = 'B58',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var64 = StringVar()
    cb64 = Checkbutton(
            master = fr1,
            text = 'B59',
            variable = var64,
            onvalue = 'B59',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var65 = StringVar()
    cb65 = Checkbutton(
            master = fr1,
            text = 'B60',
            variable = var65,
            onvalue = 'B60',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var66 = StringVar()
    cb66 = Checkbutton(
            master = fr1,
            text = 'B61',
            variable = var66,
            onvalue = 'B61',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var67 = StringVar()
    cb67 = Checkbutton(
            master = fr1,
            text = 'B62',
            variable = var67,
            onvalue = 'B62',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var68 = StringVar()
    cb68 = Checkbutton(
            master = fr1,
            text = 'B63',
            variable = var68,
            onvalue = 'B63',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var69 = StringVar()
    cb69 = Checkbutton(
            master = fr1,
            text = 'B64',
            variable = var69,
            onvalue = 'B64',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var70 = StringVar()
    cb70 = Checkbutton(
            master = fr1,
            text = 'B65',
            variable = var70,
            onvalue = 'B65',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var71 = StringVar()
    cb71 = Checkbutton(
            master = fr1,
            text = 'B67',
            variable = var71,
            onvalue = 'B67',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var72 = StringVar()
    cb72 = Checkbutton(
            master = fr1,
            text = 'B70',
            variable = var72,
            onvalue = 'B70',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var73 = StringVar()
    cb73 = Checkbutton(
            master = fr1,
            text = 'B71',
            variable = var73,
            onvalue = 'B71',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var74 = StringVar()
    cb74 = Checkbutton(
            master = fr1,
            text = 'B72',
            variable = var74,
            onvalue = 'B72',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var75 = StringVar()
    cb75 = Checkbutton(
            master = fr1,
            text = 'B73',
            variable = var75,
            onvalue = 'B73',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var76 = StringVar()
    cb76 = Checkbutton(
            master = fr1,
            text = 'B75',
            variable = var76,
            onvalue = 'B75',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var77 = StringVar()
    cb77 = Checkbutton(
            master = fr1,
            text = 'B77',
            variable = var77,
            onvalue = 'B77',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var78 = StringVar()
    cb78 = Checkbutton(
            master = fr1,
            text = 'B78',
            variable = var78,
            onvalue = 'B78',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var79 = StringVar()
    cb79 = Checkbutton(
            master = fr1,
            text = 'B81',
            variable = var79,
            onvalue = 'B81',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var80 = StringVar()
    cb80 = Checkbutton(
            master = fr1,
            text = 'B82',
            variable = var80,
            onvalue = 'B82',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var81 = StringVar()
    cb81 = Checkbutton(
            master = fr1,
            text = 'B703',
            variable = var81,
            onvalue = 'B703',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var82 = StringVar()
    cb82 = Checkbutton(
            master = fr1,
            text = 'B0802',
            variable = var82,
            onvalue = 'B0802',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var83 = StringVar()
    cb83 = Checkbutton(
            master = fr1,
            text = 'B0803',
            variable = var83,
            onvalue = 'B0803',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var84 = StringVar()
    cb84 = Checkbutton(
            master = fr1,
            text = 'B1309',
            variable = var84,
            onvalue = 'B1309',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var85 = StringVar()
    cb85 = Checkbutton(
            master = fr1,
            text = 'B1809',
            variable = var85,
            onvalue = 'B1809',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var86 = StringVar()
    cb86 = Checkbutton(
            master = fr1,
            text = 'B2706',
            variable = var86,
            onvalue = 'B2706',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var87 = StringVar()
    cb87 = Checkbutton(
            master = fr1,
            text = 'B2717',
            variable = var87,
            onvalue = 'B2717',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var88 = StringVar()
    cb88 = Checkbutton(
            master = fr1,
            text = 'B2718',
            variable = var88,
            onvalue = 'B2718',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var89 = StringVar()
    cb89 = Checkbutton(
            master = fr1,
            text = 'B3901',
            variable = var89,
            onvalue = 'B3901',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var90 = StringVar()
    cb90 = Checkbutton(
            master = fr1,
            text = 'B3902',
            variable = var90,
            onvalue = 'B3902',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var91 = StringVar()
    cb91 = Checkbutton(
            master = fr1,
            text = 'B4005',
            variable = var91,
            onvalue = 'B4005',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var92 = StringVar()
    cb92 = Checkbutton(
            master = fr1,
            text = 'B4406',
            variable = var92,
            onvalue = 'B4406',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var93 = StringVar()
    cb93 = Checkbutton(
            master = fr1,
            text = 'B4409',
            variable = var93,
            onvalue = 'B4409',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var94 = StringVar()
    cb94 = Checkbutton(
            master = fr1,
            text = 'B4412',
            variable = var94,
            onvalue = 'B4412',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var95 = StringVar()
    cb95 = Checkbutton(
            master = fr1,
            text = 'B4702',
            variable = var95,
            onvalue = 'B4702',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var96 = StringVar()
    cb96 = Checkbutton(
            master = fr1,
            text = 'B5102',
            variable = var96,
            onvalue = 'B5102',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var97 = StringVar()
    cb97 = Checkbutton(
            master = fr1,
            text = 'B5103',
            variable = var97,
            onvalue = 'B5103',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    var98 = StringVar()
    cb98 = Checkbutton(
            master = fr1,
            text = 'B5607',
            variable = var98,
            onvalue = 'B5607',
            offvalue = '',
            font = ('Abadi', 12),
            bg = '#0f0f0f',
            fg = '#b87333',
            anchor = 'w',
            width = 8
            )
    cbs = [cb1,cb2,cb3,cb4,cb5,cb6,cb7,cb8,cb9,cb10,
           cb11,cb12,cb13,cb14,cb15,cb16,cb17,cb18,cb19,cb20,
           cb21,cb22,cb23,cb24,cb25,cb26,cb27,cb28,cb29,cb30,
           cb31,cb32,cb33,cb34,cb35,cb36,cb37,cb38,cb39,cb40,
           cb41,cb42,cb43,cb44,cb45,cb46,cb47,cb48,cb49,cb50,
           cb51,cb52,cb53,cb54,cb55,cb56,cb57,cb58,cb59,cb60,
           cb61,cb62,cb63,cb64,cb65,cb66,cb67,cb68,cb69,cb70,
           cb71,cb72,cb73,cb74,cb75,cb76,cb77,cb78,cb79,cb80,
           cb81,cb82,cb83,cb84,cb85,cb86,cb87,cb88,cb89,cb90,
           cb91,cb92,cb93,cb94,cb95,cb96,cb97,cb98]
    
    def checkall():
        for cb in cbs:
            cb.select()
            
    def uncheckall():
        for cb in cbs:
            cb.deselect()
            
    cb_but1 = Button(
            master = fr1,
            text = 'Select All Antibodies',
            command = checkall,
            font = ('Abadi', 12, 'bold'),
            bg = '#0f0f0f',
            fg = '#b87333',
            width = 22,
            relief = RIDGE,
            bd = 3
            )
    cb_but2 = Button(
            master = fr1,
            text = 'Deselect All Antibodies',
            command = uncheckall,
            font = ('Abadi', 12, 'bold'),
            bg = '#0f0f0f',
            fg = '#b87333',
            width = 22,
            relief = RIDGE,
            bd = 3
            )

    
    fr1.pack(padx = 3, pady = 3)
    lab1.grid(row = 0, column = 0, padx = 3, pady = 5)
    lab2.grid(row = 0, column = 2, padx = 3, pady = 5)
    lab3.grid(row = 1, column = 0, padx = 3, pady = 5)
    lab4.grid(row = 1, column = 2, padx = 3, pady = 5)
    lab5.grid(row = 3, column = 0, padx = 3, pady = 20, columnspan = 7)
    lab6.grid(row = 0, column = 4, padx = 3, pady = 5)
    #lab7.grid(row = 1, column = 4, padx = 3, pady = 5)
    ent1.grid(row = 0, column = 1, padx = 3, pady = 5, sticky = W)
    ent2.grid(row = 0, column = 3, padx = 3, pady = 5, sticky = W)
    ent3.grid(row = 1, column = 1, padx = 3, pady = 5, sticky = W)
    ent4.grid(row = 1, column = 3, padx = 3, pady = 5, sticky = W)
    cb1.grid(row = 4, column = 0, padx = 3, pady = 5)
    cb2.grid(row = 4, column = 1, padx = 3, pady = 5)
    cb3.grid(row = 4, column = 2, padx = 3, pady = 5)
    cb4.grid(row = 4, column = 3, padx = 3, pady = 5)
    cb5.grid(row = 4, column = 4, padx = 3, pady = 5)
    cb6.grid(row = 4, column = 5, padx = 3, pady = 5)
    cb7.grid(row = 4, column = 6, padx = 3, pady = 5)
    cb8.grid(row = 5, column = 0, padx = 3, pady = 5)
    cb9.grid(row = 5, column = 1, padx = 3, pady = 5)
    cb10.grid(row = 5, column = 2, padx = 3, pady = 5)
    cb11.grid(row = 5, column = 3, padx = 3, pady = 5)
    cb12.grid(row = 5, column = 4, padx = 3, pady = 5)
    cb13.grid(row = 5, column = 5, padx = 3, pady = 5)
    cb14.grid(row = 5, column = 6, padx = 3, pady = 5)
    cb15.grid(row = 6, column = 0, padx = 3, pady = 5)
    cb16.grid(row = 6, column = 1, padx = 3, pady = 5)
    cb17.grid(row = 6, column = 2, padx = 3, pady = 5)
    cb18.grid(row = 6, column = 3, padx = 3, pady = 5)
    cb19.grid(row = 6, column = 4, padx = 3, pady = 5)
    cb20.grid(row = 6, column = 5, padx = 3, pady = 5)
    cb21.grid(row = 6, column = 6, padx = 3, pady = 5)
    cb22.grid(row = 7, column = 0, padx = 3, pady = 5)
    cb23.grid(row = 7, column = 1, padx = 3, pady = 5)
    cb24.grid(row = 7, column = 2, padx = 3, pady = 5)
    cb25.grid(row = 7, column = 3, padx = 3, pady = 5)
    cb26.grid(row = 7, column = 4, padx = 3, pady = 5)
    cb27.grid(row = 7, column = 5, padx = 3, pady = 5)
    cb28.grid(row = 7, column = 6, padx = 3, pady = 5)
    cb29.grid(row = 8, column = 0, padx = 3, pady = 5)
    cb30.grid(row = 8, column = 1, padx = 3, pady = 5)
    cb31.grid(row = 8, column = 2, padx = 3, pady = 5)
    cb32.grid(row = 8, column = 3, padx = 3, pady = 5)
    cb33.grid(row = 8, column = 4, padx = 3, pady = 5)
    cb34.grid(row = 8, column = 5, padx = 3, pady = 5)
    cb35.grid(row = 8, column = 6, padx = 3, pady = 5)
    cb36.grid(row = 9, column = 0, padx = 3, pady = 5)
    cb37.grid(row = 9, column = 1, padx = 3, pady = 5)
    cb38.grid(row = 9, column = 2, padx = 3, pady = 5)
    cb39.grid(row = 9, column = 3, padx = 3, pady = 5)
    cb40.grid(row = 9, column = 4, padx = 3, pady = 5)
    cb41.grid(row = 9, column = 5, padx = 3, pady = 5)
    cb42.grid(row = 9, column = 6, padx = 3, pady = 5)
    cb43.grid(row = 10, column = 0, padx = 3, pady = 5)
    cb44.grid(row = 10, column = 1, padx = 3, pady = 5)
    cb45.grid(row = 10, column = 2, padx = 3, pady = 5)
    cb46.grid(row = 10, column = 3, padx = 3, pady = 5)
    cb47.grid(row = 10, column = 4, padx = 3, pady = 5)
    cb48.grid(row = 10, column = 5, padx = 3, pady = 5)
    cb49.grid(row = 10, column = 6, padx = 3, pady = 5)
    cb50.grid(row = 11, column = 0, padx = 3, pady = 5)
    cb51.grid(row = 11, column = 1, padx = 3, pady = 5)
    cb52.grid(row = 11, column = 2, padx = 3, pady = 5)
    cb53.grid(row = 11, column = 3, padx = 3, pady = 5)
    cb54.grid(row = 11, column = 4, padx = 3, pady = 5)
    cb55.grid(row = 11, column = 5, padx = 3, pady = 5)
    cb56.grid(row = 11, column = 6, padx = 3, pady = 5)
    cb57.grid(row = 12, column = 0, padx = 3, pady = 5)
    cb58.grid(row = 12, column = 1, padx = 3, pady = 5)
    cb59.grid(row = 12, column = 2, padx = 3, pady = 5)
    cb60.grid(row = 12, column = 3, padx = 3, pady = 5)
    cb61.grid(row = 12, column = 4, padx = 3, pady = 5)
    cb62.grid(row = 12, column = 5, padx = 3, pady = 5)
    cb63.grid(row = 12, column = 6, padx = 3, pady = 5)
    cb64.grid(row = 13, column = 0, padx = 3, pady = 5)
    cb65.grid(row = 13, column = 1, padx = 3, pady = 5)
    cb66.grid(row = 13, column = 2, padx = 3, pady = 5)
    cb67.grid(row = 13, column = 3, padx = 3, pady = 5)
    cb68.grid(row = 13, column = 4, padx = 3, pady = 5)
    cb69.grid(row = 13, column = 5, padx = 3, pady = 5)
    cb70.grid(row = 13, column = 6, padx = 3, pady = 5)
    cb71.grid(row = 14, column = 0, padx = 3, pady = 5)
    cb72.grid(row = 14, column = 1, padx = 3, pady = 5)
    cb73.grid(row = 14, column = 2, padx = 3, pady = 5)
    cb74.grid(row = 14, column = 3, padx = 3, pady = 5)
    cb75.grid(row = 14, column = 4, padx = 3, pady = 5)
    cb76.grid(row = 14, column = 5, padx = 3, pady = 5)
    cb77.grid(row = 14, column = 6, padx = 3, pady = 5)
    cb78.grid(row = 15, column = 0, padx = 3, pady = 5)
    cb79.grid(row = 15, column = 1, padx = 3, pady = 5)
    cb80.grid(row = 15, column = 2, padx = 3, pady = 5)
    cb81.grid(row = 15, column = 3, padx = 3, pady = 5)
    cb82.grid(row = 15, column = 4, padx = 3, pady = 5)
    cb83.grid(row = 15, column = 5, padx = 3, pady = 5)
    cb84.grid(row = 15, column = 6, padx = 3, pady = 5)
    cb85.grid(row = 16, column = 0, padx = 3, pady = 5)
    cb86.grid(row = 16, column = 1, padx = 3, pady = 5)
    cb87.grid(row = 16, column = 2, padx = 3, pady = 5)
    cb88.grid(row = 16, column = 3, padx = 3, pady = 5)
    cb89.grid(row = 16, column = 4, padx = 3, pady = 5)
    cb90.grid(row = 16, column = 5, padx = 3, pady = 5)
    cb91.grid(row = 16, column = 6, padx = 3, pady = 5)
    cb92.grid(row = 17, column = 0, padx = 3, pady = 5)
    cb93.grid(row = 17, column = 1, padx = 3, pady = 5)
    cb94.grid(row = 17, column = 2, padx = 3, pady = 5)
    cb95.grid(row = 17, column = 3, padx = 3, pady = 5)
    cb96.grid(row = 17, column = 4, padx = 3, pady = 5)
    cb97.grid(row = 17, column = 5, padx = 3, pady = 5)
    cb98.grid(row = 17, column = 6, padx = 3, pady = 5)
    cb_but1.grid(row = 18, column = 1, padx = 3, pady = 5, columnspan = 2, sticky = W)
    cb_but2.grid(row = 18, column = 4, padx = 3, pady = 5, columnspan = 2, sticky = E)

    
    def get_daily_file():
        global daily_file
        HLA_report_file = filedialog.askopenfilename(
            filetypes = [("Excel File", "*.xlsx")]
            )
        if not HLA_report_file:
            return
        daily_file = HLA_report_file

    
    but1 = Button(
            master = fr1,
            text = 'Open',
            command = get_daily_file,
            font = ('Abadi', 12, 'bold'),
            bg = '#0f0f0f',
            fg = '#b87333',
            relief = RIDGE,
            width = 8,
            bd = 3
            )
        
    but1.grid(row = 0, column = 5, padx = 3, pady = 5)
    
    def save_daily_file():
        ptA1 = ent1.get()
        ptA2 = ent2.get()
        ptB1 = ent3.get()
        ptB2 = ent4.get()
        vvar1 = var1.get()
        vvar2 = var2.get()
        vvar3 = var3.get()
        vvar4 = var4.get()
        vvar5 = var5.get()
        vvar6 = var6.get()
        vvar7 = var7.get()
        vvar8 = var8.get()
        vvar9 = var9.get()
        vvar10 = var10.get()
        vvar11 = var11.get()
        vvar12 = var12.get()
        vvar13 = var13.get()
        vvar14 = var14.get()
        vvar15 = var15.get()
        vvar16 = var16.get()
        vvar17 = var17.get()
        vvar18 = var18.get()
        vvar19 = var19.get()
        vvar20 = var20.get()
        vvar21 = var21.get()
        vvar22 = var22.get()
        vvar23 = var23.get()
        vvar24 = var24.get()
        vvar25 = var25.get()
        vvar26 = var26.get()
        vvar27 = var27.get()
        vvar28 = var28.get()
        vvar29 = var29.get()
        vvar30 = var30.get()
        vvar31 = var31.get()
        vvar32 = var32.get()
        vvar33 = var33.get()
        vvar34 = var34.get()
        vvar35 = var35.get()
        vvar36 = var36.get()
        vvar37 = var37.get()
        vvar38 = var38.get()
        vvar39 = var39.get()
        vvar40 = var40.get()
        vvar41 = var41.get()
        vvar42 = var42.get()
        vvar43 = var43.get()
        vvar44 = var44.get()
        vvar45 = var45.get()
        vvar46 = var46.get()
        vvar47 = var47.get()
        vvar48 = var48.get()
        vvar49 = var49.get()
        vvar50 = var50.get()
        vvar51 = var51.get()
        vvar52 = var52.get()
        vvar53 = var53.get()
        vvar54 = var54.get()
        vvar55 = var55.get()
        vvar56 = var56.get()
        vvar57 = var57.get()
        vvar58 = var58.get()
        vvar59 = var59.get()
        vvar60 = var60.get()
        vvar61 = var61.get()
        vvar62 = var62.get()
        vvar63 = var63.get()
        vvar64 = var64.get()
        vvar65 = var65.get()
        vvar66 = var66.get()
        vvar67 = var67.get()
        vvar68 = var68.get()
        vvar69 = var69.get()
        vvar70 = var70.get()
        vvar71 = var71.get()
        vvar72 = var72.get()
        vvar73 = var73.get()
        vvar74 = var74.get()
        vvar75 = var75.get()
        vvar76 = var76.get()
        vvar77 = var77.get()
        vvar78 = var78.get()
        vvar79 = var79.get()
        vvar80 = var80.get()
        vvar81 = var81.get()
        vvar82 = var82.get()
        vvar83 = var83.get()
        vvar84 = var84.get()
        vvar85 = var85.get()
        vvar86 = var86.get()
        vvar87 = var87.get()    
        vvar88 = var88.get()
        vvar89 = var89.get()
        vvar90 = var90.get()
        vvar91 = var91.get()
        vvar92 = var92.get()
        vvar93 = var93.get()
        vvar94 = var94.get()
        vvar95 = var95.get()
        vvar96 = var96.get()
        vvar97 = var97.get()
        vvar98 = var98.get()
        antibodies = {vvar1,vvar2,vvar3,vvar4,vvar5,vvar6,vvar7,vvar8,vvar9,vvar10,
                  vvar11,vvar12,vvar13,vvar14,vvar15,vvar16,vvar17,vvar18,vvar19,vvar20,
                  vvar21,vvar22,vvar23,vvar24,vvar25,vvar26,vvar27,vvar28,vvar29,vvar30,
                  vvar31,vvar32,vvar33,vvar34,vvar35,vvar36,vvar37,vvar38,vvar39,vvar40,
                  vvar41,vvar42,vvar43,vvar44,vvar45,vvar46,vvar47,vvar48,vvar49,vvar50,
                  vvar51,vvar52,vvar53,vvar54,vvar55,vvar56,vvar57,vvar58,vvar59,vvar60,
                  vvar61,vvar62,vvar63,vvar64,vvar65,vvar66,vvar67,vvar68,vvar69,vvar70,
                  vvar71,vvar72,vvar73,vvar74,vvar75,vvar76,vvar77,vvar78,vvar79,vvar80,
                  vvar81,vvar82,vvar83,vvar84,vvar85,vvar86,vvar87,vvar88,vvar89,vvar90,
                  vvar91,vvar92,vvar93,vvar94,vvar95,vvar96,vvar97,vvar98}
    
        antibodies = list(antibodies)
        graded_HLA_report_file = daily_grader(daily_file, ptA1, ptA2, ptB1, ptB2, antibodies)
        save_HLA_report_file = filedialog.asksaveasfilename(
            filetypes = [("Excel Files", "*.xlsx")]
            )
        if not save_HLA_report_file:
            return
        writer = pd.ExcelWriter(save_HLA_report_file + '.xlsx', engine='xlsxwriter')
        graded_HLA_report_file.to_excel(writer, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format':'#,##0'})
        worksheet.set_column('A:A', 6, format1)
        worksheet.set_column('B:B', 8, format1)
        worksheet.set_column('C:C', 18, format1)
        worksheet.set_column('D:H', 8, format1)
        worksheet.set_column('I:I', 4, format1)
        writer.save()
        
    but2 = Button(
            master = fr1,
            text = 'Save',
            command = save_daily_file,
            font = ('Abadi', 12, 'bold'),
            bg = '#0f0f0f',
            fg = '#b87333',
            relief = RIDGE,
            width = 8,
            bd = 3
            )
        
    but2.grid(row = 0, column = 6, padx = 3, pady = 5)
    
    
    '''def get_donor_pool_file():
        global donor_pool_file
        HLA_report_file = filedialog.askopenfilename(
            filetypes = [("Excel File", "*.xlsx")]
            )
        if not HLA_report_file:
            return
        donor_pool_file = HLA_report_file

    
    but3 = Button(
            master = fr1,
            text = 'Open',
            command = get_donor_pool_file,
            font = ('Abadi', 12, 'bold'),
            bg = '#0f0f0f',
            fg = '#b87333',
            relief = RIDGE,
            width = 8,
            bd = 3
            )
        
    but3.grid(row = 1, column = 5, padx = 3, pady = 5)'''
    
    def save_donor_pool_file():
        ptA1 = ent1.get()
        ptA2 = ent2.get()
        ptB1 = ent3.get()
        ptB2 = ent4.get()
        vvar1 = var1.get()
        vvar2 = var2.get()
        vvar3 = var3.get()
        vvar4 = var4.get()
        vvar5 = var5.get()
        vvar6 = var6.get()
        vvar7 = var7.get()
        vvar8 = var8.get()
        vvar9 = var9.get()
        vvar10 = var10.get()
        vvar11 = var11.get()
        vvar12 = var12.get()
        vvar13 = var13.get()
        vvar14 = var14.get()
        vvar15 = var15.get()
        vvar16 = var16.get()
        vvar17 = var17.get()
        vvar18 = var18.get()
        vvar19 = var19.get()
        vvar20 = var20.get()
        vvar21 = var21.get()
        vvar22 = var22.get()
        vvar23 = var23.get()
        vvar24 = var24.get()
        vvar25 = var25.get()
        vvar26 = var26.get()
        vvar27 = var27.get()
        vvar28 = var28.get()
        vvar29 = var29.get()
        vvar30 = var30.get()
        vvar31 = var31.get()
        vvar32 = var32.get()
        vvar33 = var33.get()
        vvar34 = var34.get()
        vvar35 = var35.get()
        vvar36 = var36.get()
        vvar37 = var37.get()
        vvar38 = var38.get()
        vvar39 = var39.get()
        vvar40 = var40.get()
        vvar41 = var41.get()
        vvar42 = var42.get()
        vvar43 = var43.get()
        vvar44 = var44.get()
        vvar45 = var45.get()
        vvar46 = var46.get()
        vvar47 = var47.get()
        vvar48 = var48.get()
        vvar49 = var49.get()
        vvar50 = var50.get()
        vvar51 = var51.get()
        vvar52 = var52.get()
        vvar53 = var53.get()
        vvar54 = var54.get()
        vvar55 = var55.get()
        vvar56 = var56.get()
        vvar57 = var57.get()
        vvar58 = var58.get()
        vvar59 = var59.get()
        vvar60 = var60.get()
        vvar61 = var61.get()
        vvar62 = var62.get()
        vvar63 = var63.get()
        vvar64 = var64.get()
        vvar65 = var65.get()
        vvar66 = var66.get()
        vvar67 = var67.get()
        vvar68 = var68.get()
        vvar69 = var69.get()
        vvar70 = var70.get()
        vvar71 = var71.get()
        vvar72 = var72.get()
        vvar73 = var73.get()
        vvar74 = var74.get()
        vvar75 = var75.get()
        vvar76 = var76.get()
        vvar77 = var77.get()
        vvar78 = var78.get()
        vvar79 = var79.get()
        vvar80 = var80.get()
        vvar81 = var81.get()
        vvar82 = var82.get()
        vvar83 = var83.get()
        vvar84 = var84.get()
        vvar85 = var85.get()
        vvar86 = var86.get()
        vvar87 = var87.get()    
        vvar88 = var88.get()
        vvar89 = var89.get()
        vvar90 = var90.get()
        vvar91 = var91.get()
        vvar92 = var92.get()
        vvar93 = var93.get()
        vvar94 = var94.get()
        vvar95 = var95.get()
        vvar96 = var96.get()
        vvar97 = var97.get()
        vvar98 = var98.get()
        antibodies = {vvar1,vvar2,vvar3,vvar4,vvar5,vvar6,vvar7,vvar8,vvar9,vvar10,
                  vvar11,vvar12,vvar13,vvar14,vvar15,vvar16,vvar17,vvar18,vvar19,vvar20,
                  vvar21,vvar22,vvar23,vvar24,vvar25,vvar26,vvar27,vvar28,vvar29,vvar30,
                  vvar31,vvar32,vvar33,vvar34,vvar35,vvar36,vvar37,vvar38,vvar39,vvar40,
                  vvar41,vvar42,vvar43,vvar44,vvar45,vvar46,vvar47,vvar48,vvar49,vvar50,
                  vvar51,vvar52,vvar53,vvar54,vvar55,vvar56,vvar57,vvar58,vvar59,vvar60,
                  vvar61,vvar62,vvar63,vvar64,vvar65,vvar66,vvar67,vvar68,vvar69,vvar70,
                  vvar71,vvar72,vvar73,vvar74,vvar75,vvar76,vvar77,vvar78,vvar79,vvar80,
                  vvar81,vvar82,vvar83,vvar84,vvar85,vvar86,vvar87,vvar88,vvar89,vvar90,
                  vvar91,vvar92,vvar93,vvar94,vvar95,vvar96,vvar97,vvar98}
    
        antibodies = list(antibodies)
        donor_pool_file = 'Book1.xlsx'
        graded_HLA_report_file = donor_pool_grader(donor_pool_file, ptA1, ptA2, ptB1, ptB2, antibodies)
        save_HLA_report_file = filedialog.asksaveasfilename(
            filetypes = [("Excel Files", "*.xlsx")]
            )
        if not save_HLA_report_file:
            return
        writer = pd.ExcelWriter(save_HLA_report_file + '.xlsx', engine='xlsxwriter')
        graded_HLA_report_file.to_excel(writer, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format':'#,##0'})
        worksheet.set_column('A:A', 6, format1)
        worksheet.set_column('B:B', 10, format1)
        worksheet.set_column('C:C', 23, format1)
        worksheet.set_column('D:H', 8, format1)
        worksheet.set_column('I:I', 4, format1)
        writer.save()
        
    but3 = Button(
            master = fr1,
            text = 'Donor Recruitment List',
            command = save_donor_pool_file,
            font = ('Abadi', 12, 'bold'),
            bg = '#0f0f0f',
            fg = '#b87333',
            relief = RIDGE,
            width = 19,
            bd = 3
            )
        
    but3.grid(row = 1, column = 5, padx = 3, pady = 5, columnspan = 2)

but1 = Button(
        master = fr1,
        text = 'HLA Grader',
        command = HLA_grader,
        width = 20,
        font = ('Abadi', 12, 'bold'),
        relief = RIDGE,
        bg = '#0f0f0f',
        fg = '#b87333'
        )
lab1 = Label(
        master = fr1,
        text = 'Grade daily reports and setup donor recruitment list.',
        anchor = 'w',
        width = 80,
        font = ('Abadi', 12),
        bg = '#0f0f0f',
        fg = '#b87333'
        )
        
but1.grid(row = 0, column = 0, padx = 5, pady = 5)
lab1.grid(row = 0, column = 1, padx = 5, pady = 5)



'''
################################RBC Finder################################
'''
def RBC():
    RBC_finder_window = Toplevel(onyx)
    RBC_finder_window.title("RBC Finder")
    RBC_finder_window.resizable(width = False, height = False)
    
but2 = Button(
        master = fr1,
        text = 'RBC Finder',
        command = RBC,
        width = 20,
        font = ('Abadi', 12, 'bold'),
        relief = RIDGE,
        bg = '#0f0f0f',
        fg = '#b87333',
        bd = 3
        )
lab2 = Label(
        master = fr1,
        text = 'Find RBCs for sickle patients, rare freezing, and calculate units to screen based on STBTC population.',
        anchor = 'w',
        width = 80,
        font = ('Abadi', 12),
        bg = '#0f0f0f',
        fg = '#b87333'
        )
        
but2.grid(row = 1, column = 0, padx = 5, pady = 5)
lab2.grid(row = 1, column = 1, padx = 5, pady = 5)


'''
################################SA Tracking Log################################
'''
def SA_track():
    SA_tracking_log = Toplevel(onyx)
    SA_tracking_log.title("SA Tracking Log")
    SA_tracking_log.resizable(width = False, height = False)
    
but3 = Button(
        master = fr1,
        text = 'SA Tracking Log',
        command = SA_track,
        width = 20,
        font = ('Abadi', 12, 'bold'),
        relief = RIDGE,
        bg = '#0f0f0f',
        fg = '#b87333',
        bd = 3
        )
lab3 = Label(
        master = fr1,
        text = 'Specimen tracking log for San Antonio IRL.',
        anchor = 'w',
        width = 80,
        font = ('Abadi', 12),
        bg = '#0f0f0f',
        fg = '#b87333'
        )
        
but3.grid(row = 2, column = 0, padx = 5, pady = 5)
lab3.grid(row = 2, column = 1, padx = 5, pady = 5)


'''
################################ATL Tracking Log################################
'''
def ATL_track():
    ATL_tracking_log = Toplevel(onyx)
    ATL_tracking_log.title("ATL Tracking Log")
    ATL_tracking_log.resizable(width = False, height = False)
    
but4 = Button(
        master = fr1,
        text = 'ATL Tracking Log',
        command = ATL_track,
        width = 20,
        font = ('Abadi', 12, 'bold'),
        relief = RIDGE,
        bg = '#0f0f0f',
        fg = '#b87333',
        bd = 3
        )
lab4 = Label(
        master = fr1,
        text = 'Specimen tracking log for Atlanta IRL.',
        anchor = 'w',
        width = 80,
        font = ('Abadi', 12),
        bg = '#0f0f0f',
        fg = '#b87333',
        bd = 3
        )
        
but4.grid(row = 3, column = 0, padx = 5, pady = 5)
lab4.grid(row = 3, column = 1, padx = 5, pady = 5)


onyx.mainloop()
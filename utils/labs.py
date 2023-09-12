s = ['o','D', '^' ,'s', 'x','P']


c_edu = ['#8dd3c7','#276FBF','#183059']
c_emp = ['#addd8e','#31a354']
c_sett= ['#7a0177','#f768a1', '#fbb4b9']
c_fin = ['#fcae91','#fb6a4a','#a50f15']
c_age = ['#e0ecf4','#bfd3e6','#9ebcda','#8c96c6','#8c6bb1','#88419d','#810f7c','#4d004b']

C_VAR = {'employed':'#31a354',
         'education3':'#276FBF',
         'settlement_cur_num':'#7a0177',
         'fin_now3a' :'#fb6a4a',
         'age_group8': '#fed976'
        }

P_VAR = {'employed':'Greens',
         'education3':'Blues',
         'settlement_cur_num':'PuRd',
         'fin_now3a' :'Reds',
         'age_group8': 'YlOrBr'
        }

C_VAR_LEVS = {
    'employed':c_emp,
    'education3':c_edu,
    'settlement_cur_num':c_sett,
    'fin_now3a' :c_fin,
    'age_group8' :c_age
        }



epi_waves_oredered =[
'1st IP',
 '2nd W',
 '3rd W',
 '2nd IP',
 '4th W',
 '5th W',
 #'3rd IP'
]

WAVES = {
 '04_2020': 1,  
    '05_2020': 2,
    '06_2020': 3,   
    '08_2020': 4,  
    '09_2020': 5,  
    '10_2020': 6,  
    '11_2020': 7,  
    '12_2020': 8,  
    '01_2021': 9,  
    '02_2021': 10,   
    '03_2021': 11,  
    '04_2021': 12,  
    '05_2021': 13,   
    '06_2021': 14,
    '07_2021': 15, 
    '08_2021': 16,  
    '09_2021': 17,  
    '10_2021': 18,  
    '11_2021': 19,  
    '12_2021': 20,  
    '01_2022': 21, 
    '02_2022':22,  
    '03_2022':23, 
    '04_2022':24,  
    '05_2022':25,
    '06_2022':26
}

WAVES_r = {
 1: '04_2020',
 2: '05_2020',
 3: '06_2020',
 4: '08_2020',
 5: '09_2020',
 6: '10_2020',
 7: '11_2020',
 8: '12_2020',
 9: '01_2021',
 10: '02_2021',
 11: '03_2021',
 12: '04_2021',
 13: '05_2021',
 14: '06_2021',
 15: '07_2021',
 16: '08_2021',
 17: '09_2021',
 18: '10_2021',
 19: '11_2021',
 20: '12_2021',
 21: '01_2022',
 22: '02_2022',
 23: '03_2022',
 24: '04_2022',
 25: '05_2022',
 26: '06_2022'}



labs_var= {
    
    'age_group8':  'age group',
    'fin_now3a':   'income',
    'fin_now4a':   'income4',
    'employed' :   'employment',
    'education4':  'education',
    'education3':  'education',
    'gender':      'gender',
    'settlement':  'settlement',
    'settlement4': 'settlement',
    'smoking_new':
    'smoking',
    'settlement_cur_num': 'settlement',
    'chronic_disease': 'chronic disease',
 'acute_disease': 'acute disease'}




labs= {
    'overall':['overall'],
    'fin_now3a': {1:r'$income_{low}$',
                  2:r'$income_{mid}$', 
                  3:r'$income_{high}$'},
    
    'employed' :  {1:'employed', 
                   2:'not employed'},
    
    'education4': {1:r'$edu_{low}$', 
                   2:r'$edu_{mid-low}$', 
                   3:r'$edu_{mid-high}$', 
                   4:r'$edu_{high}$'},
    
    'education3': {1:r'edu$_{low}$', 
                   2:r'edu$_{mid}$', 
                   3:r'edu$_{high}$'},
    
    'gender':     {1:r'female', 
                   2:r'male'},
    
    'settlement': {1:'1',
                   2:'2',
                   3:'3',
                   4:'4'},
    
    'settlement4': {1:'1',
                    2:'2',
                    3:'3',
                    4:'4'},
   
    'settlement_cur_num': {1:'capital', 
                           2:'urban', 
                           3:'rural'},
    
    'chronic_disease': {1:r'yes', 
                        2:r'no'},
   
    'age_group4':{0:'[0-30)', 
                  1:'[30-45)', 
                  2:'[45-60)', 
                  3:'[60+)'},
          
    'age_group7':{0:'[0-5)',
                  1:'[5-15)',
                  2:'[15-30)', 
                  3:'[30-45)',
                  4:'[45-60)',
                  5:'[60-70)',
                  6:'[70+)'},
    
    
    'age_group8':{0:'[0-5)', 
                  1:'[5-15)', 
                  2:'[15-30)', 
                  3:'[30-45)',
                  4:'[45-60)',
                  5:'[60-70)',
                  6:'[70-80)', 
                  7:'[80+)'},
  }
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
moodle setup skript
"""
# Import libs
import pandas as pd
import numpy as np
import os
import argparse
import configparser
import random
import string
from unidecode import unidecode
import unicodedata

# define object
class moodlesetup:
    """
    Manage the user and course setup of a moodle system.
    """
    def __init__(self,configfile='config.ini'):
        # Init directorys
        self.rootdir = os.getcwd()
        self.datadir = os.path.abspath(self.rootdir + '/data')
        self.exportdir = os.path.abspath(self.rootdir + '/export')
        
        if not os.path.exists(self.datadir):
            os.makedirs(self.datadir)
        if not os.path.exists(self.exportdir):
            os.makedirs(self.exportdir)
        
        # Init argparser
        self.parser = argparse.ArgumentParser(description='Manage the user and course setup of a moodle system.')
        self.parser.add_argument("-c", help="create csv-files for batch-moodle setup", action="store_true")

        self.args = self.parser.parse_args()

        # Initialize config file
        self.configfile = configfile
        if os.path.isfile(self.configfile):
            self.config = configparser.ConfigParser()
            self.config.read(self.configfile)

        else:
            self.config = configparser.ConfigParser()
            self.config['DEFAULT'] =        {
                                            'file'          : "schuelerliste.xls",                                           
                                            'seed'          : self.makepass(30),
                                            }
            with open(self.configfile, 'w') as savefile:
                self.config.write(savefile)
            print('created config file.')
            
        
        # execute tasks from given args
        if self.args.c:
            self.createtables()
            
    def makepass(self,n=5):
        """
        Generate an n-length random password
        """
        rainbow = (string.ascii_uppercase + string.ascii_lowercase + string.digits).replace('l','').replace('I','').replace('O','').replace('0','')
        return ''.join(random.choice(rainbow) for _ in range(n))
    
    def setseed(self,username):
        """
        Set the seed of the random numer generators
        """
        seedoffset = np.sum([ord(i) for i in self.config['DEFAULT']['seed']])
        random.seed(int(seedoffset + np.sum([ord(k) for k in username])))
        np.random.seed(int(seedoffset + np.sum([ord(k) for k in username])))
        
    def createtables(self):
        """
        Create and save user and course tables.
        """
        def remove_accents(input_str):
            nfkd_form = unicodedata.normalize('NFKD', input_str)
            return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).replace(chr(223) ,'ss')
        
        xl = pd.ExcelFile(os.path.abspath(self.datadir + '/schuelerliste.xls'))
        
        DF_liste = xl.parse(xl.sheet_names[0])[[u'Klasse', u'Name', u'Vorname']]
        
        DF_name = DF_liste.copy(deep=True)
        DF_name = DF_name[[u'Klasse', u'Name', u'Vorname']]
        DF_name = DF_name.rename(columns={'Name':'lastname','Vorname':'firstname','Klasse':'course1'})
        DF_name = DF_name.sort_values(['course1','lastname','firstname'])
        
        DF_name['password'] = np.nan
        DF_name['email'] = np.nan
        DF_name['group1'] = np.nan
        DF_name['cohort1'] = np.nan
        DF_name['autosubscribe'] = 1
        
        
        for i in DF_name.index:
            username = remove_accents(DF_name.loc[i,'firstname']).split(' ')[0].split('-')[0][:4].lower() + '_' + remove_accents(DF_name.loc[i,'lastname']).split(' ')[0].split('-')[0].lower()
            self.setseed(username)
            
            DF_name.loc[i,'username'] = username
            DF_name.loc[i,'password'] = self.makepass()
            DF_name.loc[i,'email'] = username + '@moodlebox.invalid'

        DF_name = DF_name[['username','password','firstname','lastname','email','course1','group1','cohort1','autosubscribe']]  
        DF_name.to_csv(self.exportdir+'/users.csv',index=False,sep=';', encoding="utf-8")
        
        DF_export = DF_name[['firstname','lastname','username','password','course1']]
        DF_export.to_csv(self.exportdir+'/print.csv',index=False,sep=';', encoding="utf-8")
        
        DF_courses = pd.DataFrame()#columns=['shortname','fullname','category','newsitems','theme','lang','format','enrolment_1','enrolment_1_role','role_student','role_teacher','templatecourse'])
        
        for i in DF_liste['Klasse'].unique():
            DF_courses = DF_courses.append(pd.DataFrame.from_dict({'shortname':i,'fullname':i,'category':'1','newsitems':'','theme':'','lang':'de','format':'','enrolment_1':'','enrolment_1_role':'','role_student':'','role_teacher':'','templatecourse':''},orient='index').T)
        
        DF_courses = DF_courses[['shortname','fullname','category','newsitems','theme','lang','format','enrolment_1','enrolment_1_role','role_student','role_teacher','templatecourse']]
        DF_courses.to_csv(self.exportdir+'/courses.csv',index=False,sep=';', encoding="utf-8")       

       
if __name__ == "__main__":
    MS = moodlesetup()

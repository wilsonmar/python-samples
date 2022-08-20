#!/usr/bin/env python3
# caiq-yaml-gen.py in https://github.com/wilsonmar/python-samples/blob/main/dataframe-lookup-multiline.py
# by Wilson Mar

# This reads a csv file (of CAIQ questions). 
# A value from that file is used ask a key to retrieve rows in the 
# Each For looking up metrics text associated,
# it builds an internal matrix by reading another CSV file.
# Text is carried over from previous row so the assumed value is displayed if blank.
# Output is filtered and formatted according to various boolean flags.

import csv
import os
from datetime import datetime 
from datetime import timezone

import pandas as pd  # after pip install pandas
# from csv import DictReader

# Install pandas package:
# See https://docs.python.org/3/library/subprocess.html#subprocess.check_call
package="pandas"
import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


this_program_name="caiq-yaml-gen.py"

# Capture date/time with local offset:
utc_dt = datetime.now(timezone.utc) # UTC time
local_dt = utc_dt.astimezone() # local time

now = datetime.now()  # Get tzname from https://www.timeanddate.com/time/zones/
local_now = now.astimezone()
local_tz = local_now.tzinfo
local_tzname = local_tz.tzname(local_now)


# User selections: TODO: choose in parameters within a GUI:
bool_output_console=True
bool_output_file=True
bool_output_table=False

print_category_list=False
bool_print_categories=True

bool_print_metrics=True
print_questions=True
print_annually=True
print_annually_only=False   # True to ignore lines with no annual in question
print_answers=True
print_answers_only=False     # True to ignore lines with no answers

stop_after_caiq_item=18

# This provides an example of how vendors of software can provide a customer-centric use of CAIQ.
# > PROTIP: Phrase what your customer can say in a CAIQ after installing your product. That would save them the agony of drafting paragraphs for their auditors. That's the customer-centric approach.

file_subject_text="for Consul users' auditors"
caiq_file_to_open='CAIQ4.0.1.consul.csv'
metrics_file_to_open='caiq-metrics-v1.csv'

#output_file_date=str(local_dt)[0:10]
output_file_date="2022-08-09"
output_file_prefix="CAIQ4.0.1.consul"
output_file_name=output_file_date+"-"+output_file_prefix+".md"  # Like 2021-05-12-caiq-yaml-gen.md
    # See https://courses.cs.washington.edu/courses/cse140/13wi/csv-parsing.html
# Validate run parameters:
output_file_delete_if_exists=True
# To avoid io.UnsupportedOperation: not writable, first verify if file exists
if os.path.exists(output_file_name) :
    print(f'*** file {output_file_name} being removed for rewrite ...')
    # No Prompt so this can run silent.
    os.remove(output_file_name)      
f = open(output_file_name, "a")

# Show what setting were selected for this run:
run_stats_line=""
if bool_output_file == True :
    if len(output_file_name) == 0 :
        run_stats_line=run_stats_line + "output_file_name not specified"
        bool_output_file=False

# Print only if there is an answer: Print only if there is no answer:
if print_annually == True :
    if print_annually_only == True :
        run_stats_line=run_stats_line + "Annual questions only"

if print_answers == True :
    if print_answers_only == True :
       run_stats_line=run_stats_line + "Only questions with answers"

# Internal formatting options:
category_format="###"  # "bold" or "Not"


# Output yaml heading:
if bool_output_console == True :
    print("*** "+ str(local_dt) +" "+ local_tzname +"\r\n")
    print("*** "+ run_stats_line +"\r\n")
if bool_output_file == True :
    f.write("---" +"\r\n")
    f.write("layout: post" +"\r\n")
    f.write("date: \""+ output_file_date +"\"\r\n")
    f.write("file: \""+ output_file_prefix  +"\"\r\n")
    f.write("title: \"CAIQ (Consensus Assessment Initiative Questionnaire) " + file_subject_text +".\"\r\n")
    f.write("excerpt: \""+ run_stats_line +" generated from file "+ caiq_file_to_open +" by "+ this_program_name +"\"\r\n")
    f.write("tags: [cloud, security, management, audit]" +"\r\n")
    f.write("---" +"\r\n")

#    f.write("\r\n")
#    f.write("<!-- At https://github.com/bomonike/fullest-stack/blob/main/python/caiq-yaml-gen/ -->\r\n")
#    f.write("\r\n")

    f.write("## Categories in the CAIQ : \r\n")
    f.write("\r\n")

# Output Category summary:
caiq_categories = {
    'A&A': 'Audit Assurance & Compliance',
    'AIS': 'Application & Interface Security',
    'BCR': 'Business Continuing Management & Operational Resilience',
    'CCC': 'Change Control & Configuration Management',
    'CEK': 'Cryptography, Encryption, and Key Management',
    'DCS': 'Datacenter Security',
    'DSP': 'Data Security & Privacy Lifecycle Management',
    'GRC': 'Governance, Risk Management, and Compliance',
    'HRS': 'Human Resources',
    'IAM': 'Identity & Access Management',
    'IPY': 'Interoperability & Portability',
    'IVS': 'Infrastructure & Virtualization Security',
    'LOG': 'Logging and Monitoring',
    'SEF': 'Security Incident Management, E-Discovery, and Cloud Forensics',
    'STA': 'Supply Chain Management, Transparancy, and Accountability',
    'TVM': 'Threat and Vulnerability Management',
    'UEM': 'Universal Endpoint Management'
    }
    # TODO: UEM DEFINITION: Unified Endpoint Management (UEM) allows IT to manage, secure, and deploy corporate resources and applications on any device from a single console. UEM “unifies” legacy mobile device management (MDM) by incorporating IoT and other new device technologies.
if print_category_list == True :
    for key, value in caiq_categories.items():
        print_line="1. <a href=\"#"+ key +"-\"><tt>"+ key +"</tt></a> = "+ value
        if bool_output_console == True :
            print(f'{print_line}')
        if bool_output_file == True :
            f.write(f'{print_line} \r\n')
    if bool_output_console == True :
        print("\r\n---------")
    if bool_output_file == True :
        f.write("\r\n<hr />\r\n")


if bool_print_metrics == True :
   # pd=pandas, df=dataframe (table) instead of default encoding="utf-8" :
   df = pd.read_csv(metrics_file_to_open, encoding="ISO-8859-1", sep = ",")
      # Alternately, into dict: a = pd.read_csv("File1.txt", delimiter=" ", header = None).to_dict()[0]
   # print(df)  # display entire dataframe. Alternately: df.head()
   # print(pd.options.display.max_rows) 
   df.set_index("_CCM_ID", inplace = True)
       # See https://pandas.pydata.org/docs/user_guide/indexing.html#indexing
   if bool_output_console == True :
      print( "*** "+ str(len(df.index)) +" rows (excluding title row) in dataframe "+ metrics_file_to_open )
         # Alternately, print(pd.options.display.max_rows) 

   # TODO: Print list of CCM metrics described at https://cloudsecurityalliance.org/artifacts/metrics-and-measurements-for-the-csa-ccm/ and PDF downloaded from https://cloudsecurityalliance.org/download/artifacts/metrics-and-measurements-for-the-csa-ccm/


# Output yaml heading and table heading:
if bool_output_file == True :
    f.write("\r\n")
    f.write("## "+ run_stats_line +" in the CAIQ "+ file_subject_text +" (by Category)\r\n")
    f.write("\r\n")
    if bool_output_table == True :
        f.write('<table border="1" cellpadding="4" cellspacing="0">\r\n')
        f.write('<tr valign="bottom"><th> CAIQ Item & Title </th><th> Question </th><th> Answer </th></tr>\r\n')
        f.write("\r\n")


with open(caiq_file_to_open, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    caiq_rows_read = 0
    caiq_rows_printed = 0
    prev_first_qid_chars=""
    metric_rows_printed = 0
    prev_caiq_ccm_id=""
    
    category_lines_out=0
    prev_title=""  # Def for next row.

    for row in csv_reader:
        if caiq_rows_read == 0:
            print(f'*** Column names are {", ".join(row)}')
            #  ID, _QID, _Title, _Question, _Answer_ID, _Answer
            # WARNING: Retrieving first column (ID) causes an error.
            caiq_rows_read += 1

        # Rest of lines: Get first 3 characters of _QID for Categories:
        first_qid_chars=row["_QID"][0:3]   # such as "A&A"
        caiq_ccm_id=row["_QID"][0:6]       # such as "A&A-01" to lookup metric 
        
        bool_print_caiq_line=True   # starting with all lines unless restricted.

        # See https://stackoverflow.com/questions/23866442/how-to-implement-efficient-filtering-logic-in-python
        if (row["_Question"].find('annual') != -1) :  # NOT FOUND
            if print_annually_only == True :
                bool_print_caiq_line=False
    
        if len(row["_Answer"]) == 0 and len(row["_Answer_ID"]) == 0 :  # Answer NOT present in line:
            if print_answers_only == True :  
                bool_print_caiq_line=False   # ignore lines with no answers
    
        # Print only if there is an answer: Print only if there is no answer:
        # if print_filter == "all" or len(row["_Answer"]) > 0 :
        if bool_print_caiq_line == True :
            caiq_rows_printed += 1
            if caiq_rows_printed < 10 :
               line_prefix="   "  # 3 spaces
            elif caiq_rows_printed < 100 :
               line_prefix="    "  # 4 spaces
            else:  # more than 999:
               line_prefix="     "  # 5 spaces

            # TODO: Instead Lookup CategoryText & CCM from csv file?
            # Lookup CategoryText from in-code table:
            if bool_print_categories == True :
                if first_qid_chars != prev_first_qid_chars :

                    # For GitHub Markdown weirdness:x
                    if category_lines_out <= 1 :  # Except first line 
                        category_prefix=""       # for GitHub Markdown weirdness
                    else:
                        category_prefix=line_prefix

                    category_text = caiq_categories[first_qid_chars]
                    category_line='<a name="'+ first_qid_chars +'-"></a>\r\n'
                    if bool_output_console == True :
                        print("\r\n"+ category_prefix+category_line+"\r\n")
                    if bool_output_file == True :
                        if bool_output_table == True :
                            f.write('\r\n<tr valign="top"><td colspan="4">' +category_line )
                        else:
                            f.write("\r\n"+ category_prefix + category_line)

                    if category_format == "bold" :
                        category_display = category_prefix+"<strong>"+ first_qid_chars +" = "+ category_text + "</strong>"
                    else:
                        category_display = category_prefix+"### "+ first_qid_chars +" = "+ category_text

                    category_line="\r\n"+ category_display +"\r\n \r\n"
                    if bool_output_console == True :
                        print(category_line)
                    if bool_output_file == True :
                        if bool_output_table == True :
                            f.write("<strong>"+ first_qid_chars +" = "+ category_text + '</strong></td></tr>\r\n')
                        else:
                            f.write(category_line)

                    category_lines_out += 1
                    prev_first_qid_chars=first_qid_chars  # for next row.


            if bool_print_metrics == True :
                caiq_ccm_id=row["_QID"][0:6]       # such as "A&A-01" to lookup metric 
                metrics_line=""  # clear from previous.
                if caiq_ccm_id != prev_caiq_ccm_id :
                    try:
                        # TODO: If CCM_ID is a Series in dataframe (not unique):

                        metrics_line='<a name="'+ df.loc[caiq_ccm_id,'_Metric_ID'] +'"></a>'+ df.loc[caiq_ccm_id,'_Metric_ID'] +" CCM METRIC SLO: "+ str(df.loc[caiq_ccm_id,'_SLO']) +" <strong>" + df.loc[caiq_ccm_id,'_Metric_Title'] +"</strong> = " + df.loc[caiq_ccm_id,'_Metric_Desc']
                        if bool_output_console == True :
                            print("\r\n"+line_prefix+metrics_line +"\r\n")
                        if bool_output_file == True :
                            if bool_output_table == True :
                                f.write('<tr valign="top" colspan="4"><td>'+metrics_line+'</td></tr')
                            else:
                                f.write('\r\n\r\n'+line_prefix+'<table border="1" cellpadding="4" cellspacing="0"><tr valign="top"><td>'+ metrics_line +'</td></tr></table>\r\n')
                        metric_rows_printed += 1
                    except:
                        # FIX: error when more than one metric for a CAIQ CCM ID. AIS-07-M3 & AIS-07-M6
                        # TODO: Check in dataframe if response
                            # SEF-06         <a name="SEF-06-M1">CCM SEF-06-M1</a> MET...
                            # SEF-06         <a name="SEF-06-M2">CCM SEF-06-M2</a> MET...
                            # dtype: object
                        # TODO: Loop for multiple metrics per CAIQ item
                        if bool_output_console == True :
                            print(line_prefix+"*** No metric for "+ caiq_ccm_id )
                            quit
                    prev_caiq_ccm_id=caiq_ccm_id  # for next row.


            # If no title, get from previous row:
            if len(row["_Title"]) == 0 :
                caiq_title=prev_title
            else :
                caiq_title=row["_Title"]
            # Mix of ' and " works?
            title_line="\r\n"+ str(caiq_rows_printed) +'. <a name="'+ row["_QID"] +'"></a>'+ row["_QID"] +" - "+ caiq_title +"\r\n"
            if bool_output_console == True :
                print(title_line)
            if bool_output_file == True :
                if bool_output_table == True :
                    f.write('<tr valign="top"><td>'+ str(caiq_rows_printed) +'. <a href="#'+ row["_QID"] +'"></a>'+ row["_QID"] +" - "+ caiq_title )
                else:
                    f.write(title_line)

            if print_questions == True :
                question_text=line_prefix + row["_Question"]
                if bool_output_console == True :
                    print("\r\n"+question_text)
                if bool_output_file == True :
                    if bool_output_table == True :
                        f.write("</td><td> " + row["_Question"] )
                    else:
                        f.write("\r\n"+question_text)

            #if bool_output_table == True :
            #    f.write("</td><td> Y ")

            if print_answers == True :
                if len(row["_Answer_ID"]) != 0 :  # blank value
                    answer_text=row["_Answer_ID"] + " : "+ row["_Answer"]
                    answer_line=line_prefix+ "ANSWER : "+ answer_text +"\r\n"
                    if bool_output_console == True :
                        print("\r\n"+answer_line)
                    if bool_output_file == True :
                        if bool_output_table == True :
                            f.write("</td><td>" + row["_Answer"] )
                        else:
                            f.write("\r\n"+answer_line)

            if bool_output_table == True :
                f.write('\r\n</td></tr>\r\n')

        caiq_rows_read += 1
#        if caiq_rows_read > stop_after_caiq_item :  # after AIS-07 at 18
#           quit
        if len(row["_Title"]) > 0 :
           prev_title=row["_Title"]  # Save for next row if title is blank

    last_stats_line=str(caiq_rows_read) +" CAIQ rows in, "+ str(category_lines_out) +" categories, "+ str(metric_rows_printed) +" CCM metrics. "+ str(caiq_rows_printed) +" questions+answers printed."
    if bool_output_console == True :
        print("*** "+ last_stats_line)
    if bool_output_file == True :
        if bool_output_table == True :
            f.write('</table>')
            f.write("\r\n")
        f.write("\r\n<-- "+ last_stats_line +" -->")

    # TODO: Display elapsed time for run:
    # from dateutil import relativedelta
    # relativedelta.relativedelta(end_time,start_time).seconds

    f.close()
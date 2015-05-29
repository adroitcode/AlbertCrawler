import datetime
import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sys
import time
import re
import traceback
import json

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#http://dev.mysql.com/doc/connector-python/en/connector-python-examples.html

def replace_all(my_string,change_this,to_this):
    while change_this in my_string:
        my_string = my_string.replace(change_this,to_this)
    return my_string

#Finds the index of the n'th character in a string
def index_of_nth(my_string,find_string,n):
    try:
        splits = my_string.split('find_string')
        index_count = 0
        for x in range(0,n - 1):
            split = splits[x]
            index_count += len(split) + len(find_string)
        return index_count
    except:
        return -1


def write_to_file(file_name,string_data):
    file = open(file_name,'w+')
    file.write(string_data)
    file.close()

main_data_dict = {'schools':[]}

def main():
    global main_data_dict
    #open db connection
    #connection = mysql.connector.connect(user='root', database='urlinq_new')
    #cursor = connection.cursor(dictionary=True)

    #query = ('SELECT * FROM event')
    #cursor.execute(query)

    #for event in cursor:
        #print event
       # pass

    #cursor.close()


    #Start selenium web driver
    driver_name = 'chromedriver.exe'
    #Determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    exe_path = os.path.join(application_path, driver_name)

    browser = webdriver.Chrome(executable_path=exe_path)

    #browser = webdriver.Firefox()

    #fp = webdriver.FirefoxProfile()
    #fp.set_preference("webdriver.load.strategy", "unstable")


    #browser = webdriver.Firefox(firefox_profile=fp)
    #browser = webdriver.PhantomJS()
    #browser = webdriver.PhantomJS()





    #browser.implicitly_wait(20) # seconds

    browser.get('https://admin.portal.nyu.edu/psp/paprod/EMPLOYEE/EMPL/h/?tab')
    time.sleep(3)

    user_id_input = browser.find_element_by_id('userid')
    user_id_input.send_keys('your net id here')

    password_input = browser.find_element_by_id('pwd')
    password_input.send_keys('your password here')
    password_input.submit()

    time.sleep(5)

    #Get the link from the student resources page
    student_center_soup = BeautifulSoup(browser.page_source)
    student_center_div = student_center_soup.find('div',{'id':'student_center_wsq'})
    student_center_a_element = student_center_div.find("a")
    student_center_link = student_center_a_element['href']
    student_center_link = student_center_link[2:-1]
    #print student_center_link
    #Take browser to student center_link
    browser.get("https://admin.portal.nyu.edu/psp/paprod/EMPLOYEE/EMPL" + student_center_link)
    #Let the page load
    time.sleep(5)


    browser.get('https://admin.portal.nyu.edu/psp/paprod/EMPLOYEE/CSSS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath=PORTAL_ROOT_OBJECT.NYU_STUDENT_CTR&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder')


    #Switch the the stupid ass frame
    browser.switch_to.default_content()
    content_frame = browser.find_element_by_name('TargetContent')
    browser.switch_to.frame(content_frame)


    search_for_classes_link = browser.find_element_by_id('DERIVED_SSS_SCR_SSS_LINK_ANCHOR2')
    search_for_classes_link.click()

    time.sleep(4)

    #Check the "spring 2015" checkbox

    spring_checkbox = browser.find_element_by_id('NYU_CLS_WRK_NYU_SPRING')
    spring_checkbox.click()

    time.sleep(4)

    #Loop through the table elements on the page class: SSSGROUPBOXLEFTWBO
    #Each table contains the school name with class: SSSGROUPBOXLEFTLABEL
    #and the departments for that school in class: SSSAZLINK

    school_tables = browser.find_elements_by_class_name('SSSGROUPBOXLEFTWBO')
    while len(school_tables) <= 0:
        school_tables = browser.find_elements_by_class_name('SSSGROUPBOXLEFTWBO')
        time.sleep(1)
        print "Waiting for school table elements."
        print "Length of school_tables: " + str(school_tables)


    for school_index in range(0,len(school_tables)):

        try:


            #RECLICK THE SPRING 2015 BUTTON
            #Check the "spring 2015" checkbox
            #print "CHECK BOX STATUS - SCHOOL PAGE"


            spring_checkbox = browser.find_element_by_id('NYU_CLS_WRK_NYU_SPRING')
            checkbox_checked = spring_checkbox.is_selected()
            #print checkbox_checked

            if not checkbox_checked:
                print "CHECKING THE FUCKING CHECKBOX - SCHPOOL"
                spring_checkbox.click()
                time.sleep(4)



            #Refind the school_tables because after going through a departments courses/classes,
            #we then come back to this page where the dom elements in the original school_tables
            #are not "attatched" to the current document anymore

            school_tables = browser.find_elements_by_class_name('SSSGROUPBOXLEFTWBO')
            while len(school_tables) <= 0:
                school_tables = browser.find_elements_by_class_name('SSSGROUPBOXLEFTWBO')
                time.sleep(1)
                print "Waiting for school table elements. in school loop"
                print "Length of school_tables: " + str(school_tables)


            school_table = school_tables[school_index]


            #Pull the school name

            school_name = school_table.find_elements_by_class_name('SSSGROUPBOXLEFTLABEL')[0].text
            #Remove the first and last space
            school_name = school_name[1:-1]
            #remove ' - Graduate' or ' - Undergraduate'
            school_name.replace(' - Graduate','')
            school_name.replace(' - Undergraduate','')
            data_dict = {'school_name':school_name,'departments':[]}



            departments_holder = school_table.find_element_by_class_name('SSSGROUPBOXLEFT')


            #Get all the department links SSSAZLINK
            departments = departments_holder.find_elements_by_tag_name('a')


            while len(departments) <= 0:
                departments = school_table.departments_holder.find_elements_by_tag_name('a')
                time.sleep(1)
                print "Waiting department elements"
                print "Length of departments: " + str(departments)
                print "school: " + school_name

            for department_index in range(0,len(departments)):
                department_dict = {'courses':[]}
                #RECLICK THE SPRING 2015 BUTTON
                #Check the "spring 2015" checkbox
                #if it is NOT checked
                spring_checkbox = browser.find_element_by_id('NYU_CLS_WRK_NYU_SPRING')
                #print "CHECK BOX STATUS - IN DEPARTMENTS LOOP"
                checkbox_checked = spring_checkbox.is_selected()
                #print checkbox_checked


                if not checkbox_checked:
                    print "CHECKING THE FUCKING CHECKBOX - DEP"
                    spring_checkbox.click()
                    time.sleep(4)


                #Repeat all these steps so the elements are
                #forsure attatched to the DOM

                school_tables = browser.find_elements_by_class_name('SSSGROUPBOXLEFTWBO')
                while len(school_tables) <= 0:
                    school_tables = browser.find_elements_by_class_name('SSSGROUPBOXLEFTWBO')
                    time.sleep(1)
                    print "Waiting for school table elements. In department loop"
                    print "Length of school_tables: " + str(school_tables)

                school_table = school_tables[school_index]

                departments_holder = school_table.find_element_by_class_name('SSSGROUPBOXLEFT')
                departments = departments_holder.find_elements_by_tag_name('a')
                department = departments[department_index]

                department_name = department.text
                #department_name looks like this: Ctr for Urban Sci and Progress (CUSP-GX)
                #so we need to remove the (text)
                department_name = department_name[0:department_name.index('(') - 1]
                department_name = replace_all(department_name,'\n',' ')

                department_dict['department_name'] = department_name
                #Go to the courses for this department
                department.click()

                time.sleep(4)
                #Get all the courses and loop through

                courses = browser.find_elements_by_class_name('PSGROUPBOXWBO')
                continue_loop = False
                while len(courses) <= 0:
                    courses = browser.find_elements_by_class_name('PSGROUPBOXWBO')
                    time.sleep(1)
                    print "Waiting for courses elements"
                    print "Length of courses: " + str(school_tables)

                    #check if this department simply as no courses
                    try:
                        class_count_span_text = browser.find_element_by_id("NYU_CLS_WRK_DESCR100").text
                        if 'Total Class Count: 0' in class_count_span_text:
                            print "This department doesnt have any fucking courses"
                            continue_loop = True
                            break
                    except:
                        print "class count page title not an element"

                if continue_loop:
                    clicked = False
                    while not clicked:
                        try:
                            browser.find_element_by_id('NYU_CLS_DERIVED_BACK').click()
                            clicked = True
                            print "SUCCESSFULLY CLICKED THE BACK BUTTON"
                        except:
                            print "COULD NOT CLICK THE BACK BUTTON. TRYING AGAIN"
                            print "department_name: " + department_name
                            time.sleep(1)
                    #If this department doesnt have any courses, lets just go back to school page
                    continue

                print str(len(courses)) + " COURSES IN " + department_name
                if len(courses) > 0:
                    time.sleep(1)
                    for course_index in range(0,len(courses)):
                        try:
                            course_dict = {'classes':[]}

                            courses = browser.find_elements_by_class_name('PSGROUPBOXWBO')
                            course = courses[course_index]
                            try:
                                #Try to click the "show more description link if it exists
                                show_more_description_link = course.find_element_by_xpath(".//a[contains(@href,'#')]")
                                show_more_description_link.click()
                                time.sleep(4)
                            except:
                                pass



                            #re get the course because selenium is fucking retarded
                            courses = browser.find_elements_by_class_name('PSGROUPBOXWBO')

                            while len(courses) <= 0:
                                school_tables = browser.find_elements_by_class_name('SSSGROUPBOXLEFTWBO')
                                time.sleep(1)
                                print "Waiting for school table elements."
                                print "Length of school_tables: " + str(school_tables)

                            course = courses[course_index]




                            span_element = course.find_element_by_tag_name('span')



                            course_text = span_element.text


                            course_name_b_element_text = ''



                            try_count = 0
                            active = False
                            while not active:
                                try:
                                    course_name_b_element = span_element.find_element_by_tag_name('b')
                                    course_name_b_element_text = course_name_b_element.text
                                    active = True
                                except:
                                    try_count += 1
                                    if try_count > 5:
                                        print 'TRY COUNT IS 5'
                                        print 'LOOKING FOR THE FIRST B ELEMENT IN COURSE'
                                        course_name_b_element = course.find_element_by_tag_name('b')
                                        course_name_b_element_text = course_name_b_element.text

                                    time.sleep(1)
                                    print "ERROR GETTING THE COURSE NAME B ELEMENT"
                                    print "TRYING AGAIn"
                                    pass






                            #Course name is close to the start of course_text
                            #and is strucutured like this:
                            #CUSP-GX 6003 Innovation and Entrepreneurship for Urban Technologies | Innovation in Complex Urban Systems\n
                            #We only want the "Innovation and..." part for the course_name
                            #CUSP-GX 6003 is the course_tag
                            second_space_index = 0
                            #find the second space index. The space inbetween 6003 and Innovation
                            space_count = 0
                            for space_index in range(0,len(course_name_b_element_text)):
                                character = course_text[space_index]
                                if character == ' ':
                                    space_count += 1
                                if space_count == 2:
                                    second_space_index = space_index
                                    break

                            #Get the index of the first \n
                            #It seperats the course_name from the course_description
                            try:
                                first_new_line_index = course_text.index('\n')
                            except:
                                first_new_line_index = -1



                            #course_tag = course_text[0:second_space_index]
                            course_tag = course_name_b_element.text[0:second_space_index]
                            #course_name = course_text[second_space_index + 1:first_new_line_index]
                            course_name = replace_all(course_name_b_element_text,'\n',' ')
                            course_name = course_name.replace(course_tag + ' ','')


                            #If "less description for" is not in the string,
                            #then we want to just read until the end of the file (-1)
                            end_of_description_index = 0
                            try:
                                end_of_description_index = course_text.index('less description for')
                            except:
                                end_of_description_index = len(course_text)
                            course_description = course_text[first_new_line_index + 1: end_of_description_index]
                            course_description = course_description.replace(course_tag + ' ','')
                            course_description = replace_all(course_description,'\n',' ')


                            course_dict['course_tag'] = course_tag
                            course_dict['course_name'] = course_name
                            course_dict['course_description'] = course_description
                            #print "COURSE NAME"
                            #print course_name_string
                            #print "end course name string"





                            #Make the drop down appear for classes
                            course.find_element_by_class_name('PSHYPERLINK').click()
                            time.sleep(3)

                            #refind the course element after that click
                            courses = browser.find_elements_by_class_name('PSGROUPBOXWBO')
                            course = courses[course_index]

                            #classes = course.find_elements_by_class_name('PSLEVEL3SCROLLAREABODY')
                            #print "COURSE HTML"
                            #print course.get_attribute('innerHTML')

                            #.// get
                            classes = course.find_elements_by_xpath(".//div[contains(@id, 'win0divNYU_CLS_DERIVED_HTMLAREA3')]")
                            while len(classes) <= 0:
                                classes = course.find_elements_by_xpath(".//div[contains(@id, 'win0divNYU_CLS_DERIVED_HTMLAREA3')]")
                                time.sleep(1)
                                print "Waiting for classes to show up for course " + course_name
                                print "Length of classes: " + str(classes)

                            #Skip the first one
                            for class_box in classes:
                                try:
                                    class_dict = {}
                                    class_box_text = class_box.text
                                    class_box_text_parts = class_box_text.split('|')


                                    class_credits = 0
                                    #Find the section that contains the credits for this class (if any)
                                    for class_box_text_part in class_box_text_parts:
                                        if 'units' in class_box_text_part:
                                            class_credits = class_box_text_part[1:class_box_text_part.index('units') - 1]
                                            break

                                    class_number = ''
                                    #find the section that contains class#
                                    for class_box_text_part in class_box_text_parts:
                                        if 'Class#' in class_box_text_part:
                                            class_number = class_box_text_part[class_box_text_part.index('Class#') + 8:len(class_box_text_part) - 1]
                                            break


                                    #get the last part which usually contains something like this:
                                    # | Component: Seminar\n01/26/2015 - 05/11/2015 Thu 3.30 PM - 6.10 PM at TISC LC2
                                    # with Lukes, Steven\nNotes: Open to sophomores and higher. CAS students register first;
                                    # students from other schools can register on Friday, November 21. Sociology majors can enroll
                                    # under SOC-UA 935.001.
                                    last_class_text_part = class_box_text_parts[-1]
                                    class_location = ''
                                    class_professor_name = ''
                                    #Look for 'at ' with a space to ensure that 'at' is its own word,
                                    #not in another string like 'status'
                                    if 'at ' in last_class_text_part and 'with ' in last_class_text_part:
                                        at_index = last_class_text_part.index('at ')
                                        with_index = last_class_text_part.index('with ')
                                        class_location = last_class_text_part[at_index + 3:with_index - 1]
                                        with_till_end_string = last_class_text_part[with_index: len(last_class_text_part)]
                                        try:
                                            next_new_line_index = with_till_end_string.index('\n')
                                        except:
                                            next_new_line_index = len(with_till_end_string)

                                        #Find the next line after this
                                        class_professor_name = with_till_end_string[5:next_new_line_index]
                                        #If there are multiple professors, they will be split with a ;
                                        #We just want the first one for now to simplify this shit
                                        class_professor_name = class_professor_name.split(';')[0]
                                    elif 'with ' in last_class_text_part:
                                        with_index = last_class_text_part.index('with ')
                                        with_till_end_string = last_class_text_part[with_index: len(last_class_text_part)]
                                        try:
                                            next_new_line_index = with_till_end_string.index('\n')
                                        except:
                                            next_new_line_index = len(with_till_end_string)

                                        #Find the next line after this
                                        class_professor_name = with_till_end_string[5:next_new_line_index]
                                        #If there are multiple professors, they will be split with a ;
                                        #We just want the first one for now to simplify this shit
                                        class_professor_name = class_professor_name.split(';')[0]

                                    days_of_week = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
                                    class_datetime_string = ''
                                    #extract the date/s and time range for this class
                                    for day_of_week in days_of_week:
                                        first_day_index = 0
                                        if day_of_week in last_class_text_part:
                                            first_day_index = last_class_text_part.index(day_of_week)
                                            end_of_class_datetime_index = 0
                                            first_am_or_pm_index = 0
                                            if 'AM ' in last_class_text_part:
                                                first_am_or_pm_index = last_class_text_part.index('AM ')
                                            elif 'PM ' in last_class_text_part:
                                                first_am_or_pm_index = last_class_text_part.index('PM ')

                                            #cut last_class_text_part starting at first_am_or_pm_string until the end
                                            sub_string = last_class_text_part[first_am_or_pm_index + 2:-1]
                                            #find the index of the next AM or PM in the sub string
                                            if 'AM ' in sub_string:
                                                end_of_class_datetime_index = sub_string.index('AM ')
                                            elif 'PM ' in sub_string:
                                                end_of_class_datetime_index = sub_string.index('PM ')

                                            #Add the first AM or PM index to the end, because we want it to be
                                            #the index of the second AM or PM in last_class_text_part
                                            end_of_class_datetime_index += first_am_or_pm_index
                                            #add two to set the index after the AM or PM
                                            end_of_class_datetime_index += 4

                                            class_datetime_string = last_class_text_part[first_day_index:end_of_class_datetime_index]


                                            #Stop the forloop so we dont skip the first day
                                            break



                                    class_dict['class_name'] = class_box_text
                                    class_dict['class_credits'] = class_credits
                                    class_dict['class_number'] = class_number
                                    class_dict['class_location'] = class_location
                                    class_dict['class_professor_name'] = class_professor_name
                                    class_dict['class_datetime'] = class_datetime_string

                                    #print "CLASS CREDITS"
                                    #print class_credits

                                    #print 'CLASS NUMBER'
                                    #print class_number


                                    course_dict['classes'].append(class_dict)
                                except:

                                    print "Error getting class in course " + course_name
                                    print traceback.print_exc()
                                    print '---------------------------------------------'

                                    course_dict['classes'].append({'class_name':'ERROR'})

                            department_dict['courses'].append(course_dict)
                        except:
                            print "Error grabbing courses from school " + school_name + " and department " + department_name
                            print traceback.print_exc()
                            course_dict = {'course_name':'ERROR'}
                            department_dict['courses'].append(course_dict)

                    data_dict['departments'].append(department_dict)


                print json.dumps(data_dict)
                #after we are done extracting data from all courses/classes, go back to the
                #school page
                clicked = False
                while not clicked:
                    try:
                        browser.find_element_by_id('NYU_CLS_DERIVED_BACK').click()
                        clicked = True
                        print "SUCCESSFULLY CLICKED THE BACK BUTTON"
                    except:
                        print "COULD NOT CLICK THE BACK BUTTON. TRYING AGAIN"
                        print "department_name: " + department_name
                        time.sleep(1)

                time.sleep(10)


            main_data_dict['schools'].append(data_dict)
            print "Writing main JSON to data.txt"
            write_to_file('data.txt',json.dumps(main_data_dict))

        except:
            print 'ERROR LOOPING THROUGH SCHOOL'
            print traceback.print_exc()




    time.sleep(10)



    #close selenium browser
    browser.close()

    #connection.close()



main()
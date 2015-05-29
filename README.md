# AlbertCrawler
Gathers all school/department/course/class data as JSON from NYU Albert

Just replace "your netid here" and "your password here" on lines 90/93 and run, 

example of what the structured JSON data looks like:


{
  "schools": [
    {
      "school_name": "Center for Urban Science and Progress",
      "departments": [
        {
          "courses": [
            {
              "course_tag": "CUSP-GX 5007",
              "course_description": "Open only to students in the spring and/or summer semester(s). To register for this course, the student must obtain the written approval of his or her faculty adviser. Three (3) credits per semester. Students engage in individual research and specific projects in a selected field under the supervision of a member of the faculty and with the permission of the Deputy Director of Academics.",
              "classes": [
                {
                  "class_name": "CUSP-GX 5007 | 3 units | Class#: 24842 | Session: 1 01/26/2015 - 05/11/2015 | Section: 001\nClass Status: Open | Grading: CUSP Graded\nCourse Location: Washington Square | Component: Independent Study\n01/26/2015 - 05/11/2015",
                  "class_number": "24842",
                  "class_professor_name": "",
                  "class_credits": "3",
                  "class_location": "",
                  "class_datetime": ""
                }
              ],
              "course_name": "Independent Study"
            },
            ...


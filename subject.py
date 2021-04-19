class Subject:
    def __init__(self,
                 subject_code=None,
                 section=None,
                 course_name=None,
                 professor=None,
                 zoom=None):
        self.subject_code = subject_code
        self.section = section
        self.course_name = course_name
        self.professor = professor
        self.zoom = zoom

    def __str__(self):
        if not self.subject_code:
            print(
                'Invalid subject code. Will not print the rest of the information.'
            )
            return
        else:
            print()

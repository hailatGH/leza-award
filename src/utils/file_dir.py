def Users_Profile_Images(instance, filename):
    return '/'.join(['Media_Files', 'Users_Profile_Images', str(filename)])

def Candidate_Profile_Images(instance, filename):
    return '/'.join(['Media_Files', 'Candidate_Profile_Images', str(filename)])

def Category_Profile_Images(instance, filename):
    return '/'.join(['Media_Files', 'Category_Profile_Images', str(filename)])

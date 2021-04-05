from django.shortcuts import render, redirect
import dbConnectionFunctions as db
from datetime import date

def sponsorDashDisplay(request):

    class driver_applicant:
        def __init__(self, name, applicant_id):
            self.name = name
            self.applicant_id = applicant_id

    driver_application_list = []

    if (request.session['isViewing']):
        org_num = db.getOrgNo(request.session['tempEmail'])
    else:
        org_num = db.getOrgNo(request.session['email'])

    conn = db.getDB()
    cursor = db.getCursor(conn)

    query_applicants = "SELECT * FROM APPLICANT WHERE ORGID=%s"
    cursor.execute(query_applicants, (org_num,))
    result = cursor.fetchall()

    for x in result:
        temp_name = x[4]
        temp_id = x[0]

        temp_driver = driver_applicant(temp_name, temp_id)

        driver_application_list.append(temp_driver)

    cursor.close()
    conn.close()

    context = {'driver_application_list': driver_application_list, 'isSponsor': request.session['isSponsor'], 'isAdmin': request.session['isAdmin']}
    return render(request, 'sponsor_dash.html', context)

def sponsorViewApplicant(request, applicant_id):

    applicant_name = db.getUserName(db.getUserEmail(applicant_id))

    context = {'applicant_id': applicant_id, 'applicant_name': applicant_name}
    return render(request, 'view_application.html', context)

def sponsorAcceptApplicant(request, applicant_id):
    today = date.today()

    conn = db.getDB()
    cursor = db.getCursor(conn)

    query = "SELECT Email FROM APPLICANT WHERE ApplicantID=%s"
    cursor.execute(query, (applicant_id,))
    result = cursor.fetchone()

    for name in result:
            cursor.close()
            conn.close()
            applicant_email = name

    db.acceptApplicant(applicant_email, "Sponsor Accepted", db.getRandomPassword(), today.strftime("%Y-%m-%d"))

    response = redirect('/sponsor_dash/')
    return response

def sponsorRejectApplicant(request, applicant_id):
    today = date.today()
    
    conn = db.getDB()
    cursor = db.getCursor(conn)

    query = "SELECT Email FROM APPLICANT WHERE ApplicantID=%s"
    cursor.execute(query, (applicant_id,))
    result = cursor.fetchone()

    for name in result:
            cursor.close()
            conn.close()
            applicant_email = name

    db.rejectApplicant(applicant_email, "Sponsor Rejected", today.strftime("%Y-%m-%d"))

    response = redirect('/sponsor_dash/')
    return response
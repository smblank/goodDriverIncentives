from django.shortcuts import render, redirect
import dbConnectionFunctions as db
import datetime


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

    query_applicants = "SELECT * FROM APPLICANT WHERE OrgID=%s"
    cursor.execute(query_applicants, (org_num,))
    result = cursor.fetchall()

    for x in result:
        temp_name = x[4]
        temp_id = x[0]

        temp_driver = driver_applicant(temp_name, temp_id)

        driver_application_list.append(temp_driver)

    cursor.close()
    conn.close()

    context = {'driver_application_list': driver_application_list,
               'isSponsor': request.session['isSponsor'], 'isAdmin': request.session['isAdmin']}
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

    db.acceptApplicant(applicant_email, "Sponsor Accepted",
                       db.getRandomPassword(), today.strftime("%Y-%m-%d"))

    response = redirect('/sponsor_dash')
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

    db.rejectApplicant(applicant_email, "Sponsor Rejected",
                       today.strftime("%Y-%m-%d"))

    response = redirect('/sponsor_dash/')
    return response


def sponsorViewDrivers(request):
    # query driver database and get all for current sponsor
    class indiv_driver:
        def __init__(self, name, driver_id):
            self.name = name
            self.driver_id = driver_id

    driver_list = []

    org_num = db.getOrgNo(request.session['email'])

    conn = db.getDB()
    cursor = db.getCursor(conn)

    query_drivers = "SELECT * FROM USER INNER JOIN DRIVER_ORGS ON DRIVER_ORGS.UserID = USER.UserID WHERE OrgID=%s"
    cursor.execute(query_drivers, (org_num,))
    result = cursor.fetchall()

    for x in result:
        temp_name = x[1]
        temp_id = x[0]

        temp_driver = indiv_driver(temp_name, temp_id)

        driver_list.append(temp_driver)

    cursor.close()
    conn.close()

    context = {'driver_list': driver_list}
    return render(request, 'sponsor_view_drivers.html', context)


def sponsorChangePoints(request, driver_id):
    if request.method == 'POST':
        reason_id = request.POST.get('reason_id')
        sponsor_id = request.session['id']

        conn = db.getDB()
        cursor = db.getCursor(conn)

        query_driver_points = 'SELECT * FROM DRIVER INNER JOIN DRIVER_ORGS ON DRIVER.UserID = DRIVER_ORGS.UserID WHERE DRIVER.UserID = %s'
        cursor.execute(query_driver_points, (driver_id,))
        result = cursor.fetchone()
        original_points = result[4]
        print('original points: ', original_points)

        query_point_value = 'SELECT * FROM POINT_CHANGE_REASON WHERE ReasonID=%s'
        cursor.execute(query_point_value, (reason_id,))
        result = cursor.fetchone()
        num_points = result[2]

        if (request.session['isViewing']):
            orgNo = db.getOrgNo(request.session['tempEmail'])
        else:
            orgNo = db.getOrgNo(request.session['email'])

        query_change_point_total = 'UPDATE DRIVER_ORGS SET Points = Points + %s WHERE UserID = %s AND OrgID = %s'
        cursor.execute(query_change_point_total,
                       (num_points, driver_id, orgNo))

        cursor.execute(query_driver_points, (driver_id,))
        result = cursor.fetchone()
        after_points = result[4]
        print('after points: ', after_points)

        now = datetime.datetime.now()
        query_insert_point_change = 'INSERT INTO POINT_CHANGE (ChangeDate, ReasonID, TotalPoints, DriverID, SponsorID) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(query_insert_point_change, (now.strftime(
            '%Y-%m-%d'), reason_id, after_points, driver_id, request.session['id'],))

        # check if points where added and send to confirmation page
        if original_points + num_points == after_points:
            successful = True
        else:
            successful = False

        query_driver_name = 'SELECT * FROM USER INNER JOIN DRIVER ON DRIVER.UserID = USER.UserID WHERE USER.UserID=%s'
        cursor.execute(query_driver_name, (driver_id,))
        result = cursor.fetchone()
        driver_name = result[1]
        driver_email = result[2]

        cursor.close()
        conn.close()

        context = {'successful': successful, 'driver_name': driver_name, 'driver_email': driver_email, 'original_points': original_points, 'point_change': num_points,
                   'new_total': after_points}
        return render(request, 'change_points_confirmation.html', context)

    else:
        query_driver_name = 'SELECT * FROM USER INNER JOIN DRIVER ON DRIVER.UserID = USER.UserID WHERE USER.UserID=%s'

        conn = db.getDB()
        cursor = db.getCursor(conn)

        cursor.execute(query_driver_name, (driver_id,))
        result = cursor.fetchone()

        driver_name = result[1]
        driver_email = result[2]

        class point_reasons:
            def __init__(self, reason_id, reason_desc, reason_points):
                self.reason_id = reason_id
                self.reason_desc = reason_desc
                self.reason_points = reason_points

        reasons = []

        if (request.session['isViewing']):
            orgNo = db.getOrgNo(request.session['tempEmail'])
        else:
            orgNo = db.getOrgNo(request.session['email'])

        query_reasons = 'SELECT * FROM POINT_CHANGE_REASON WHERE OrgID=%s'

        cursor.execute(query_reasons, (orgNo,))
        result = cursor.fetchall()

        if result != None:
            for x in result:
                temp_reason_id = x[0]
                temp_reason_desc = x[1]
                temp_reason_points = x[2]

                temp_reason = point_reasons(
                    temp_reason_id, temp_reason_desc, temp_reason_points)

                reasons.append(temp_reason)

        cursor.close()
        conn.close()

        context = {'driver_name': driver_name,
                   'driver_id': driver_id, 'reason_list': reasons}
        return render(request, 'change_driver_points.html', context)

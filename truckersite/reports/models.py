from django.shortcuts import render
import dbConnectionFunctions as db

def exists(list, element):
    for elem in list:
        if elem == element:
            return True
        
    return False

def find(list, element):
    index = 0
    for elem in list:
        if elem == element:
            return index
        index += 1

    return -1

# Create your models here.
def getSponsorReport(request):
    driver = request.POST.get('driver')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    if (request.session['isViewing']):
        orgID = db.getOrgNo(request.session['tempEmail'])
    else:
        orgID = db.getOrgNo(request.session['email'])

    if (driver == 'all'):
        result = db.allDriverPointChangeReport(startDate, endDate, orgID)
    else:
        result = db.indvDriverPointChangeReport(startDate, endDate, orgID, driver)

    class PointChangeAtributes:
        def __init__(self):
            date = '00/00/00'
            pointChange = 0
            sponsor = 'none'
            reason = 'none'

    driverNames = []
    driverPoints = []
    pointChanges = []

    drivers = []

    for (driverName, pointTotal, changeDate, numPoints, sponsorID, reasonDesc) in result:
        if (not exists(driverNames, driverName)):
            driverNames.append(driverName)
            driverPoints.append(pointTotal)
            pointChanges.append([])

        i = find(driverNames, driverName)
        tempChange = PointChangeAtributes()
        tempChange.date = changeDate
        tempChange.pointChange = numPoints
        tempChange.sponsor = db.getUserName(db.getUserEmail(sponsorID))
        tempChange.reason = reasonDesc
        pointChanges[i].append(tempChange)

    drivers = zip(driverNames, driverPoints, pointChanges)

    context = {
        'startDate': startDate,
        'endDate': endDate,
        'drivers': drivers,
    }

    return render(request, 'sponsor_generate_report.html', context)

def getAuditLog(request):
    reportType = request.POST.get('logType')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    if (reportType == 'applications'):
        result = db.driverApplicationsReport(startDate, endDate)

        class Applicant:
            def __init__(self):
                date = '00/00/00'
                orgName = 0
                name = 'none'
                accepted = False
                reason = 'none'

        applicants = []

        for (applicantDate, orgID, applicantName, isAccepted, reason) in result:
            tempApplicant = Applicant()
            tempApplicant.date = applicantDate
            tempApplicant.orgName = db.getOrgName(orgID)
            tempApplicant.name = applicantName
            tempApplicant.acceptApplicant = isAccepted
            tempApplicant.reason = reason
            applicants.append(tempApplicant)

        context = {
            'startDate': startDate,
            'endDate': endDate,
            'applicants': applicants,
            'applications': True,
            'points': False,
            'passwords': False,
            'login': False
        }

    elif (reportType == 'points'):
        result = db.pointChangeReport(startDate, endDate)

        class PointChangeAtributes:
            def __init__(self):
                date = '00/00/00'
                orgName = 'none'
                pointChange = 0
                reason = 'none'

        
        driverNames = []
        pointChanges = []

        drivers = []

        for (driverName, changeDate, orgName, numPoints, reasonDesc) in result:
            if (not exists(driverNames, driverName)):
                driverNames.append(driverName)
                pointChanges.append([])

            i = find(driverNames, driverName)
            tempChange = PointChangeAtributes()
            tempChange.date = changeDate
            tempChange.orgName = orgName
            tempChange.pointChange = numPoints
            tempChange.reason = reasonDesc
            pointChanges[i].append(tempChange)

        drivers = zip (driverNames, pointChanges)

        context = {
            'startDate': startDate,
            'endDate': endDate,
            'drivers': drivers,
            'applications': False,
            'points': True,
            'passwords': False,
            'login': False
        }

    elif(reportType == 'passwords'):
        result = db.passwordChangeReport(startDate, endDate)

        class PassChange:
            def __init__(self):
                date = '00/00/00'
                changeType = 'none'

        userNames = []
        passChanges = []

        users = []

        for (userName, changeDate, changeType) in result:
            if (not exists(userNames, userName)):
                userNames.append(userName)
                passChanges.append([])

            i = find(userNames, userName)
            tempChange = PassChange()
            tempChange.date = changeDate
            tempChange.changeType = changeType
            passChanges[i].append(tempChange)

        users = zip (userNames, passChanges)

        context = {
            'startDate': startDate,
            'endDate': endDate,
            'users': users,
            'applications': False,
            'points': False,
            'passwords': True,
            'login': False
        }

    #FIXME: result is not being read in?
    else:
        result = db.loginAttemptsReport(startDate, endDate)

        class LoginAttempt:
            def __init__(self):
                date = '00/00/00'
                succeeded = False

        userEmails = []
        attempts = []

        users = []

        for (userEmail, attemptDate, succeeded) in result:
            if (not exists(userEmails, userEmail)):
                userEmails.append(userEmail)
                attempts.append([])

            i = find(userEmails, userEmail)
            tempLogin = LoginAttempt()
            tempLogin.date = attemptDate
            tempLogin.succeeded = succeeded
            attempts[i].append(tempLogin)

        users = zip (userEmails, attempts)

        context = {
            'startDate': startDate,
            'endDate': endDate,
            'users': users,
            'applications': False,
            'points': False,
            'passwords': False,
            'login': True
        }


    return render(request, 'audit_log.html', context)

def getInvoice(request):
    orgID = request.POST.get('org')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    if (orgID == 'all'):
        result = db.allSponsorInvoice(startDate, endDate)
    else:
        result = db.indvSponsorInvoice(startDate, endDate, orgID)

    class InvoiceItem:
        def __init__(self):
            date = '00/00/00'
            driver = 'none'
            cost = 0

    orgNames = []
    invoices = []
    costs = []

    orgs = []

    for (orgName, orderDate, driverName, price, qty) in result:
        if (not exists(orgNames, orgName)):
            orgNames.append(orgName)
            invoices.append([])
            costs.append(0)

        i = find(orgNames, orgName)
        tempItem = InvoiceItem()
        tempItem.date = orderDate
        tempItem.driver = driverName
        tempItem.cost = price
        invoices[i].append(tempItem)
        costs[i] += price * qty

    orgs = zip (orgNames, invoices, costs)

    context = {
        'startDate': startDate,
        'endDate': endDate,
        'orgs': orgs,
    }


    return render(request, 'invoice.html', context)

def getDriverSales(request):
    orgID = request.POST.get('org')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    detailed = request.POST.get('detail')

    if detailed == 'on':
        details = True

        if (orgID == 'all'):
            result = db.driverSaleReport(startDate, endDate, details, -1, db.getUserID(request.session['email']))
        else:
            result = db.driverSaleReport(startDate, endDate, details, orgID, db.getUserID(request.session['email']))

        class Product:
            def __init__(self):
                name = ""
                qty = 0
                price = 0

        class DriverOrder:
            def __init__(self):
                id = -1
                date = '00/00/00'
                products = []
                totalCost = 0

        driver = ""
        orgNames = []
        orders = []
        orderIDs = []

        orgs = []

        for (driverName, orgName, orderID, orderDate, productName, qty, price) in result:
            driver = driverName
            if (not exists(orgNames, orgName)):
                orgNames.append(orgName)
                orders.append([])

            i = find(orgNames, orgName)
            if (not exists(orderIDs, orderID)):
                orderIDs.append(orderID)
                tempOrder = DriverOrder()
                tempOrder.id = orderID
                tempOrder.date = orderDate
                orders[i].append(tempOrder)

            tempProduct = Product()
            tempProduct.name = productName
            tempProduct.qty = qty
            tempProduct.price = price
            orders[i].products.append(tempProduct)
            orders[i].totalCost += price * qty

        orgs = zip (orgNames, orders)

    else:
        details = False

        if (orgID == 'all'):
            result = db.driverSaleReport(startDate, endDate, details, -1, db.getUserID(request.session['email']))
        else:
            result = db.driverSaleReport(startDate, endDate, details, orgID, db.getUserID(request.session['email']))

        class DriverOrder:
            def __init__(self):
                id = -1
                date = '00/00/00'
                totalCost = 0

        driver = ""
        orgNames = []
        orders = []
        orderIDs = []

        orgs = []

        for (driverName, orgName, orderID, orderDate, qty, price) in result:
            driver = driverName
            if (not exists(orgNames, orgName)):
                orgNames.append(orgName)
                orders.append([])

            i = find(orgNames, orgName)
            if (not exists(orderIDs, orderID)):
                orderIDs.append(orderID)
                tempOrder = DriverOrder()
                tempOrder.id = orderID
                tempOrder.date = orderDate
                orders[i].append(tempOrder)

            orders[i].totalCost += price * qty

        orgs = zip (orgNames, orders)

    context = {
        'startDate': startDate,
        'endDate': endDate,
        'orgs': orgs,
        'driverName': driver,
        'detailed': details
    }


    return render(request, 'sales_by_driver.html', context)

def getSponsorSales(request):
    orgID = request.POST.get('sponsor')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    detailed = request.POST.get('detail')
    driver = request.POST.get('driver')

    if detailed == 'on':
        details = True

        if (orgID == 'all'):
            result = db.allSponsorSaleReport(startDate, endDate, details)
        else:
            if (driver == 'all'):
                result = db.indvSponsorSaleReport(startDate, endDate, details, -1, orgID)
            else:
                result = db.indvSponsorSaleReport(startDate, endDate, details, db.getUserID(driver), orgID)

        class Product:
            def __init__(self):
                name = ""
                qty = 0
                price = 0

        class DriverOrder:
            def __init__(self):
                id = -1
                date = '00/00/00'
                driver = ""
                products = []
                totalCost = 0

        orgNames = []
        orders = []
        orderIDs = []

        orgs = []

        for (orgName, orderID, orderDate, driverName, productName, qty, price) in result:
            if (not exists(orgNames, orgName)):
                orgNames.append(orgName)
                orders.append([])

            i = find(orgNames, orgName)
            if (not exists(orderIDs, orderID)):
                orderIDs.append(orderID)
                tempOrder = DriverOrder()
                tempOrder.id = orderID
                tempOrder.driver = driverName
                tempOrder.date = orderDate
                orders[i].append(tempOrder)

            tempProduct = Product()
            tempProduct.name = productName
            tempProduct.qty = qty
            tempProduct.price = price
            orders[i].products.append(tempProduct)
            orders[i].totalCost += price * qty

        orgs = zip (orgNames, orders)

    else:
        details = False

        if (orgID == 'all'):
            result = db.allSponsorSaleReport(startDate, endDate, details)
        else:
            if (driver == 'all'):
                result = db.indvSponsorSaleReport(startDate, endDate, details, -1, orgID)
            else:
                result = db.indvSponsorSaleReport(startDate, endDate, details, db.getUserID(driver), orgID)

        class DriverOrder:
            def __init__(self):
                id = -1
                date = '00/00/00'
                driver = ""
                totalCost = 0

        orgNames = []
        orders = []
        orderIDs = []

        orgs = []

        for (orgName, orderID, orderDate, driverName, qty, price) in result:
            driver = driverName
            if (not exists(orgNames, orgName)):
                orgNames.append(orgName)
                orders.append([])

            i = find(orgNames, orgName)
            if (not exists(orderIDs, orderID)):
                orderIDs.append(orderID)
                tempOrder = DriverOrder()
                tempOrder.id = orderID
                tempOrder.driver = driverName
                tempOrder.date = orderDate
                orders[i].append(tempOrder)

            orders[i].totalCost += price * qty

        orgs = zip (orgNames, orders)

    context = {
        'startDate': startDate,
        'endDate': endDate,
        'orgs': orgs,
        'detailed': details
    }


    return render(request, 'sales_by_sponsor.html', context)
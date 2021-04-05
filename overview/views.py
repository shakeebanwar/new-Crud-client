from django.shortcuts import render, reverse
from django.views import View
import calendar
from calendar import HTMLCalendar
from overview.models import Booking
from organization.models import Office, Organization
from users.models import Account
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from datetime import datetime, timedelta, date
import pytz
from django.db.models import Q, Count, F
import pdb

class CustomHTMLCalender(HTMLCalendar):
    cssclasses_weekday_head = ["custom_class" for style in
                  calendar.HTMLCalendar.cssclasses_weekday_head]
    
    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            return self.date_cell(cssclass, day)
        return self.no_date_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(CustomHTMLCalender, self).formatmonth(year, month)

    # def group_by_day(self, workouts):
    #     field = lambda workout: workout.performed_at.day
    #     return dict(
    #         [(day, list(items)) for day, items in groupby(workouts, field)]
    #     )
    
    def date_cell(self, cssclass, date):
        return '<td class="%s"><a href=/overview/{0}/{1}/{2}>%s</a></td>'.format(self.year,self.month,date) % (cssclass, date)

    def no_date_cell(self, cssclass, date):
        return '<td class="%s">%s</td>'.format(self.year,self.month,date) % (cssclass, date)
# TODO add redirects if setup from org, office or team is not done
@login_required
def overview_view(request, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day):
    context = {}
    context['year'] = year
    context['month'] = month
    context['day'] = day

    # Get current year
    day1 = datetime(year, month, day)
    context['day1'] = day1.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
    context['day2'] = day1 + timedelta(days=1)
    context['day3'] = day1 + timedelta(days=2)
    context['day4'] = day1 + timedelta(days=3)
    context['day5'] = day1 + timedelta(days=4)

    # Product context for calendar buttons
    # Previous Month
    last_day_current_month = context['day1'].replace(day=1)
    lastMonth = last_day_current_month - timedelta(days=1)
    context['lastMonth'] = lastMonth
    # Next Month
    nextMonth = lastMonth + timedelta(days=32)
    context['nextMonth'] = nextMonth.replace(day=1)
    # Today
    context['today'] = datetime.today()

    # create a calendar
    # context['calendar'] = HTMLCalendar().formatmonth(
    #     year,
    #     month)
    # my_workouts = Workouts.objects.order_by('my_date').filter(my_date__year=year, my_date__month=month)
    context['calendar']  = CustomHTMLCalender().formatmonth(year, month)

    if request.method == 'GET':

        if 'term' in request.GET:
            query_set_full_names = Account.objects.filter(organization_id=request.user.organization_id).filter(
                full_name__icontains=request.GET.get('term'))
            full_names = []
            for full_name in query_set_full_names:
                full_names.append(full_name.full_name)
            return JsonResponse(full_names, safe=False)

        # if user_id != None:
        #     context['bookings1'] = Booking.objects.filter(
        #         Q(organization_id=request.user.organization_id) & Q(booking_time__exact=context['day1']) & Q(account_id = user_id))
        #     context['offices'] = Office.objects.filter(organization_id__exact=request.user.organization_id)
        #
        #
        #     all_accounts = Account.objects.filter(organization_id=request.user.organization_id)
        #     context['non_bookings1'] = all_accounts.exclude(id__in=context['bookings1'].values('account_id'))
        #
        #     current_location = Booking.objects.filter(account_id=request.user.id).filter(
        #         booking_time__exact=context['day1'])
        #     all_locations = Office.objects.filter(organization_id=request.user.organization_id)
        #
        #     if not current_location:
        #         current_location = {'not_indicated': 'Not indicated'}
        #         other_locations = all_locations
        #     else:
        #         other_locations = all_locations.exclude(id=current_location.values('office_id')[0]['office_id'])
        #         current_location = Office.objects.filter(id=current_location.values('office_id')[0]['office_id'])
        #
        #     context['other_locations'] = other_locations
        #     context['current_location'] = current_location
        #
        #
        #     return render(request, 'overview/overview.html', context)

        else:
            context['bookings1'] = Booking.objects.filter(
                Q(organization_id=request.user.organization_id) & Q(booking_time__exact=context['day1']))
            context['bookings2'] = Booking.objects.filter(
                Q(organization_id=request.user.organization_id) & Q(booking_time__exact=context['day2']))
            context['bookings3'] = Booking.objects.filter(
                Q(organization_id=request.user.organization_id) & Q(booking_time__exact=context['day3']))
            context['bookings4'] = Booking.objects.filter(
                Q(organization_id=request.user.organization_id) & Q(booking_time__exact=context['day4']))
            context['bookings5'] = Booking.objects.filter(
                Q(organization_id=request.user.organization_id) & Q(booking_time__exact=context['day5']))
            context['offices'] = Office.objects.filter(organization_id__exact=request.user.organization_id)

            # Excluding those users within an organization that have a booking to show not indicates ones without having to put them into the db all the time
            all_accounts = Account.objects.filter(organization_id=request.user.organization_id)
            context['non_bookings1'] = all_accounts.exclude(id__in=context['bookings1'].values('account_id'))
            context['non_bookings2'] = all_accounts.exclude(id__in=context['bookings2'].values('account_id'))


            # BookingForm implementation
            #Relevant for all days
            all_locations = Office.objects.filter(organization_id=request.user.organization_id)

            # Day 1
            current_location1 = Booking.objects.filter(account_id=request.user.id).filter(
                booking_time__exact=context['day1'])

            if not current_location1:
                context['current_location1'] = {'not_indicated': 'Not indicated'}
                context['other_locations1'] = all_locations
            else:
                context['other_locations1'] = all_locations.exclude(
                    id=current_location1.values('office_id')[0]['office_id'])
                context['current_location1'] = Office.objects.filter(
                    id=current_location1.values('office_id')[0]['office_id'])

            # Getting data of office availabilities
            spots_with_bookings1 = Booking.objects.filter(organization_id=request.user.organization_id).filter(booking_time__exact=context['day1']).values('office_id', 'office__office_capacity', 'office__office_name')
            spots_with_bookings1 = spots_with_bookings1.annotate(office_bookings1=Count('office_id'))
            context['spots_with_bookings1'] = spots_with_bookings1.annotate(remaining_spots=F('office__office_capacity') - F('office_bookings1'))
            context['spots_without_bookings1'] = Office.objects.filter(organization_id=request.user.organization_id).exclude(id__in=context['spots_with_bookings1'].values('office_id'))
            print(context['spots_with_bookings1'])
            # print(context['spots_without_bookings1'].values('id'))
            print(context['spots_without_bookings1'].values())

            # Day 2
            current_location2 = Booking.objects.filter(account_id=request.user.id).filter(
                booking_time__exact=context['day2'])

            if not current_location2:
                context['current_location2'] = {'not_indicated': 'Not indicated'}
                context['other_locations2'] = all_locations
            else:
                context['other_locations2'] = all_locations.exclude(
                    id=current_location2.values('office_id')[0]['office_id'])
                context['current_location2'] = Office.objects.filter(
                    id=current_location2.values('office_id')[0]['office_id'])

            return render(request, 'overview/overview.html', context)

    if request.method == 'POST':
        office_id1 = request.POST.get('office_id1')
        office_id2 = request.POST.get('office_id2')

        if office_id1:

            # Day 1
            if int(office_id1) == 1:
                location = 'H'
            else:
                location = 'O'

            if not Booking.objects.filter(account_id=request.user.id).filter(booking_time=context['day1']):
                Booking.objects.create(account_id=request.user.id, booking_time=context['day1'], location=location,
                                       organization_id=request.user.organization_id, office_id=office_id1)
            else:
                # TODO Implement select_for_update
                Booking.objects.filter(account_id=request.user.id).filter(booking_time=context['day1']).update(
                    location=location, office_id=office_id1)

            return HttpResponseRedirect(reverse('overview',
                                                kwargs={'year': context['day1'].year, 'month': context['day1'].month,
                                                        'day': context['day1'].day}))

        elif office_id2:

            # Day 2
            if int(office_id2) == 1:
                location = 'H'
            else:
                location = 'O'

            if not Booking.objects.filter(account_id=request.user.id).filter(booking_time=context['day2']):
                Booking.objects.create(account_id=request.user.id, booking_time=context['day2'], location=location,
                                       organization_id=request.user.organization_id, office_id=office_id2)
            else:
                # TODO Implement select_for_update
                Booking.objects.filter(account_id=request.user.id).filter(booking_time=context['day2']).update(
                    location=location, office_id=office_id2)

            return HttpResponseRedirect(reverse('overview',
                                                kwargs={'year': context['day1'].year, 'month': context['day1'].month,
                                                        'day': context['day1'].day}))

        return HttpResponseRedirect(reverse('overview',
                                            kwargs={'year': context['day1'].year, 'month': context['day1'].month,
                                                    'day': context['day1'].day}))

    return render(request, 'overview/overview.html')

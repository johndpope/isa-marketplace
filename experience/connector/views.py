from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import requests
from connector.status_codes import *

@csrf_exempt
@require_http_methods(["GET"])
def home():
    return  JsonResponse({}, status=HTTP_200_OK)

@csrf_exempt
@require_http_methods(["POST"])
def authenticate_user(request):
    data = json.loads(request.body.decode("utf-8"))
    url = authenticate_user_url(username, password)
    resp = requests.post(url)
    if resp.status == HTTP_202_ACCEPTED:
        return JsonResponse({'message': 'User authenticated'}, status=HTTP_202_ACCEPTED)
    else:
        return JsonResponse({'message': 'Invalid Login'}, status=HTTP_401_UNAUTHORIZED)

@csrf_exempt
@require_http_methods(["GET"])
def get_ride(requst, id):
    url = "http://models:8000/" + "api/v1/ride/ride/" + id +"/"
    resp = requests.get(url)
    if resp.status_code == HTTP_200_OK:
        data = resp.json();
        return JsonResponse({'message': 'Ride found', "data": data}, status=HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Ride not found'}, status=HTTP_401_UNAUTHORIZED)

@csrf_exempt
@require_http_methods(["GET"])
def user_rides(requst, id):
    url = "http://models:8000/" + "api/v1/accounts/user/" + id + "/rides/"
    resp = requests.get(url)
    if resp.status_code == HTTP_200_OK:
        data = resp.json();
        return JsonResponse({'message': 'Ride found', "data": data}, status=HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Ride not found'}, status=HTTP_401_UNAUTHORIZED)


@csrf_exempt
@require_http_methods(["PUT"])
def create_ride(request):
    """
    PUT http://experience:8001/create_ride/
    """
    data = json.loads(request.body.decode("utf-8"))
    # curl -H "Content-Type: application/json" -X PUT -d '{"driver":"1","open_seats":3, "departure": "2016-01-20 05:30"}' http://localhost:8000/api/v1/ride/ride/
    url = "http://models:8000/" + "api/v1/ride/ride/"
    resp = requests.put(url, data={"driver":data['driver'],"open_seats":data['open_seats'], "departure": data['departure']})

    new_ride = resp.json()['data']
    if resp.status_code == HTTP_201_CREATED:
        return JsonResponse({'message': 'Ride Created', 'status': str(HTTP_201_CREATED), 'ride_id': new_ride['ride_id'], 'open_seats': new_ride['open_seats'], 'departure': new_ride['departure']}}, status=HTTP_201_CREATED)
    else:
        return JsonResponse({'message': 'Ride not found'}, status=HTTP_401_UNAUTHORIZED)


# def create_ride(driver_id, open_seats, departure_time, ride_status):
#     resp = requests.get()

# @csrf_exempt
# @require_http_methods(["GET", "POST"])
# def ride(request, id):
#     if request.method == 'GET':
#         try:
#             ride = Ride.objects.get(pk=id)
#             driver = UserProfile.objects.get(pk=ride.driver.pk)
#             passengers = ride.passenger.all()
#             dropoffLocations = ride.dropoffLocation.all()
#             data = {'ride_status': str(ride.status), 'dropOffLocations': str(dropoffLocations), 'passengers': str(passengers), 'departure': str(ride.departure), 'open-seats': str(ride.openSeats), 'driver': str(driver), 'status': str(HTTP_200_OK)}
#             return JsonResponse(data, status=HTTP_200_OK)
#         except Ride.DoesNotExist:
#             data = {'message': 'ride with id ' + id + ' was not found.', 'status': str(HTTP_404_NOT_FOUND)}
#             return JsonResponse(data, status=HTTP_404_NOT_FOUND)
#     else:
#         data = json.loads(request.body.decode("utf-8"))
#         try:
#             ride = Ride.objects.get(pk=id)
#             if not data.get('driver', "") == "":
#                 driver = UserProfile.objects.get(pk=data['driver'])
#                 ride.driver = driver
#             if not data.get('open_seats', "") == "":
#                 ride.openSeats = data['open_seats']
#             if not data.get('departure', "") == "":
#                 ride.departure = data['departure']
#             if not data.get('ride_status', "") == "":
#                 ride.ride_status = data['ride_status']
#             ride.save()
#             data = {'status': str(HTTP_204_NO_CONTENT)}
#             return JsonResponse(data, status=HTTP_204_NO_CONTENT)
#         except UserProfile.DoesNotExist:
#             data = {'message': 'ride with id ' + id + ' was not found.', 'status': str(HTTP_404_NOT_FOUND)}
#             return JsonResponse(data, status=HTTP_404_NOT_FOUND)
#
# @csrf_exempt
# @require_http_methods(["PUT"])
# def create_ride(request):
#     data = json.loads(request.body.decode("utf-8"))
#     # driver = UserProfile.objects.get(user=request.user)
#     driver = UserProfile.objects.get(pk=data['driver'])
#     new_ride = Ride(driver=driver, openSeats=data['open_seats'], departure=data['departure'], status=0)
#     new_ride.save()
#     dataresult = {'status': str(HTTP_201_CREATED),'id': str(new_ride.id), 'open_seats': new_ride.openSeats, 'departure': new_ride.departure}
#     return JsonResponse(dataresult, status=HTTP_201_CREATED)
#
# @csrf_exempt
# @require_http_methods(["POST"])
# def delete_ride(request, id):
#     try:
#         ride = Ride.objects.get(pk=id)
#         ride.delete()
#         data = {'status': str(HTTP_204_NO_CONTENT)}
#         return JsonResponse(data, status=HTTP_204_NO_CONTENT)
#     except UserProfile.DoesNotExist:
#         data = {'message': 'ride with id ' + id + ' was not found.', 'status': str(HTTP_404_NOT_FOUND)}
#         return JsonResponse(data, status=HTTP_404_NOT_FOUND)
#
# @csrf_exempt
# @require_http_methods(["GET", "POST"])
# def ride_request(request, id):
#     if request.method == 'GET':
#         try:
#             riderequest = RideRequest.objects.get(pk=id)
#             data = {'ride': str(riderequest.ride.id), 'passenger': str(riderequest.passenger.id), 'driver-confirm': str(riderequest.driverConfirm), 'ride-confirm': str(riderequest.rideConfirm), 'status': str(HTTP_200_OK)}
#             return JsonResponse(data, status=HTTP_200_OK)
#         except Ride.DoesNotExist:
#             data = {'message': 'ride request with id ' + id + ' was not found.', 'status': str(HTTP_404_NOT_FOUND)}
#             return JsonResponse(data, status=HTTP_404_NOT_FOUND)
#     else:
#         html = "<html><body><h1>update ride</h1></body></html>"
#         return HttpResponse(html)
#
# @csrf_exempt
# @require_http_methods(["PUT"])
# def create_ride_request(request):
#     data = json.loads(request.body.decode("utf-8"))
#     ride = Ride.objects.get(pk=data['ride_id'])
#     passenger = UserProfile.objects.get(pk=data['passenger_id'])
#
#     new_ride_request = RideRequest.objects.create(ride=ride, passenger=passenger, driverConfirm=False, rideConfirm=False)
#     new_ride_request.save()
#     dataresult = {'status': str(HTTP_201_CREATED),'id': str(new_ride_request.id)}
#     return JsonResponse(dataresult, status=HTTP_201_CREATED)


# SERVICES  list
# GET
# - driver, open seats, departure time, status
# POST
# -

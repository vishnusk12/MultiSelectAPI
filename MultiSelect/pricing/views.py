'''
Created on Jan 16, 2017

@author: vishnu.sk
'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from pymongo import MongoClient
from .dbauth import DATABASE_ACCESS

prop_type = ['Single Family Residence', 'Condominium', 'Townhouse', 'All']
SpanType = ['last 1 Month', 'last 2 Month', 'last 3 Month', 'last 6 Month', 'last 12 Month']
PriceType = ['ClosePrice', 'ListPrice']
ListOffices = ['TheMLSonline.com']


@permission_classes((permissions.AllowAny,))
class PricingViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        Pricing Analysis

               API will return the number of sold homes/listings within few ranges of ClosePrice and ListPrice.

               ---

               type:
                 schema : { CountyData: { Margin: [], type: FeatureCollection, features: [] }, StateData: { Margin: [], type: FeatureCollection, features: [] }}
               parameters_strategy: merge
               omit_parameters:
                   - path
               parameters:
                   - name: Zip
                     description: It is the location/Zip in which the Property is listed/sold.
                     required: true
                     type: string
                     paramType: query
                     "enum": ['55044', '55429', '55306', '55079', '55040', '98391', '55343']
                     defaultValue: 55044
                   - name: ListOfficeName
                     description:  It is the Brokerage office.
                     required: true
                     type: string
                     paramType: query
                     defaultValue: TheMLSonline.com
                   - name: PropertyType
                     description: The kind of Property types that are sold.
                     required: true
                     type: string
                     paramType: query
                     "enum": ['All,Condominium', 'All,Condominium,Single Family Residence', 'All,Condominium,Single Family Residence,Townhouse','Single Family Residence', 'Condominium', 'Townhouse', 'All']
                     defaultValue: All,Condominium
                   - name: Price
                     description:  It is the Sold price or List price.
                     required: true
                     type: string
                     paramType: query
                     "enum" : ['ClosePrice', 'ListPrice']
                     defaultValue: ClosePrice
                   - name: Span
                     description: It is the time span in which the Total Transaction done in a particular time which calculates as '1M', '3M', '6M', '12M', '18M'.
                     required: true
                     paramType: query
                     "enum" : ['last 1 Month', 'last 2 Month', 'last 3 Month', 'last 6 Month', 'last 12 Month']
                     defaultValue: last 12 Month


               responseMessages:
                   - code: 401
                     message: Not authenticated
                   - code : 404
                     message: Not Found
                   - code : ERROR
                     message : Unknown Error

               consumes:
                   - application/json
                   - application/xml
               produces:
                   - application/json
                   - application/xml
        """
        try:
            if 'Zip' not in request.query_params:
                return Response({'status': 'ERROR', 'error':
                                 'INVALID_Zip'})
            elif 'ListOfficeName' not in request.query_params and request.query_params['ListOfficeName'] not in ListOffices:
                return Response({'status': 'ERROR', 'error':
                                 'INVALID_ListOfficeName'})
            elif 'PropertyType' not in request.query_params and request.query_params['PropertyType'] not in prop_type:
                return Response({'status': 'ERROR', 'error':
                                 'INVALID_Property_type'})
            elif 'Span' not in request.query_params and request.query_params['Span'] not in SpanType:
                return Response({'status': 'ERROR', 'error': 'INVALID_SPAN'})
            elif 'Price' not in request.query_params and request.query_params['Price'] not in PriceType:
                return Response({'status': 'ERROR', 'error': 'INVALID_Price'})
        except:
                return Response({'status': 'ERROR',
                                 'error': 'UnknownError'})
        req_zip = request.query_params['Zip']
        req_listoffice = request.query_params['ListOfficeName']
        req_span = request.query_params['Span']
        prop = request.query_params['PropertyType'].split(',')
        req_price = request.query_params['Price']
        zip = str(req_zip)
        span = str(req_span)
        listoffice = str(req_listoffice)
        price = str(req_price)
        db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
        db_client.pricing.authenticate(**DATABASE_ACCESS)
        dict_ = {}
        for PropertyType in prop:
            dict_.update({"performance_index."+PropertyType + "." + span + "." + price: 1})
        data = list(db_client.pricing.brokeragepricingstats.find({'_id': {"PostalCode": zip, "ListOfficeName": listoffice}}, dict_))
        result = data[0]['performance_index']
        return Response(result)

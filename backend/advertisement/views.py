from bitrix24 import BitrixError
from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Advertisement
from .serializers import AdvertisementModelSerializer
from .utils import bitrix_manager
from .tasks import avito_scrape_data


class AdvertisementModelViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementModelSerializer

    @swagger_auto_schema(manual_parameters=[
        Parameter(
            'url', IN_QUERY, 'URL to parse', type='str'
        ),
    ])
    @action(methods=['GET', ], detail=False, url_path='get_avito_ads', url_name='get_avito_ads')
    def get_avito_ads(self, request):
        url_to_parse = request.query_params.get('url')
        if url_to_parse:
            assert url_to_parse.startswith('https://www.avito.ru/')
            avito_scrape_data.delay(url_to_parse)
        return Response(data={"task": "created"}, status=status.HTTP_201_CREATED)

    @action(methods=['GET', ], detail=True, url_path='bitrix_add_deal', url_name='bitrix_add_deal')
    def bitrix_add_deal(self, request, pk=None):
        advertisement = self.get_object()
        with bitrix_manager() as bitrix:
            try:
                data = bitrix.callMethod('crm.deal.add', fields={
                    'TITLE': advertisement.title,
                    'TYPE_ID': advertisement.category,
                    'CURRENCY_ID': advertisement.currency,
                    'OPPORTUNITY': advertisement.price,
                    'BEGINDATE': advertisement.created.date,
                    'SOURCE_DESCRIPTION': advertisement.description,
                    'COMMENTS': advertisement.link,
                })
            except BitrixError as bexp:
                return Response(data={'error': bexp}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'data': data}, status=status.HTTP_201_CREATED)

    @action(methods=['GET', ], detail=False, url_path='bitrix_get_deals', url_name='bitrix_get_deals')
    def bitrix_get_deals(self, request):
        with bitrix_manager() as bitrix:
            try:
                data = bitrix.callMethod('crm.deal.list')
            except BitrixError as bexp:
                return Response(data={'error': bexp}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'data': data}, status=status.HTTP_200_OK)
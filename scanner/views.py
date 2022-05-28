import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from scanner.models import Scan, State
from scanner.serializers import ScanSerializer

from scanner.tasks import process_scan

logger = logging.getLogger('django')


@api_view(['GET', 'POST'])
def scan_list(request, format=None):
    logger.info(f'scan_list: called: method=[{request.method}], data:{request.data}.')
    if request.method == 'GET':
        scans = Scan.objects.all()
        serializer = ScanSerializer(scans, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ScanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['state'] not in [State.COM.label, State.RUN.label]:
                process_scan.apply_async(kwargs={"scan_id": serializer.data['id']})
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'DELETE'])
def scan_detail(request, id, format=None):
    logger.info(f'scan_detail: called: method=[{request.method}], scan_id=[{id}].')
    try:
        scan = Scan.objects.get(pk=id)
    except Scan.DoesNotExist:
        return Response(data=dict(id=id, state=State.NOT.label), status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ScanSerializer(scan)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        scan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Division, District, Upazilla, Union

@require_http_methods(["GET"])
def get_divisions(request):
    """Get all active divisions"""
    divisions = Division.objects.filter(is_active=True).values('id', 'name', 'name_en')
    return JsonResponse({'divisions': list(divisions)})

@require_http_methods(["GET"])
def get_districts(request):
    """Get districts by division ID"""
    division_id = request.GET.get('division_id')
    if not division_id:
        return JsonResponse({'error': 'division_id is required'}, status=400)
    
    districts = District.objects.filter(
        division_id=division_id, 
        is_active=True
    ).values('id', 'name', 'name_en')
    return JsonResponse({'districts': list(districts)})

@require_http_methods(["GET"])
def get_upazillas(request):
    """Get upazillas by district ID"""
    district_id = request.GET.get('district_id')
    if not district_id:
        return JsonResponse({'error': 'district_id is required'}, status=400)
    
    upazillas = Upazilla.objects.filter(
        district_id=district_id, 
        is_active=True
    ).values('id', 'name', 'name_en')
    return JsonResponse({'upazillas': list(upazillas)})

@require_http_methods(["GET"])
def get_unions(request):
    """Get unions by upazilla ID"""
    upazilla_id = request.GET.get('upazilla_id')
    if not upazilla_id:
        return JsonResponse({'error': 'upazilla_id is required'}, status=400)
    
    unions = Union.objects.filter(
        upazilla_id=upazilla_id, 
        is_active=True
    ).values('id', 'name', 'name_en')
    return JsonResponse({'unions': list(unions)})

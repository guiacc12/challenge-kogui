from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
from .forms import LeadForm
import requests
import os


@csrf_protect
def lead_form(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()

            webhook_url = os.getenv('N8N_WEBHOOK_URL', '')
            print(f"Variável N8N_WEBHOOK_URL: '{webhook_url}'")
            if webhook_url:
                try:
                    payload = {
                        'name': lead.name,
                        'email': lead.email,
                        'telefone': lead.telefone,
                    }
                    print(f"Enviando webhook para: {webhook_url}")
                    print(f"Payload: {payload}")
                    response = requests.post(webhook_url, json=payload, timeout=5)
                    print(f"Resposta do webhook: {response.status_code} - {response.text}")
                    response.raise_for_status()
                except Exception as e:
                    print(f"Erro no webhook: {e}")
                    import traceback
                    traceback.print_exc()

            return JsonResponse({'ok': True})
        return JsonResponse({'ok': False, 'errors': form.errors}, status=422)
    else:
        form = LeadForm()
    return render(request, 'leads/lead_form.html', {'form': form})


def health(request):
    return HttpResponse('ok')
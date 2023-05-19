from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Video, ResultatAnalyse


def get_notion_pages(request):
    # Récupérer le header Authorization
    auth_header = request.headers.get('Authorization')

    # Vérifier si l'en-tête Authorization est présent et s'il commence par "Bearer"
    if auth_header and auth_header.startswith('Bearer '):
        # Extraire le token
        token = auth_header[7:]

        # Effectuer la requête GET à l'API de Notion avec le token
        response = requests.get("https://api.notion.com/v1/pages", headers={"Authorization": f"Bearer {token}"})

        # Vérifier le statut de la réponse
        if response.status_code == 200:
            # Récupérer les données de la réponse au format JSON
            data = response.json()

            # Traiter les données et effectuer les opérations nécessaires

            # Retourner une réponse JSON avec les données traitées
            return JsonResponse(data, status=200)
        else:
            # En cas d'erreur, retourner une réponse d'erreur appropriée
            return JsonResponse({"message": "Une erreur s'est produite lors de la récupération des pages."}, status=500)
    else:
        # Retourner une réponse d'erreur si le header Authorization est manquant ou mal formaté
        return JsonResponse({"message": "Autorisation invalide"}, status=401)



def update_notion_page(request, page_id):
    # Effectuez une requête PATCH à l'API de Notion pour mettre à jour une page spécifique
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        # Les données de mise à jour de la page
    }
    headers = {
        "Authorization": "Bearer secret_1VBniOlc5XOn1rdhIIfnd3mcTi9UAjBnRlIGVESiamI",
        "Content-Type": "application/json"
    }
    response = requests.patch(url, json=payload, headers=headers)

    # Vérifiez le statut de la réponse
    if response.status_code == 200:
        # Récupérez les données de la réponse au format JSON
        data = response.json()

        # Traitez les données et effectuez les opérations nécessaires

        # Retournez une réponse JSON avec les données traitées
        return JsonResponse(data, status=200)
    else:
        # En cas d'erreur, retournez une réponse d'erreur appropriée
        return JsonResponse({"message": "Une erreur s'est produite lors de la mise à jour de la page."}, status=500)
    
class MySecuredView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Code de traitement pour la vue sécurisée
        user = request.user  # Utilisateur authentifié
        return Response(f'Hello, {user.username}!')

    def post(self, request):
        # Code de traitement pour la vue sécurisée avec une méthode POST
        return Response('Post request processed.')

    def put(self, request, pk):
        # Code de traitement pour la vue sécurisée avec une méthode PUT
        return Response(f'Put request processed for id: {pk}.')




def envoyer_video(request):
    if request.method == 'POST':
        # Traitement de la vidéo envoyée
        titre = request.POST['titre']
        description = request.POST['description']
        fichier_video = request.FILES['fichier_video']
        
        # Enregistrer la vidéo dans la base de données
        video = Video(titre=titre, description=description, fichier_video=fichier_video)
        video.save()
        
        # Appel à l'API Whisper pour l'analyse vidéo
        # ...
        
        # Enregistrer les résultats d'analyse dans la base de données
        resultat = ResultatAnalyse(video_liee=video, resultats='Résultats d\'analyse')
        resultat.save()
        
        return render(request, 'video_envoyee.html')
    else:
        return render(request, 'envoyer_video.html')

def recuperer_resultats(request, video_id):
    video = Video.objects.get(pk=video_id)
    resultat = ResultatAnalyse.objects.get(video_liee=video)
    return render(request, 'resultats.html', {'video': video, 'resultat': resultat})
# Create your views here.

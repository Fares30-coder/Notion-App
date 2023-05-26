
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Video, ResultatAnalyse
from django.shortcuts import render
from notion.client import NotionClient
from notion.block import TextBlock


def create_entity(request):
    # Récupérer le token d'intégration Notion
    token = 'secret_1VBniOlc5XOn1rdhIIfnd3mcTi9UAjBnRlIGVESiamI'
    
    # Créer une instance de NotionClient
    client = NotionClient(token_v2=token)

    # Récupérer la page parente
    parent_page_url = 'https://www.notion.so/test-629eac2d9b424cd8bb11d7325f018e8e?pvs=4'
    parent_page = client.get_block(parent_page_url)

    # Créer une nouvelle page enfant
    new_page = parent_page.children.add_new(TextBlock, title='Nouvelle page')

    # Récupérer les données de la nouvelle page
    new_page_data = {
        'title': new_page.title,
        'url': new_page.get_browseable_url(),
    }

    return render(request, 'template_notion.html', {'new_page_data': new_page_data})


def home(request):
    return render(request, 'home.html')


def notion_integration(request):
    # Endpoint de l'API Notion pour récupérer une page
    notion_url = 'https://api.notion.com/v1/pages/{page_id}'

    # ID de la page Notion que vous souhaitez récupérer
    page_id = '1e9ea5d2-82c8-4d3b-8c79-490ca5206bd0'

    # Header d'autorisation pour l'API Notion
    headers = {
        'Authorization': 'Bearer secret_1VBniOlc5XOn1rdhIIfnd3mcTi9UAjBnRlIGVESiamI',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'  
    }

    # Effectuer la requête GET pour récupérer la page
    response = requests.get(notion_url.format(page_id=page_id), headers=headers)

    # Traiter la réponse de l'API Notion
    if response.status_code == 200:
        page_data = response.json()  # Données de la page récupérée
        # Effectuez ici les opérations souhaitées sur les données de la page

        # Renvoyer les résultats dans le rendu de votre choix
        return render(request, 'template_notion.html', {'page_data': page_data})
    else:
        # Gérer les erreurs éventuelles et fournir une réponse appropriée
        error_message = response.json().get('message', 'Une erreur s est produite.')
        return render(request, 'error.html', {'error_message': error_message})



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



""""
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
"""

"""def get_models_view(request):
    # Effectuer la requête GET pour obtenir les modèles
    headers = {
        'Authorization': 'Bearer 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',
    }
    response = requests.get('https://api.openai.com/v1/models', headers=headers)
    data = response.json()

    processed_data = []
    for model_data in data['models']:
        model = {
            'name': model_data['name'],
            'description': model_data['description'],
            # Autres informations pertinentes
        }
        processed_data.append(model)


    # Répondre avec les données traitées sous forme de réponse JSON
    return JsonResponse({'models': processed_data})
"""

def get_models_view(request):
    headers = {
        'Authorization': 'Bearer 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',
    }
    response = requests.get('https://api.openai.com/v1/models', headers=headers)
    data = response.json()

   # print(data)  # Print the response data for debugging purposes

    if 'models' in data:
        processed_data = []
        for model_data in data['models']:
            model = {
                'name': model_data['name'],
                'description': model_data['description'],
                # Autres informations pertinentes
            }
            processed_data.append(model)

        # Répondre avec les données traitées sous forme de réponse JSON
        return JsonResponse({'models': processed_data})
    else:
        # Handle the case when 'models' key is not present in the response
        error_message = "Error: 'models' key is not present in the API response"
        return JsonResponse({'error': error_message}, status=500)



def audio_transcription_view(request):
    if request.method == 'POST':
        # Récupérer le fichier audio envoyé dans la requête
        audio_file = request.FILES.get('audio_file')

        # Effectuer la requête POST pour transcrire l'audio
        headers = {
            'Authorization': 'Bearer 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',
        }
        files = {'file': audio_file}
        response = requests.post('https://api.openai.com/v1/audio/transcriptions', headers=headers, files=files)
        data = response.json()

        # Traiter les données de réponse
        if 'transcription' in data:
            transcription = data['transcription']
            # Faites quelque chose avec la transcription, comme l'afficher ou la sauvegarder

            # Retourner une réponse JSON avec la transcription
            return JsonResponse({'transcription': transcription})
        else:
            # Gérer les cas d'erreur si la transcription n'est pas présente dans la réponse
            return JsonResponse({'error': 'La transcription n\'est pas disponible'}, status=500)

    else:
        # Gérer le cas où la méthode HTTP n'est pas POST
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)



def transcribe_video(video_url):
    # Définir l'URL de l'API Whisper pour la transcription vidéo
    url = 'https://api.openai.com/v1/audio/transcriptions'
   
    # Définir les paramètres de la requête
    params = {
        'model': 'whisper-1.0',
        'audio': video_url,
    }

    # Ajouter l'en-tête d'authentification avec votre clé API
    headers = {
        'Authorization': f'Bearer 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',
    # Effectuer la requête POST à l'API Whisper
        'Content-Type': 'application/json',
    }

    response = requests.post(url, json=params, headers=headers)

    # Obtenir la réponse JSON
    data = response.json()
    #transcription = transcribe_video('React Native - How to make an image button in react-native .mp4')
    # Traiter la réponse
    if response.status_code == 200:
        # La requête a réussi
        transcription = data['transcription']
        return transcription
    else:
        # La requête a échoué
        error_message = data['error']
        return f"Erreur: {error_message}"
    


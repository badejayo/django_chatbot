from django.shortcuts import render
from django.http import JsonResponse
import cohere

# Create your views here.
def cohere_chat_bot(message):
  # Initialize the chat history
  chat_history = []

  # Define the preamble (Not needed because we have initial message)
  # print('Starting the chat. Type "quit" to end.\n')

  preamble_override = "You are connecting homeless people of color to social workers in Toronto"

  co = cohere.Client('ER2h4O9Vjk4gdTx0S1bYRttHGQIucPvpTwDWrg4r')

  # Chatbot response
  response = co.chat(model="command", message=message,  preamble_override=preamble_override, chat_history=chat_history, 
  documents=[
    {"title": "Emergency", "contact":"If you need emergency shelter, call 311 or Central Intake at 416-338-4766 for assistance."}, 
    {"title": "shelter", "mixed": "101 Placer Ct"},
    {"title": "shelter", "mixed": "1322 Bloor St W"},
    {"title": "shelter", "women": "1st Stop Woodlawn Residence"},
    {"title": "shelter",  "men": "705 Progress Ave Shelter Building E"},  
    {"title": "shelter", "mixed": "4117 Lawrence Ave E Scarborough ON M1E 2S2"},
    {"title": "shelter", "women": "67 Adelaide St E Toronto ON M5C 1K6"},
    {"title": "shelter", "mixed": "545 Lake Shore Blvd W Toronto ON M5V 1A3"} 
  ])
  
  # Add to chat history
  chat_history.extend(
      [{"role": "USER", "message": message},
      {"role": "CHATBOT", "message": response.text}]
  )

  return response.text

# This function handles the call to the Cohere API to give our chatbot response
def chatbot(request):
  # This is done so that we're only calling this on sends, not on initial page load
  if request.method == 'POST':
    message = request.POST.get('message')
    response = cohere_chat_bot(message)
    return JsonResponse({'message': message, 'response': response})

  return render(request, 'chatbot.html')

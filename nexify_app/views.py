from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from nexify_app.models import Chat, ChatMessage
from nexify_app.serializers import ChatMessageSerializer, ChatSerializer
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from groq import Groq   # ✅ Groq client

# Create your Groq client
groq_client = Groq(api_key=settings.GROQ_API_KEY)

# Time calculations
now = timezone.now()
today = now.date()
yesterday = today - timedelta(days=1)
seven_days_ago = today - timedelta(days=7)
thirty_days_ago = today - timedelta(days=30)


def createChatTitle(user_message):
    """Create a short descriptive title for the chat"""
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ Supported Groq model
            messages=[
                {"role": "system", "content": "Generate a short, descriptive title (max 5 words)."},
                {"role": "user", "content": user_message},
            ]
        )
        title = response.choices[0].message.content.strip()
    except Exception:
        title = user_message[:50]
    return title


@api_view(['POST'])
def prompt_gpt(request):
    """Handle user prompts and generate responses using Groq"""
    chat_id = request.data.get("chat_id")
    content = request.data.get("content")

    if not chat_id:
        return Response({"error": "Chat ID was not provided."}, status=400)

    if not content:
        return Response({"error": "There was no prompt passed."}, status=400)

    # Fetch or create chat
    chat, created = Chat.objects.get_or_create(id=chat_id)
    chat.title = createChatTitle(content)
    chat.save()

    # Save user message
    ChatMessage.objects.create(role="user", chat=chat, content=content)

    # Get recent chat history (last 10 messages)
    chat_messages = chat.messages.order_by("created_at")[:10]
    groq_messages = [{"role": msg.role, "content": msg.content} for msg in chat_messages]

    if not any(msg["role"] == "assistant" for msg in groq_messages):
        groq_messages.insert(0, {"role": "system", "content": "You are a helpful assistant."})

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ Groq chat model
            messages=groq_messages
        )
        reply = response.choices[0].message.content
    except Exception as e:
        return Response({"error": f"Groq API error: {str(e)}"}, status=500)

    # Save assistant reply
    ChatMessage.objects.create(role="assistant", chat=chat, content=reply)

    return Response({"reply": reply}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_chat_messages(request, pk):
    chat = get_object_or_404(Chat, id=pk)
    chatmessages = chat.messages.all()
    serializer = ChatMessageSerializer(chatmessages, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def todays_chat(request):
    chats = Chat.objects.filter(created_at__date=today).order_by("-created_at")[:10]
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def yesterdays_chat(request):
    chats = Chat.objects.filter(created_at__date=yesterday).order_by("-created_at")[:10]
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def seven_days_chat(request):
    chats = Chat.objects.filter(created_at__lt=yesterday, created_at__gte=seven_days_ago).order_by("-created_at")[:10]
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data)

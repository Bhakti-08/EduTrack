from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from main.models import StudentResponses, Questions,TestDetails,Students,StudentScores
import json

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("Connection closed with code: ", close_code)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']
        if message_type == 'save_answer':
            # Handle save_answer message
            await self.save_student_response(int(data['attempt_id']), int(data['question_id']), data['selected_option'])
            # Save answer to database
        elif message_type == 'timer_update':
            await self.save_student_timervalue(int(data['test_id']),data['student_id'],int(data['timer']))
    
    @database_sync_to_async
    def create_student_response(self, attempt_id, question_id, selected_option):
        attempt = StudentScores.objects.get(id=attempt_id)
        question = Questions.objects.get(id=question_id)
        response = StudentResponses.objects.update_or_create(attempt=attempt, question=question)[0]
        response.selectedAnswer=selected_option
        response.save()

    async def save_student_response(self, attempt_id, question_id, selected_option):
        await self.create_student_response(attempt_id, question_id, selected_option)

    @database_sync_to_async
    def create_student_timerecord(self,test_id,student_id,timer):
        test =  TestDetails.objects.get(id=test_id)
        student = Students.objects.get(registrationNum=student_id)
        update_value = StudentScores.objects.update_or_create(test=test,Student=student)[0]
        update_value.TimeRemaining = timer
        update_value.save()

    async def save_student_timervalue(self,test_id,student_id,timer):
        await self.create_student_timerecord(test_id,student_id,timer)

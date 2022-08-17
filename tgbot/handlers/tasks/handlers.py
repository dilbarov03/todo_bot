from django.utils import timezone
from telegram import ParseMode, Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from tgbot.models import User
from tasks.models import Tasks
from tgbot.handlers.tasks.keyboards import main_keyboard
from tgbot.handlers.tasks import keyboards

import pretty_errors

priorities = {
   "high": 1,
   "medium": 2,
   "low": 3
}

l1 = ["create-high", "create-medium", "create-low"]

todo_priority = {
   1: "🔴",
   2: "🟠",
   3: "🔵"
}

todo_status = {
   True: "✅",
   False: "🕓"
}

def tasks_start(update: Update, context: CallbackContext) -> None:
   user = User.objects.get(user_id=update.effective_user.id)
   todos = Tasks.objects.users_tasks(user)
   
   inline_keyboard = main_keyboard()


   txt = ""

   if len(todos)==0:
     txt = "You have no todo tasks"
   else:
      txt = "<b>Your tasks:</b>\n\n"
      for todo in todos:
         txt += f"{todo_priority[todo.priority]} {todo.title} - {todo_status[todo.status]}\n"

      txt += "\n\n🔴 <i>High priority</i>\n🟠 <i>Medium priority</i>\n🔵 <i>Low priority</i>"


   if update.callback_query:
      try:
         update.callback_query.message.edit_text(
            text=txt, reply_markup=inline_keyboard,
            parse_mode=ParseMode.HTML
         )
      except:
         context.bot.send_message(chat_id=update.effective_user.id, text=txt, parse_mode='html', reply_markup=inline_keyboard)
   else:
      update.message.reply_text(txt, parse_mode='html', reply_markup=inline_keyboard)

def calback_handler(update: Update, context: CallbackContext) -> None:
   data = update.callback_query.data
   text = ""
   keyboard = keyboards.cancel_keyboard()

   if data=="add-todo":
      text = "Send the name of the task"
      context.user_data['action'] = "set-name"
      context.user_data['msg-id'] = update.callback_query.message.message_id

      context.bot.edit_message_text(
         text=text,
         chat_id=update.callback_query.message.chat_id,
         message_id=update.callback_query.message.message_id,
         parse_mode=ParseMode.HTML,
         reply_markup=keyboard
      )   
   
   elif data in l1:
      data = data.split("-")
      action = data[0]
      value = data[1]
      title = context.user_data['title']
      priority = priorities[value]
      user = User.objects.get(user_id=update.effective_user.id)

      if action=="create":

         new_task = Tasks(title=title, priority=priority, user=user)
         new_task.save()
         context.bot.delete_message(chat_id = update.effective_user.id, message_id = update.callback_query.message.message_id)
         context.bot.send_message(chat_id = update.effective_user.id, text="✅ Task added successfully")
         tasks_start(update, context)

   elif data=="edit-todo":
      text = "Select the task to edit:"
      context.bot.edit_message_text(
         text=text,
         chat_id=update.callback_query.message.chat_id,
         message_id=update.callback_query.message.message_id,
         parse_mode=ParseMode.HTML,
         reply_markup=keyboards.edit_tasks_keyboard(update.effective_user.id)
      )

   elif data.startswith("edit-"):
      data = data.split("-")
      todo_id = data[1]

      todo_priority = {
         1: "🔴 High",
         2: "🟠 Medium",
         3: "🔵 Low"
      }

      todo_status = {
         True: "✅ Completed",
         False: "🕓 Active"
      }

      call_status = {
         True: "completed",
         False: "active"         
      }

      call_priority = {
         1: "high",
         2: "medium",
         3: "low"
      }

      task = Tasks.objects.get(id=todo_id)
      
      print(data)

      try:
         content = data[2].split("/")
         action = data[3]
         print(f"Content: {content}")
         status = ""
         if content[0]=="completed":
            status = True
         elif content[0]=="active":
            status = False
         
        
         priority = ""
         if content[1] == "high":
            priority = 1
         elif content[1] == "medium":
            priority = 2
         elif content[1] == "low":
            priority = 3               

         if action=="save":
            context.bot.delete_message(chat_id=update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id,)
            task.status = status
            task.priority = priority
            task.save()
            tasks_start(update, context)
            return    

      except:
         status = task.status
         priority = task.priority
      
      txt = f"<b>Task:</b> {task.title}\n<b>Status</b>: {todo_status[status]}\n<b>Priority</b>: {todo_priority[priority]}\n\nClick the buttons below to edit status or priority"       

      context.bot.edit_message_text(
         text=txt,
         chat_id=update.callback_query.message.chat_id,
         message_id=update.callback_query.message.message_id,
         parse_mode=ParseMode.HTML,
         reply_markup=keyboards.detail_edit(todo_id, call_status[status], call_priority[priority])
      )

   elif data=="delete-todo":
      text = "Select the task to delete:"
      context.bot.edit_message_text(
         text=text,
         chat_id=update.callback_query.message.chat_id,
         message_id=update.callback_query.message.message_id,
         parse_mode=ParseMode.HTML,
         reply_markup=keyboards.delete_tasks_keyboard(update.effective_user.id)
      )

   elif data.startswith("delete-"):
      data = data.split("-")
      task_id = data[1]

      task = Tasks.objects.get(id=task_id)
      task.delete()

      context.bot.delete_message(chat_id=update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id,)
      tasks_start(update, context)
      

   elif data=="cancel":
      context.user_data["action"] = "nothing"
      tasks_start(update, context)

   elif data=="clear-todo":
      user = User.objects.get(user_id=update.effective_user.id)
      todos = Tasks.objects.users_tasks(user)

      for todo in todos:
         todo.delete()

      context.bot.delete_message(chat_id=update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id,)
      #context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="Deleted successfully")
      tasks_start(update, context)     


def set_name(update: Update, context: CallbackContext) -> None:
   action = context.user_data['action']
   if action=="set-name":
      context.user_data['title'] = update.message.text
      context.user_data["action"] = "nothing"
      text = "Set the priority:"
      try:
         context.bot.delete_message(chat_id = update.effective_user.id, message_id = context.user_data['msg-id'])
      except:
         pass
      update.message.reply_text(text, reply_markup=keyboards.priority_keyboard("create"))
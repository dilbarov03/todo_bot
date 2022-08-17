from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup

from tgbot.models import User
from tasks.models import Tasks

from tgbot.handlers.tasks import handlers

def edit_tasks_keyboard(tg_user) -> InlineKeyboardMarkup:
   buttons = []
   user = User.objects.get(user_id=tg_user)
   todos = Tasks.objects.users_tasks(user)

   for todo in todos:
      buttons.append([InlineKeyboardButton(
         f"{handlers.todo_priority[todo.priority]} {todo.title} - {handlers.todo_status[todo.status]}", callback_data=f'edit-{todo.id}'), ])
   buttons.append([InlineKeyboardButton("Cancel", callback_data="cancel")])

   return InlineKeyboardMarkup(buttons)

def delete_tasks_keyboard(tg_user) -> InlineKeyboardMarkup:
   buttons = []
   user = User.objects.get(user_id=tg_user)
   todos = Tasks.objects.users_tasks(user)

   for todo in todos:
      buttons.append([InlineKeyboardButton(
         f"{handlers.todo_priority[todo.priority]} {todo.title} - {handlers.todo_status[todo.status]}", callback_data=f'delete-{todo.id}'), ])
   buttons.append([InlineKeyboardButton("Cancel", callback_data="cancel")])

   return InlineKeyboardMarkup(buttons)

def detail_edit(todo_id, status, priority):
   buttons = [
      [
         InlineKeyboardButton("🕓 Active", callback_data=f'edit-{todo_id}-active/{priority}-cancel'), 
         InlineKeyboardButton("✅ Completed", callback_data=f'edit-{todo_id}-completed/{priority}-cancel') 
      ],
      [
         InlineKeyboardButton("🔴 High", callback_data=f'edit-{todo_id}-{status}/high-cancel'),
         InlineKeyboardButton("🟠 Medium", callback_data=f'edit-{todo_id}-{status}/medium-cancel'),
         InlineKeyboardButton("🔵 Low", callback_data=f'edit-{todo_id}-{status}/low-cancel')
      ],
      [
         InlineKeyboardButton("Save", callback_data=f'edit-{todo_id}-{status}/{priority}-save'), 
         InlineKeyboardButton("Cancel", callback_data=f'cancel') 
      ],      
   ]

   return InlineKeyboardMarkup(buttons)


def main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
      [
         InlineKeyboardButton("Add todo ", callback_data=f'add-todo'), 
         InlineKeyboardButton("Edit todo", callback_data=f'edit-todo')
      ],
      [
         InlineKeyboardButton("Delete todo ", callback_data=f'delete-todo'), 
         InlineKeyboardButton("Clear todo list", callback_data=f'clear-todo')
      ],
    ]
    return InlineKeyboardMarkup(buttons)

def cancel_keyboard():
   button = [
      [InlineKeyboardButton("Cancel", callback_data=f'cancel')]
   ]

   return InlineKeyboardMarkup(button)

def priority_keyboard(action):
   buttons = [
      [InlineKeyboardButton("🔴 High", callback_data=f'{action}-high'),
      InlineKeyboardButton("🟠 Medium", callback_data=f'{action}-medium'),
      InlineKeyboardButton("🔵 Low", callback_data=f'{action}-low')],
      [InlineKeyboardButton("Cancel", callback_data=f'cancel')]
   ]

   return InlineKeyboardMarkup(buttons)
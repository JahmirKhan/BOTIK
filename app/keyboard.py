from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)

actions = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Detailed Text Analysis'), KeyboardButton(text='Vocabulary Enrichment')],
                                     [KeyboardButton(text='Create Grammar Exercises'), KeyboardButton(text='Check Grammar')],],
                                      resize_keyboard=True,)    
